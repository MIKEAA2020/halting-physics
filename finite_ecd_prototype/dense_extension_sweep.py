#!/usr/bin/env python3
"""Phase 6 extension: comparative scaling study on dense-chain n=17, 18.

Applies the fixed external-baseline protocol of the recorded phase 6 study
(``mechanics_baseline_sweep.py``) to the four dense-family extension
instances: 60-second wall-clock timeout, 3 GiB address-space cap, three
repetitions per solver and instance with the median reported, single-threaded
deterministic configurations, identical encodings emitted once, and the native
tree-decomposition DP pipeline as a bounded isolated process
(``native_dp_runner.py``) with certificate re-verification and policy
reconstruction. External SAT models are verified natively as policies;
external UNSAT answers are cross-checked against verified DP-REFUTATION
certificates.

The run is checkpointed per (case, solver) unit because the environment
terminates long-running sessions: every unit is an unmodified invocation of
the recorded runner functions under the fixed limits, and progress is
persisted after each unit. ``--finalize`` assembles
``reports/mechanics_dense_extension_sweep.json``.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path
from types import SimpleNamespace

PROTO = Path(__file__).resolve().parent
sys.path.insert(0, str(PROTO))

import mechanics_baseline_sweep as mbs  # noqa: E402
from external_baseline_sweep import (  # noqa: E402
    MEMORY_LIMIT_BYTES, TIMEOUT_SECONDS, median, model_to_policy,
    run_cpsat, run_highs, run_kissat, run_minisat, run_z3,
)
from baseline_encode import to_cpsat_json, to_dimacs, to_milp_lp  # noqa: E402
from finite_ecd import Instance, verify_policy  # noqa: E402

ROOT = PROTO
PROGRESS = ROOT / "reports" / "dense_ext_sweep_progress.json"
OUT = ROOT / "reports" / "mechanics_dense_extension_sweep.json"

# (family, size, observation, instance prefix, expected)
CASES = [
    ("dense-chain", 17, "same", "examples/mech_dense17_same", "UNSAT"),
    ("dense-chain", 17, "split", "examples/mech_dense17_split", "SAT"),
    ("dense-chain", 18, "same", "examples/mech_dense18_same", "UNSAT"),
    ("dense-chain", 18, "split", "examples/mech_dense18_split", "SAT"),
]
SOLVER_ORDER = ["minisat", "kissat", "z3", "cpsat", "highs"]


def load_progress() -> dict:
    if PROGRESS.exists():
        return json.loads(PROGRESS.read_text())
    return {}


def save_progress(p: dict) -> None:
    PROGRESS.write_text(json.dumps(p, indent=2))


def discover() -> dict:
    args = SimpleNamespace(
        minisat=os.environ.get("EXTERNAL_ECD_MINISAT") or shutil.which("minisat"),
        kissat=os.environ.get("EXTERNAL_ECD_KISSAT") or shutil.which("kissat"),
        z3=os.environ.get("EXTERNAL_ECD_Z3") or shutil.which("z3"),
        cpsat_python=os.environ.get("EXTERNAL_ECD_CPSAT_PYTHON"),
        highs_python=os.environ.get("EXTERNAL_ECD_HIGHS_PYTHON"),
    )
    return mbs.discover_solvers(args)


def encode_case(family, size, obs, prefix, inst_raw):
    cnf_path = Path(prefix + ".cnf")
    cpsat_path = Path(prefix + "_cpsat.json")
    lp_path = Path(prefix + ".lp")
    t0 = time.perf_counter()
    cnf_text = to_dimacs(inst_raw)
    encode_seconds = time.perf_counter() - t0
    cnf_path.write_text(cnf_text)
    cpsat_path.write_text(json.dumps(to_cpsat_json(inst_raw), indent=2))
    lp_path.write_text(to_milp_lp(inst_raw))
    return {
        "cnf_clauses": cnf_text.count(" 0\n"),
        "encode_seconds": round(encode_seconds, 6),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=None,
                    help="comma-separated family|size|obs keys (default: all)")
    ap.add_argument("--solvers", default=None,
                    help="comma-separated solver names (default: all)")
    ap.add_argument("--repetitions", type=int, default=3)
    ap.add_argument("--finalize", action="store_true")
    args = ap.parse_args()

    selected = CASES
    if args.cases:
        keys = {k.strip() for k in args.cases.split(",") if k.strip()}
        selected = [c for c in CASES if f"{c[0]}|{c[1]}|{c[2]}" in keys]
        if not selected:
            raise SystemExit("--cases selected no cases")
    want_solvers = None
    if args.solvers:
        want_solvers = [s.strip() for s in args.solvers.split(",") if s.strip()]

    progress = load_progress()

    if not args.finalize:
        solvers = discover()
        if want_solvers is not None:
            solvers = {k: v for k, v in solvers.items() if k in want_solvers}
        if not solvers:
            raise SystemExit("no solvers discovered")

        for family, size, obs, prefix, expected in selected:
            key = f"{family}|{size}|{obs}"
            rec = progress.setdefault(key, {})
            inst_path = ROOT / (prefix + "_instance.json")
            dec_path = ROOT / (prefix + "_tree_decomp.json")
            if not inst_path.exists() or not dec_path.exists():
                rec["missing_instance"] = True
                save_progress(progress)
                continue
            inst_raw = json.loads(inst_path.read_text())
            if "encoded" not in rec:
                rec["encoded"] = encode_case(family, size, obs, prefix, inst_raw)
                rec["variables"] = len(inst_raw["variables"])
                rec["factors"] = len(inst_raw["factors"])
                save_progress(progress)

            if "native" not in rec:
                native = mbs.native_run(inst_path, dec_path, ROOT / prefix)
                rec["native"] = native
                save_progress(progress)
                print(f"  {key} native: {native.get('status')} "
                      f"{native.get('wall_seconds')}s", flush=True)

            inst_obj = Instance.from_json(inst_raw)
            native_refutation_verified = (
                rec["native"].get("status") == "DP-REFUTATION"
                and rec["native"].get("certificate_verified"))

            ext = rec.setdefault("external", {})
            for name in SOLVER_ORDER:
                if name not in solvers or name in ext:
                    continue
                reps = []
                for r in range(args.repetitions):
                    if name == "minisat":
                        resfile = Path(prefix + f"_minisat_res_{r}")
                        raw = run_minisat(solvers[name]["exe"],
                                          ROOT / (prefix + ".cnf"), resfile)
                    elif name == "kissat":
                        raw = run_kissat(solvers[name]["exe"], ROOT / (prefix + ".cnf"))
                    elif name == "z3":
                        raw = run_z3(solvers[name]["exe"], ROOT / (prefix + ".cnf"))
                    elif name == "highs":
                        raw = run_highs(solvers[name]["exe"], ROOT / (prefix + ".lp"))
                    else:
                        raw = run_cpsat(solvers[name]["exe"],
                                        ROOT / (prefix + "_cpsat.json"))
                    reps.append(raw)
                seconds = [r["seconds"] for r in reps]
                rep = reps[0]
                cls = rep["classification"]
                cross = {"status": "INCONCLUSIVE",
                         "reason": "external run did not produce a recognised status"}
                if cls == "SAT":
                    if name in ("cpsat", "highs"):
                        policy = rep.get("model")
                        if policy is not None:
                            policy = {k: int(v) for k, v in policy.items()}
                    else:
                        policy = model_to_policy(rep.get("model"), inst_raw["variables"])
                    if policy is None:
                        cross = {"status": "INCONCLUSIVE",
                                 "reason": "external model incomplete or unparsable"}
                    else:
                        ok, errors = verify_policy(inst_obj, policy)
                        if ok:
                            cross = {"status": "VERIFIED-SAT",
                                     "external_status": "CERTIFIED-SAT-EXTERNAL",
                                     "model_policy_verified": True}
                        else:
                            cross = {"status": "REJECTED", "errors": errors}
                elif cls == "UNSAT":
                    if native_refutation_verified:
                        cross = {"status": "VERIFIED-UNSAT",
                                 "external_status": "CERTIFIED-UNSAT-EXTERNAL",
                                 "native_certificate": "DP-REFUTATION verified"}
                    else:
                        cross = {"status": "INCONCLUSIVE",
                                 "reason": "no verified native DP-REFUTATION for cross-check"}
                entry = {
                    "solver": name,
                    "classification": cls,
                    "seconds_median": round(median(seconds), 6),
                    "seconds_min": round(min(seconds), 6),
                    "seconds_max": round(max(seconds), 6),
                    "peak_rss_kib": max(r.get("peak_rss_kib") or 0 for r in reps),
                    "returncode": rep.get("returncode"),
                    "cross_check": cross,
                }
                for extra in ("build_seconds", "solve_seconds", "inner_peak_rss_kib"):
                    if rep.get(extra) is not None:
                        entry[extra] = rep[extra]
                ext[name] = entry
                save_progress(progress)
                print(f"  {key} {name}: {cls} {entry['seconds_median']}s "
                      f"cross={cross['status']}", flush=True)
        print("UNITS DONE")
        return

    # ---- finalize ----
    fe_map = {}
    ext_gen = ROOT / "reports" / "mechanics_dense_extension.json"
    if ext_gen.exists():
        data = json.loads(ext_gen.read_text())
        for case in data.get("cases", []):
            k = f"{case['family']}|{case['size']}|{case['observation']}"
            fe_map[k] = {
                "fe_generate_seconds": case.get("fe_generate_seconds"),
                "fe_verify_seconds": case.get("fe_verify_seconds"),
                "instance_bytes": case.get("instance_bytes"),
                "row_batch_bytes": case.get("row_batch_bytes"),
                "generation_wall_seconds": case.get("generation_wall_seconds"),
                "instance_status": case.get("instance_status"),
            }
    solvers = discover()
    from external_baseline_sweep import hardware_info
    protocol = {
        "timeout_seconds": TIMEOUT_SECONDS,
        "memory_limit_bytes": MEMORY_LIMIT_BYTES,
        "memory_limit_note": "address space cap applied to every solver process and to the native runner",
        "repetitions": args.repetitions,
        "timing": "wall clock over the whole process; median of repetitions reported",
        "determinism": "single-threaded configurations; CP-SAT num_workers=1 with "
                       "random_seed=1; minisat and kissat default deterministic "
                       "configurations; no randomization flags otherwise",
        "hardware": hardware_info(),
        "solvers": {k: v["version"] for k, v in solvers.items()},
        "native_pipeline": "native_dp_runner.py: load instance, tree-decomposition DP, "
                           "certificate re-verification, policy reconstruction and "
                           "verification, certificate emission; bounded by the same "
                           "timeout and address-space cap",
        "fe_accounting": "FE preprocessing and certified relation generation are "
                         "recorded separately in reports/mechanics_dense_extension.json "
                         "and excluded from both native and external timings",
        "cross_check_discipline": "external SAT models are verified natively as policies "
                                  "on the original instance; external UNSAT answers are "
                                  "cross-checked against verified DP-REFUTATION "
                                  "certificates; solver logs are not certificates",
        "extension_note": "dense-family extension of the recorded phase 6 study beyond "
                          "the recorded boundary n=16; the run is checkpointed per "
                          "(case, solver) unit because the environment terminates "
                          "long-running sessions; every unit is an unmodified invocation "
                          "of the recorded runner functions under the fixed limits",
    }

    cases_out = []
    for family, size, obs, prefix, expected in CASES:
        key = f"{family}|{size}|{obs}"
        rec = progress.get(key)
        if rec is None:
            cases_out.append({"family": family, "size": size, "observation": obs,
                              "status": "NOT-RUN"})
            continue
        entry = {
            "family": family,
            "size": size,
            "observation": obs,
            "instance": prefix + "_instance.json",
            "variables": rec.get("variables"),
            "factors": rec.get("factors"),
            "cnf_clauses": rec.get("encoded", {}).get("cnf_clauses"),
            "encode_seconds": rec.get("encoded", {}).get("encode_seconds"),
            "fe_preprocessing": fe_map.get(key, {}),
            "expected": expected,
            "native": rec.get("native"),
            "external": [rec.get("external", {}).get(s) for s in SOLVER_ORDER
                         if rec.get("external", {}).get(s)],
        }
        cases_out.append(entry)

    def ext_iter():
        for c in cases_out:
            for e in c.get("external", []):
                yield c, e

    summary = {
        "instances": len(cases_out),
        "native_certificates_verified": sum(
            1 for c in cases_out if (c.get("native") or {}).get("certificate_verified")),
        "native_policies_verified": sum(
            1 for c in cases_out if (c.get("native") or {}).get("policy_verified")),
        "native_inconclusive": sum(
            1 for c in cases_out if (c.get("native") or {}).get("status") == "INCONCLUSIVE"),
        "external_runs": sum(1 for _ in ext_iter()),
        "external_sat_cross_checked": sum(
            1 for _, e in ext_iter() if e["cross_check"]["status"] == "VERIFIED-SAT"),
        "external_unsat_cross_checked": sum(
            1 for _, e in ext_iter() if e["cross_check"]["status"] == "VERIFIED-UNSAT"),
        "external_inconclusive": sum(
            1 for _, e in ext_iter() if e["cross_check"]["status"] == "INCONCLUSIVE"),
        "external_rejected": sum(
            1 for _, e in ext_iter() if e["cross_check"]["status"] == "REJECTED"),
        "status_agreement_with_native": sum(
            1 for c, e in ext_iter()
            if e["classification"] is not None
            and (c.get("native") or {}).get("status") is not None
            and e["classification"] == c["native"]["status"].replace(
                "DP-", "").replace("OPTIMUM", "SAT").replace("REFUTATION", "UNSAT")
            and e["cross_check"]["status"] in ("VERIFIED-SAT", "VERIFIED-UNSAT")),
    }
    out = {"status": "COMPLETE",
           "phase": "6-extension comparative scaling study on dense-chain n=17,18",
           "protocol": protocol, "cases": cases_out, "summary": summary}
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
