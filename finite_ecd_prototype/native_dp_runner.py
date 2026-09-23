#!/usr/bin/env python3
"""Isolated native DP runner for the mechanics comparative scaling study.

Runs the tree-decomposition dynamic program on an explicit-table instance
with a supplied decomposition, re-verifies the certificate, and, for
satisfiable instances, reconstructs and verifies a policy. Executed as an
isolated process so that wall-clock timing and memory accounting cover the
whole native pipeline and nothing else, under the same limits the external
solvers face.

Output is a JSON object with fields:
- status: DP-OPTIMUM / DP-REFUTATION / DP-ERROR;
- certificate_verified, policy_verified;
- dp_seconds, verify_seconds, policy_seconds, wall_seconds;
- certificate_bytes, peak_rss_kib.
"""
from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from finite_ecd import (Instance, load_json, td_dynamic_program,
                         verify_dp_certificate, verify_policy)
from external_baseline_sweep import reconstruct_policy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instance")
    ap.add_argument("--decomp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    t_wall0 = time.perf_counter()
    raw = load_json(args.instance)
    inst = Instance.from_json(raw)
    decomp = load_json(args.decomp)
    if "tree_decomp" in decomp:
        decomp = decomp["tree_decomp"]

    t0 = time.perf_counter()
    cert = td_dynamic_program(inst, raw, decomp)
    t1 = time.perf_counter()
    ok, errors = verify_dp_certificate(inst, raw, cert)
    t2 = time.perf_counter()

    payload = {
        "status": cert.get("type", "DP-ERROR"),
        "dp_status": cert.get("status"),
        "certificate_verified": bool(ok),
        "certificate_errors": errors[:5],
        "optimum_cost": cert.get("optimum_cost"),
        "dp_seconds": round(t1 - t0, 6),
        "verify_seconds": round(t2 - t1, 6),
    }
    if cert.get("type") == "DP-OPTIMUM":
        t3 = time.perf_counter()
        policy = reconstruct_policy(cert)
        pok, perr = verify_policy(inst, policy)
        t4 = time.perf_counter()
        payload["policy_verified"] = bool(pok)
        payload["policy_errors"] = perr[:5]
        payload["policy_seconds"] = round(t4 - t3, 6)
    cert_text = json.dumps(cert, indent=2)
    Path(args.out).write_text(cert_text)
    payload["certificate_bytes"] = len(cert_text.encode())
    payload["wall_seconds"] = round(time.perf_counter() - t_wall0, 6)
    payload["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
