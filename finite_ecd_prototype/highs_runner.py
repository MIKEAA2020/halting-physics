#!/usr/bin/env python3
"""HiGHS MILP baseline runner for the LP-format forbidden-tuple encoding.

Reads an LP model produced by ``baseline_encode.py --format milp-lp`` (or an
equivalent file), solves it under fixed options (single thread, fixed time
limit, output suppressed), and reports the outcome as an isolated process.

Output is a JSON object with fields:
- status: CERTIFIED-SAT-EXTERNAL / CERTIFIED-UNSAT-EXTERNAL / INCONCLUSIVE;
- model: variable-name -> value map when a feasible solution exists, else null;
- build_seconds, solve_seconds, wall_seconds;
- peak_rss_kib: peak resident set size of this process.
"""
from __future__ import annotations
import argparse, json, resource, time
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lp_file", help="LP-format encoding of the finite instance")
    ap.add_argument("--time-limit", type=float, default=60.0)
    args = ap.parse_args()

    t0 = time.perf_counter()
    import highspy

    highs = highspy.Highs()
    highs.setOptionValue("output_flag", False)
    highs.setOptionValue("time_limit", args.time_limit)
    highs.setOptionValue("threads", 1)
    read_status = highs.readModel(args.lp_file)
    t1 = time.perf_counter()

    if str(read_status) != "HighsStatus.kOk":
        out = {
            "solver": "highs",
            "status": "INCONCLUSIVE",
            "reason": f"LP parse failed: {read_status}",
            "wall_seconds": t1 - t0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        }
        print(json.dumps(out))
        return

    highs.run()
    t2 = time.perf_counter()

    ms = highs.getModelStatus()
    name = highs.modelStatusToString(ms) if hasattr(highs, "modelStatusToString") else str(ms)
    if "Infeasible" in name:
        status = "CERTIFIED-UNSAT-EXTERNAL"
        model = None
    elif name in ("Optimal", "Feasible"):
        status = "CERTIFIED-SAT-EXTERNAL"
        sol = highs.getSolution()
        col_names = list(highs.getLp().col_names_)
        model = {n: int(round(v)) for n, v in zip(col_names, sol.col_value)}
    else:
        status = "INCONCLUSIVE"
        model = None

    out = {
        "solver": "highs",
        "status": status,
        "highs_model_status": name,
        "model": model,
        "build_seconds": t1 - t0,
        "solve_seconds": t2 - t1,
        "wall_seconds": t2 - t0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
