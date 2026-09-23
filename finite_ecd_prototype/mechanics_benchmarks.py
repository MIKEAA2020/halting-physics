#!/usr/bin/env python3
"""Phase 4 mechanics benchmark suite: generation, certification, measurement.

For every configured case this driver

- declares the structural model (exact rational truss or scalar-chain data);
- generates the certified row batch (base-state solves, exact influence rows,
  finite relation tables) and independently re-verifies it;
- builds the finite ECD instance for the requested observation variant and a
  minimum-fill tree decomposition, validated by the decomposition verifier;
- runs the tree-decomposition dynamic program, re-verifies its certificate,
  and, for satisfiable instances, reconstructs and verifies a policy;
- records stage timings, widths, certificate sizes, peak memory, and relation
  statistics;
- on small representatives, checks that corrupted row-batch and DP
  certificates are rejected;
- on the ten-bar family, cross-validates the mechanics layer against the
  exact affine row generator of ``affine_fe.py`` and runs the brute-force
  sensor-repair demonstrator on the same-observation instance.

Lattice sizes at and beyond three columns are recorded with their measured
influence scopes and decomposition widths only: their relation tables exceed
the pipeline's relation-enumration limit and are marked
``RELATION-TABLE-LIMIT`` rather than silently truncated.

Primary output: ``reports/mechanics_benchmarks.json``.
"""
from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path
from typing import Any, Dict, List

import mechanics_fe
import mechanics_gen
from finite_ecd import (Instance, td_dynamic_program, validate_tree_decomp,
                         verify_dp_certificate, verify_policy, sensor_repair,
                         verify_sensor_repair)
from report_summary import weighted_width

ROOT = Path(__file__).resolve().parent

RELATION_CAP = 1 << 16  # 65536 assignments per relation row


def peak_rss_kib() -> int:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def write_json(path: Path, payload: Dict[str, Any]) -> int:
    path.write_text(json.dumps(payload, indent=2))
    return path.stat().st_size


def run_case(family: str, size: int, observation: str, out_prefix: str,
             relation_cap: int | None = None,
             corruption_test: bool = False) -> Dict[str, Any]:
    model = mechanics_gen.FAMILIES[family](size)
    entry: Dict[str, Any] = {
        "family": family,
        "size": size,
        "observation": observation,
        "model": model["name"],
    }

    t0 = time.perf_counter()
    batch = mechanics_fe.generate(model, relation_cap=relation_cap)
    t1 = time.perf_counter()
    entry["fe_generate_seconds"] = round(t1 - t0, 4)
    entry["fe_verify_seconds"] = None
    entry["fe_verify_status"] = "PENDING"

    t0 = time.perf_counter()
    ok, errors = mechanics_fe.verify(model, batch)
    t1 = time.perf_counter()
    entry["fe_verify_seconds"] = round(t1 - t0, 4)
    entry["fe_verify_status"] = "VERIFIED" if ok else "REJECTED"
    entry["fe_verify_errors"] = errors[:5]

    scopes = batch["scope_sizes"]
    entry["actuators"] = len(model["actuators"])
    entry["rows"] = len(batch["rows"])
    entry["scope_min"] = min(scopes)
    entry["scope_mean"] = round(sum(scopes) / len(scopes), 2)
    entry["scope_max"] = batch["max_scope"]
    limited = sum(1 for r in batch["relations"] if r.get("status") == "RELATION-TABLE-LIMIT")
    entry["relation_limited_rows"] = limited
    entry["relation_cap"] = relation_cap

    prefix = ROOT / out_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    entry["model_file"] = str(prefix.relative_to(ROOT)) + "_model.json"
    entry["row_batch_file"] = str(prefix.relative_to(ROOT)) + "_row_batch.json"
    entry["row_batch_bytes"] = write_json(Path(str(prefix) + "_row_batch.json"), batch)
    write_json(Path(str(prefix) + "_model.json"), model)

    if limited:
        entry["instance_status"] = "RELATION-TABLE-LIMIT"
        entry["decomposition_width"] = batch["max_scope"]
        entry["note"] = ("relation tables exceed the enumeration limit; scopes and "
                         "width recorded from the certified influence rows only")
        return entry

    t0 = time.perf_counter()
    instance = mechanics_gen.build_instance(model, batch, observation)
    t1 = time.perf_counter()
    entry["instance_seconds"] = round(t1 - t0, 4)
    entry["variables"] = len(instance["variables"])
    entry["factors"] = len(instance["factors"])
    rel_sizes = [len(f["relation"]) for f in instance["factors"]]
    entry["relation_min"] = min(rel_sizes)
    entry["relation_mean"] = round(sum(rel_sizes) / len(rel_sizes), 2)
    entry["relation_max"] = max(rel_sizes)
    entry["instance_file"] = str(prefix.relative_to(ROOT)) + "_instance.json"
    entry["instance_bytes"] = write_json(Path(str(prefix) + "_instance.json"), instance)

    t0 = time.perf_counter()
    decomp = mechanics_gen.min_fill_decomp(instance)
    t1 = time.perf_counter()
    entry["decomp_seconds"] = round(t1 - t0, 4)
    inst = Instance.from_json(instance)
    ok_td, err_td = validate_tree_decomp(inst, decomp)
    entry["decomp_verify_status"] = "VERIFIED" if ok_td else "REJECTED"
    entry["decomp_verify_errors"] = err_td[:3]
    widths = [len(xs) - 1 for xs in decomp["bags"].values()]
    entry["decomposition_width"] = max(widths)
    entry["weighted_width"] = weighted_width(inst, decomp)
    entry["bags"] = len(decomp["bags"])
    entry["decomp_file"] = str(prefix.relative_to(ROOT)) + "_tree_decomp.json"
    entry["decomp_bytes"] = write_json(Path(str(prefix) + "_tree_decomp.json"), decomp)

    t0 = time.perf_counter()
    cert = td_dynamic_program(inst, instance, decomp)
    t1 = time.perf_counter()
    entry["dp_seconds"] = round(t1 - t0, 4)
    entry["dp_type"] = cert["type"]
    entry["dp_status"] = cert["status"]
    entry["optimum_cost"] = cert.get("optimum_cost")
    t0 = time.perf_counter()
    ok_dp, err_dp = verify_dp_certificate(inst, instance, cert)
    t1 = time.perf_counter()
    entry["dp_verify_seconds"] = round(t1 - t0, 4)
    entry["dp_verify_status"] = "VERIFIED" if ok_dp else "REJECTED"
    entry["dp_verify_errors"] = err_dp[:3]
    entry["dp_certificate_file"] = str(prefix.relative_to(ROOT)) + "_dp_certificate.json"
    entry["dp_certificate_bytes"] = write_json(Path(str(prefix) + "_dp_certificate.json"), cert)

    if cert["type"] == "DP-OPTIMUM":
        from external_baseline_sweep import reconstruct_policy
        t0 = time.perf_counter()
        policy = reconstruct_policy(cert)
        pok, perr = verify_policy(inst, policy)
        t1 = time.perf_counter()
        entry["policy_seconds"] = round(t1 - t0, 4)
        entry["policy_verify_status"] = "VERIFIED" if pok else "REJECTED"
        entry["policy_errors"] = perr[:3]
        entry["policy_certificate_file"] = str(prefix.relative_to(ROOT)) + "_policy_certificate.json"
        write_json(Path(str(prefix) + "_policy_certificate.json"),
                   {"type": "POLICY", "assignment": policy})

    if corruption_test:
        bad_batch = json.loads(json.dumps(batch))
        bad_batch["rows"][0]["constant"] = "123456789"
        ok_bad, _ = mechanics_fe.verify(model, bad_batch)
        entry["corrupted_row_batch_rejected"] = not ok_bad
        bad_cert = json.loads(json.dumps(cert))
        bag = next(iter(bad_cert["messages"]))
        mutated = False
        for row in bad_cert["messages"][bag]["table"]:
            if row["cost"] is not None:
                row["cost"] = row["cost"] + 99
                mutated = True
                break
        if not mutated:
            # refutation certificates have only null entries: tamper the type
            if bad_cert["type"] == "DP-REFUTATION":
                bad_cert["type"] = "DP-OPTIMUM"
                bad_cert["status"] = "CERTIFIED-OPT"
                bad_cert["optimum_cost"] = 0
                bad_cert["root_assignment"] = None
            else:
                bad_cert["type"] = "DP-REFUTATION"
                bad_cert["status"] = "CERTIFIED-UNSAT"
                bad_cert["optimum_cost"] = None
            mutated = True
        ok_bad_dp, _ = verify_dp_certificate(inst, instance, bad_cert)
        entry["corrupted_dp_certificate_rejected"] = (not ok_bad_dp) and mutated

    entry["peak_rss_kib"] = peak_rss_kib()
    return entry


def ten_bar_extras(model: Dict[str, Any], batch: Dict[str, Any]) -> Dict[str, Any]:
    """Cross-validate against affine_fe.py and run the sensor-repair demo."""
    out: Dict[str, Any] = {}
    affine_model = mechanics_gen.ten_bar_affine_model(model, batch)
    affine_path = ROOT / "examples" / "mech_ten_bar_affine_model.json"
    affine_path.write_text(json.dumps(affine_model, indent=2))
    from affine_fe import generate as affine_generate, verify_batch as affine_verify
    affine_batch = affine_generate(affine_model)
    ok_aff, err_aff = affine_verify(affine_model, affine_batch)
    out["affine_cross_validation_status"] = "VERIFIED" if ok_aff else "REJECTED"
    out["affine_cross_validation_errors"] = err_aff[:3]
    # the derived finite instances must agree
    mech_instance = mechanics_gen.build_instance(model, batch, "same")
    affine_instance = affine_batch["instance"]
    same_factors = [
        {"name": f["name"], "scope": f["scope"], "relation": [[int(v) for v in row] for row in f["relation"]]}
        for f in affine_instance["factors"]
    ]
    mech_factors = [
        {"name": f["name"], "scope": f["scope"], "relation": f["relation"]}
        for f in mech_instance["factors"]
    ]
    out["affine_instance_agrees"] = same_factors == mech_factors
    (ROOT / "examples" / "mech_ten_bar_affine_rows.json").write_text(json.dumps(affine_batch, indent=2))

    sensor_data = mechanics_gen.ten_bar_sensor_data(model, batch)
    sensor_path = ROOT / "examples" / "mech_ten_bar_sensors.json"
    sensor_path.write_text(json.dumps(sensor_data, indent=2))
    actions = sensor_data["actions"]
    scenarios = sensor_data["scenarios"]
    sensors = sensor_data["sensors"]
    cert = sensor_repair(actions, scenarios, sensors)
    (ROOT / "examples" / "mech_ten_bar_sensor_repair_certificate.json").write_text(
        json.dumps(cert, indent=2))
    ok_sr, err_sr = verify_sensor_repair(actions, scenarios, sensors, cert)
    out["sensor_repair_status"] = cert.get("status")
    out["sensor_repair_size"] = cert.get("size")
    out["sensor_repair_selected"] = cert.get("selected")
    out["sensor_repair_verify_status"] = "VERIFIED" if ok_sr else "REJECTED"
    out["sensor_repair_verify_errors"] = err_sr[:3]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/mechanics_benchmarks.json")
    args = ap.parse_args()
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "examples").mkdir(exist_ok=True)

    cases: List[Dict[str, Any]] = []
    # ten-bar: pipeline and quantized-sensor structure
    for obs in ("same", "split"):
        entry = run_case("ten-bar", 1, obs, f"examples/mech_ten_bar_{obs}",
                         corruption_test=True)
        cases.append(entry)
    # chain-pretension: bounded-width scaling
    for n in (8, 64, 256, 1024):
        for obs in ("same", "split"):
            cases.append(run_case("chain-pretension", n, obs,
                                  f"examples/mech_chain{n}_{obs}",
                                  corruption_test=(n == 8)))
    # dense-chain: dense-influence stress test
    for n in (8, 16):
        for obs in ("same", "split"):
            cases.append(run_case("dense-chain", n, obs,
                                  f"examples/mech_dense{n}_{obs}",
                                  corruption_test=(n == 8)))
    # lattice: width-growth boundary
    for C in (1, 2):
        for obs in ("same", "split"):
            cases.append(run_case("lattice", C, obs,
                                  f"examples/mech_latticeC{C}_{obs}",
                                  corruption_test=(C == 1)))
    for C in (3, 4):
        cases.append(run_case("lattice", C, "scope-only",
                              f"examples/mech_latticeC{C}_scope",
                              relation_cap=RELATION_CAP))

    # ten-bar extras (cross-validation and sensor repair)
    tb_model = mechanics_gen.ten_bar_model()
    tb_batch = mechanics_fe.generate(tb_model)
    extras = ten_bar_extras(tb_model, tb_batch)

    solved = [c for c in cases if c.get("instance_status") != "RELATION-TABLE-LIMIT"]
    summary = {
        "cases": len(cases),
        "row_batches_verified": sum(1 for c in cases if c.get("fe_verify_status") == "VERIFIED"),
        "decompositions_verified": sum(1 for c in solved if c.get("decomp_verify_status") == "VERIFIED"),
        "dp_certificates_verified": sum(1 for c in solved if c.get("dp_verify_status") == "VERIFIED"),
        "policies_verified": sum(1 for c in solved if c.get("policy_verify_status") == "VERIFIED"),
        "refutations_certified": sum(1 for c in solved if c.get("dp_type") == "DP-REFUTATION"),
        "relation_table_limit_cases": sum(1 for c in cases if c.get("instance_status") == "RELATION-TABLE-LIMIT"),
        "corrupted_row_batches_rejected": sum(1 for c in cases if c.get("corrupted_row_batch_rejected") is True),
        "corrupted_dp_certificates_rejected": sum(1 for c in cases if c.get("corrupted_dp_certificate_rejected") is True),
        "peak_rss_kib": peak_rss_kib(),
    }
    out = {
        "status": "COMPLETE",
        "phase": "4 mechanics benchmark suite",
        "families": {
            "ten-bar": "10-bar cantilever truss, quantized load scenarios, node-force actuators, member-force monitors",
            "chain-pretension": "grounded mass-spring chain, pre-tension pair per spring, spring-force monitors (bounded width)",
            "dense-chain": "grounded mass-spring chain, node-force actuators, monitored mid-chain displacement (dense influence)",
            "lattice": "cross-braced two-row lattice, pre-tension pairs on verticals and diagonals, member-force monitors (width growth)",
        },
        "observation_variants": {
            "same": "both load scenarios share one command instance; observation-uniform policies must satisfy both scenarios",
            "split": "a separating sensor gives each scenario its own command copy",
        },
        "ten_bar_extras": extras,
        "cases": cases,
        "summary": summary,
    }
    out_path = ROOT / args.out
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
