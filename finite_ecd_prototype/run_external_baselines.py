#!/usr/bin/env python3
"""Gated external baseline runner.

This script records solver availability and runs no performance experiment unless
at least one supported solver is installed. Timeouts or unavailable solvers are
reported as INCONCLUSIVE.
"""
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable

def jrun(args):
    p = subprocess.run([PY, *args], cwd=ROOT, text=True, capture_output=True)
    try: return json.loads(p.stdout)
    except Exception: return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}

available = jrun(["solver_adapters.py", "available"])
results = {"availability": available, "runs": [], "status": "INCONCLUSIVE"}
# Run only if available; keep tiny path3 CNF as smoke baseline, not performance claim.
if available.get("minisat"):
    results["runs"].append(jrun(["solver_adapters.py", "minisat", "examples/path3_sat.cnf", "--timeout", "10"]))
if available.get("kissat"):
    results["runs"].append(jrun(["solver_adapters.py", "kissat", "examples/path3_sat.cnf", "--timeout", "10"]))
if available.get("z3"):
    # z3 reads DIMACS CNF directly; no SMT2 encoder is required.
    t0 = time.perf_counter()
    p = subprocess.run(["z3", "-T:10", "examples/path3_sat.cnf"], cwd=ROOT,
                       text=True, capture_output=True)
    elapsed = time.perf_counter() - t0
    text = p.stdout.upper()
    if "UNSATISFIABLE" in text:
        st = "CERTIFIED-UNSAT-EXTERNAL"
    elif "SATISFIABLE" in text:
        st = "CERTIFIED-SAT-EXTERNAL"
    else:
        st = "INCONCLUSIVE"
    results["runs"].append({"solver": "z3", "status": st,
                            "elapsed_seconds": elapsed,
                            "returncode": p.returncode})
if results["runs"]:
    results["status"] = "COMPLETE_WITH_AVAILABLE_SOLVERS"
else:
    results["reason"] = "no supported external solver installed"
out = ROOT / "reports" / "external_baselines.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
