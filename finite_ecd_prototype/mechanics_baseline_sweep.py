#!/usr/bin/env python3
"""Phase 6 comparative scaling study on mechanics-derived instances.

The same fixed protocol as the recorded external-baseline sweep is applied to
Boolean finite instances derived from the mechanics benchmark families:
identical instances encoded once by the artifact's encoders (DIMACS CNF for
minisat, kissat, and z3; the LP-format MILP encoding for HiGHS; the minimal
forbidden-tuple encoding for CP-SAT); a 60-second wall-clock timeout; a 3 GiB
address-space cap; three repetitions per solver and instance with the median
reported; single-threaded deterministic configurations (CP-SAT with one
worker and fixed seed).

The native tree-decomposition dynamic program runs under the same limits, as
an isolated process (``native_dp_runner.py``) that emits and re-verifies its
certificate and reconstructs and verifies a policy when satisfiable, so
native and external wall-clock figures cover comparable whole-process
pipelines. FE preprocessing (model generation, certified relation
generation, and independent verification) is accounted separately from the
recorded mechanics benchmark suite rather than charged to either side.

Cross-checking discipline is unchanged: external satisfiable models are
parsed, converted to policies, and verified natively; external unsatisfiable
answers are cross-checked against natively verified ``DP-REFUTATION``
certificates; timeouts, crashes, and unrecognised output remain
INCONCLUSIVE.

Primary output: ``reports/mechanics_external_baseline_sweep.json``.
"""
from __future__ import annotations

import argparse
import json
import os
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from baseline_encode import to_cpsat_json, to_dimacs, to_milp_lp
from external_baseline_sweep import (MEMORY_LIMIT_BYTES, ROOT, TIMEOUT_SECONDS,
                                      hardware_info, median, model_to_policy,
                                      run_cpsat, run_highs, run_kissat,
                                      run_minisat, run_z3)
from finite_ecd import Instance, verify_policy

NATIVE_RUNNER = ROOT / "native_dp_runner.py"

# (family label, size, observation, instance prefix, expected)
CASES = [
    ("ten-bar", 1, "same", "examples/mech_ten_bar_same", "UNSAT"),
    ("ten-bar", 1, "split", "examples/mech_ten_bar_split", "SAT"),
    ("chain-pretension", 256, "same", "examples/mech_chain256_same", "UNSAT"),
    ("chain-pretension", 256, "split", "examples/mech_chain256_split", "SAT"),
    ("chain-pretension", 1024, "same", "examples/mech_chain1024_same", "UNSAT"),
    ("chain-pretension", 1024, "split", "examples/mech_chain1024_split", "SAT"),
    ("dense-chain", 8, "same", "examples/mech_dense8_same", "UNSAT"),
    ("dense-chain", 8, "split", "examples/mech_dense8_split", "SAT"),
    ("dense-chain", 16, "same", "examples/mech_dense16_same", "UNSAT"),
    ("dense-chain", 16, "split", "examples/mech_dense16_split", "SAT"),
    ("lattice", 1, "same", "examples/mech_latticeC1_same", "UNSAT"),
    ("lattice", 1, "split", "examples/mech_latticeC1_split", "SAT"),
    ("lattice", 2, "same", "examples/mech_latticeC2_same", "UNSAT"),
    ("lattice", 2, "split", "examples/mech_latticeC2_split", "SAT"),
]


def fe_preprocessing_map() -> Dict[str, Dict[str, Any]]:
    """FE stage accounting from the recorded phase 4 mechanics benchmarks."""
    path = ROOT / "reports" / "mechanics_benchmarks.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    out: Dict[str, Dict[str, Any]] = {}
    for case in data.get("cases", []):
        key = f"{case['family']}|{case['size']}|{case['observation']}"
        out[key] = {
            "fe_generate_seconds": case.get("fe_generate_seconds"),
            "fe_verify_seconds": case.get("fe_verify_seconds"),
            "instance_bytes": case.get("instance_bytes"),
            "row_batch_bytes": case.get("row_batch_bytes"),
        }
    return out


def native_run(inst_path: Path, dec_path: Path, out_prefix: Path) -> Dict[str, Any]:
    """Run the native DP pipeline as a bounded subprocess."""
    cert_path = Path(str(out_prefix) + "_native_dp_certificate.json")
    cmd = [sys.executable, str(NATIVE_RUNNER), str(inst_path),
           "--decomp", str(dec_path), "--out", str(cert_path)]
    t0 = time.perf_counter()
    with open(Path(str(out_prefix) + "_native_stdout.txt"), "w") as so, \
         open(Path(str(out_prefix) + "_native_stderr.txt"), "w") as se:
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=so, stderr=se,
                                preexec_fn=lambda: resource.setrlimit(
                                    resource.RLIMIT_AS,
                                    (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES)))
        try:
            proc.wait(timeout=TIMEOUT_SECONDS + 30.0)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            rc = "TIMEOUT"
    elapsed = time.perf_counter() - t0
    if rc == "TIMEOUT":
        return {"status": "INCONCLUSIVE",
                "reason": "native pipeline exceeded the wall-clock limit",
                "wall_seconds": round(elapsed, 6)}
    try:
        payload = json.loads(Path(str(out_prefix) + "_native_stdout.txt").read_text())
    except Exception:
        return {"status": "INCONCLUSIVE",
                "reason": "native runner output unparsable",
                "returncode": rc,
                "wall_seconds": round(elapsed, 6)}
    payload["status"] = payload.get("status", "INCONCLUSIVE")
    payload["wall_seconds"] = round(elapsed, 6)
    payload["certificate_file"] = str(cert_path.relative_to(ROOT)) if cert_path.exists() else None
    return payload


def discover_solvers(args):
    solvers = {}
    if args.minisat:
        solvers["minisat"] = {"exe": args.minisat,
                              "version": "minisat 2.2 series (arminbiere mirror "
                                         "commit 16982a5, gcc 14.2, -O3)"}
    if args.kissat:
        solvers["kissat"] = {"exe": args.kissat,
                             "version": "kissat 4.0.4 (commit 8af8e56, gcc 14.2, -O3)"}
    if args.z3:
        from external_baseline_sweep import _solver_version
        solvers["z3"] = {"exe": args.z3, "version": _solver_version(args.z3)}
    cpsat_python = args.cpsat_python
    if cpsat_python is None:
        try:
            import importlib.metadata as md
            md.version("ortools")
            cpsat_python = sys.executable
        except Exception:
            cpsat_python = None
    if cpsat_python:
        try:
            import importlib.metadata as md
            ver = md.version("ortools") if cpsat_python == sys.executable else None
        except Exception:
            ver = None
        if ver is None:
            p = subprocess.run([cpsat_python, "-c",
                                "import importlib.metadata as m; print(m.version('ortools'))"],
                               capture_output=True, text=True, timeout=60)
            ver = p.stdout.strip() or "unknown"
        solvers["cpsat"] = {"exe": cpsat_python, "version": f"OR-Tools CP-SAT {ver}"}
    highs_python = args.highs_python
    if highs_python is None:
        try:
            import importlib.metadata as md
            md.version("highspy")
            highs_python = sys.executable
        except Exception:
            highs_python = None
    if highs_python:
        try:
            import importlib.metadata as md
            ver = md.version("highspy") if highs_python == sys.executable else None
        except Exception:
            ver = None
        if ver is None:
            p = subprocess.run([highs_python, "-c",
                                "import importlib.metadata as m; print(m.version('highspy'))"],
                               capture_output=True, text=True, timeout=60)
            ver = p.stdout.strip() or "unknown"
        solvers["highs"] = {"exe": highs_python, "version": f"HiGHS MILP {ver}"}
    return solvers


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/mechanics_external_baseline_sweep.json")
    ap.add_argument("--repetitions", type=int, default=3)
    ap.add_argument("--only", default=None,
                    help="comma-separated family|size|obs keys restricting the run")
    ap.add_argument("--merge", action="store_true",
                    help="merge the run into an existing report instead of replacing it")
    ap.add_argument("--minisat", default=os.environ.get("EXTERNAL_ECD_MINISAT")
                    or shutil.which("minisat"))
    ap.add_argument("--kissat", default=os.environ.get("EXTERNAL_ECD_KISSAT")
                    or shutil.which("kissat"))
    ap.add_argument("--z3", default=os.environ.get("EXTERNAL_ECD_Z3")
                    or shutil.which("z3"))
    ap.add_argument("--cpsat-python",
                    default=os.environ.get("EXTERNAL_ECD_CPSAT_PYTHON"))
    ap.add_argument("--highs-python",
                    default=os.environ.get("EXTERNAL_ECD_HIGHS_PYTHON"))
    args = ap.parse_args()

    (ROOT / "reports").mkdir(exist_ok=True)
    solvers = discover_solvers(args)
    fe_map = fe_preprocessing_map()

    if not solvers:
        out = {
            "status": "INCONCLUSIVE",
            "reason": "no supported external solver installed",
            "protocol": {
                "timeout_seconds": TIMEOUT_SECONDS,
                "memory_limit_bytes": MEMORY_LIMIT_BYTES,
                "hardware": hardware_info(),
            },
        }
        (ROOT / args.out).write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2))
        return

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
                         "recorded separately from the recorded mechanics benchmark "
                         "suite and excluded from both native and external timings",
        "cross_check_discipline": "external SAT models are verified natively as policies "
                                  "on the original instance; external UNSAT answers are "
                                  "cross-checked against verified DP-REFUTATION "
                                  "certificates; solver logs are not certificates",
    }

    selected = CASES
    if args.only:
        keys = {k.strip() for k in args.only.split(",") if k.strip()}
        selected = [c for c in CASES if f"{c[0]}|{c[1]}|{c[2]}" in keys]
        if not selected:
            raise SystemExit("--only selected no cases")

    cases_out = []
    for family, size, obs, prefix, expected in selected:
        inst_path = ROOT / (prefix + "_instance.json")
        dec_path = ROOT / (prefix + "_tree_decomp.json")
        if not inst_path.exists() or not dec_path.exists():
            cases_out.append({
                "family": family, "size": size, "observation": obs,
                "status": "MISSING-INSTANCE",
                "note": "run mechanics_benchmarks.py first",
            })
            continue
        inst_raw = json.loads(inst_path.read_text())
        variables = inst_raw["variables"]
        cnf_path = Path(prefix + ".cnf")
        cpsat_path = Path(prefix + "_cpsat.json")
        lp_path = Path(prefix + ".lp")
        t0 = time.perf_counter()
        cnf_text = to_dimacs(inst_raw)
        encode_seconds = time.perf_counter() - t0
        cnf_path.write_text(cnf_text)
        cpsat_path.write_text(json.dumps(to_cpsat_json(inst_raw), indent=2))
        lp_path.write_text(to_milp_lp(inst_raw))
        n_clauses = cnf_text.count(" 0\n")

        native = native_run(inst_path, dec_path, ROOT / prefix)
        native_refutation_verified = (
            native.get("status") == "DP-REFUTATION" and native.get("certificate_verified"))

        entry = {
            "family": family,
            "size": size,
            "observation": obs,
            "instance": prefix + "_instance.json",
            "variables": len(variables),
            "factors": len(inst_raw["factors"]),
            "cnf_clauses": n_clauses,
            "encode_seconds": round(encode_seconds, 6),
            "fe_preprocessing": fe_map.get(f"{family}|{size}|{obs}", {}),
            "expected": expected,
            "native": native,
            "external": [],
        }

        inst_obj = Instance.from_json(inst_raw)
        for name, cfg in solvers.items():
            reps = []
            for r in range(args.repetitions):
                if name == "minisat":
                    resfile = Path(prefix + f"_minisat_res_{r}")
                    raw = run_minisat(cfg["exe"], cnf_path, resfile)
                elif name == "kissat":
                    raw = run_kissat(cfg["exe"], cnf_path)
                elif name == "z3":
                    raw = run_z3(cfg["exe"], cnf_path)
                elif name == "highs":
                    raw = run_highs(cfg["exe"], lp_path)
                else:
                    raw = run_cpsat(cfg["exe"], cpsat_path)
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
                    policy = model_to_policy(rep.get("model"), variables)
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
            ext = {
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
                    ext[extra] = rep[extra]
            entry["external"].append(ext)
            print(f"  {family} {size} {obs} {name}: {cls} "
                  f"{ext['seconds_median']}s cross={cross['status']}", flush=True)
        cases_out.append(entry)

    out_path = ROOT / args.out
    if args.merge and out_path.exists():
        try:
            previous = json.loads(out_path.read_text())
            prev_cases = previous.get("cases", [])
            selected_keys = {f"{c[0]}|{c[1]}|{c[2]}" for c in selected}
            kept = [c for c in prev_cases
                    if f"{c.get('family')}|{c.get('size')}|{c.get('observation')}" not in selected_keys]
            order = {f"{c[0]}|{c[1]}|{c[2]}": i for i, c in enumerate(CASES)}
            merged = kept + cases_out
            merged.sort(key=lambda c: order.get(
                f"{c.get('family')}|{c.get('size')}|{c.get('observation')}", len(order)))
            cases_out = merged
        except Exception:
            pass
    summary = {
        "instances": len(cases_out),
        "native_certificates_verified": sum(
            1 for c in cases_out if c.get("native", {}).get("certificate_verified")),
        "native_policies_verified": sum(
            1 for c in cases_out if c.get("native", {}).get("policy_verified")),
        "native_inconclusive": sum(
            1 for c in cases_out if c.get("native", {}).get("status") == "INCONCLUSIVE"),
        "external_runs": sum(len(c.get("external", [])) for c in cases_out),
        "external_sat_cross_checked": sum(
            1 for c in cases_out for e in c.get("external", [])
            if e["cross_check"]["status"] == "VERIFIED-SAT"),
        "external_unsat_cross_checked": sum(
            1 for c in cases_out for e in c.get("external", [])
            if e["cross_check"]["status"] == "VERIFIED-UNSAT"),
        "external_inconclusive": sum(
            1 for c in cases_out for e in c.get("external", [])
            if e["cross_check"]["status"] == "INCONCLUSIVE"),
        "external_rejected": sum(
            1 for c in cases_out for e in c.get("external", [])
            if e["cross_check"]["status"] == "REJECTED"),
        "status_agreement_with_native": sum(
            1 for c in cases_out for e in c.get("external", [])
            if e["classification"] is not None
            and c.get("native", {}).get("status") is not None
            and e["classification"] == c["native"]["status"].replace("DP-", "").replace("OPTIMUM", "SAT").replace("REFUTATION", "UNSAT")),
    }
    out = {"status": "COMPLETE", "phase": "6 comparative scaling study on mechanics instances",
           "protocol": protocol, "cases": cases_out, "summary": summary}
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
