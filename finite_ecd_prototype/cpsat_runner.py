#!/usr/bin/env python3
"""CP-SAT baseline runner for the minimal forbidden-tuple JSON encoding.

Reads an encoding produced by ``baseline_encode.py --format cpsat-json`` (or an
equivalent file), builds the identical finite instance as a CP-SAT model with
one BoolOr constraint per forbidden tuple, and solves it under fixed parameters:
single worker, fixed random seed, fixed time limit. The run is executed as an
isolated process so that wall-clock timing includes model construction, solver
startup, and solving, and nothing else.

Output is a JSON object with fields:
- status: CERTIFIED-SAT-EXTERNAL / CERTIFIED-UNSAT-EXTERNAL / INCONCLUSIVE;
- model: variable -> value map when satisfiable, else null;
- build_seconds, solve_seconds, wall_seconds;
- peak_rss_kib: peak resident set size of this process.
"""
from __future__ import annotations
import argparse, json, resource, time
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("encoding", help="cpsat-json encoding of the finite instance")
    ap.add_argument("--time-limit", type=float, default=60.0)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    data = json.loads(Path(args.encoding).read_text())
    t0 = time.perf_counter()
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    variables = {}
    for v in data["variables"]:
        variables[v["name"]] = model.NewBoolVar(v["name"])
    for forbidden in data["forbidden_assignments"]:
        lits = []
        for name, value in zip(forbidden["scope"], forbidden["tuple"]):
            # forbidden tuple excluded: at least one variable differs
            lits.append(variables[name] if value == 0 else ~variables[name])
        model.AddBoolOr(lits)
    t1 = time.perf_counter()

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = args.seed
    result = solver.Solve(model)
    t2 = time.perf_counter()

    status_name = solver.StatusName(result)
    if status_name in ("OPTIMAL", "FEASIBLE"):
        status = "CERTIFIED-SAT-EXTERNAL"
        assignment = {
            name: int(solver.Value(var)) for name, var in variables.items()
        }
    elif status_name == "INFEASIBLE":
        status = "CERTIFIED-UNSAT-EXTERNAL"
        assignment = None
    else:
        status = "INCONCLUSIVE"
        assignment = None

    out = {
        "solver": "cpsat",
        "status": status,
        "cpsat_status": status_name,
        "model": assignment,
        "build_seconds": t1 - t0,
        "solve_seconds": t2 - t1,
        "wall_seconds": t2 - t0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
