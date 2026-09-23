#!/usr/bin/env python3
"""Optional adapters for installed external solvers.

Adapters are enabled only when their executables/modules are available. Missing
solvers are reported as INCONCLUSIVE, never as failures of an instance.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd, timeout):
    t0 = time.perf_counter()
    try:
        p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr, time.perf_counter() - t0, None
    except subprocess.TimeoutExpired as e:
        return None, e.stdout if isinstance(e.stdout, str) else "", e.stderr if isinstance(e.stderr, str) else "", time.perf_counter() - t0, "timeout"


def classify_sat_output(stdout, stderr):
    text = (stdout + "\n" + stderr).upper()
    if "UNSAT" in text:
        return "CERTIFIED-UNSAT-EXTERNAL"
    if "SATISFIABLE" in text or " SAT" in text or text.strip() == "SAT":
        return "CERTIFIED-SAT-EXTERNAL"
    return "INCONCLUSIVE"


def adapter_minisat(cnf, timeout):
    exe = shutil.which("minisat")
    if not exe:
        return {"solver": "minisat", "available": False, "status": "INCONCLUSIVE", "reason": "minisat executable not found"}
    rc, out, err, elapsed, reason = run([exe, cnf], timeout)
    if reason:
        return {"solver": "minisat", "available": True, "status": "INCONCLUSIVE", "reason": reason, "elapsed_seconds": elapsed}
    return {"solver": "minisat", "available": True, "status": classify_sat_output(out, err), "returncode": rc, "elapsed_seconds": elapsed, "stdout_tail": out[-1000:], "stderr_tail": err[-1000:]}


def adapter_kissat(cnf, timeout):
    exe = shutil.which("kissat")
    if not exe:
        return {"solver": "kissat", "available": False, "status": "INCONCLUSIVE", "reason": "kissat executable not found"}
    rc, out, err, elapsed, reason = run([exe, cnf], timeout)
    if reason:
        return {"solver": "kissat", "available": True, "status": "INCONCLUSIVE", "reason": reason, "elapsed_seconds": elapsed}
    return {"solver": "kissat", "available": True, "status": classify_sat_output(out, err), "returncode": rc, "elapsed_seconds": elapsed, "stdout_tail": out[-1000:], "stderr_tail": err[-1000:]}


def adapter_z3_smt2(smt2, timeout):
    exe = shutil.which("z3")
    if not exe:
        return {"solver": "z3", "available": False, "status": "INCONCLUSIVE", "reason": "z3 executable not found"}
    rc, out, err, elapsed, reason = run([exe, "-smt2", smt2], timeout)
    if reason:
        return {"solver": "z3", "available": True, "status": "INCONCLUSIVE", "reason": reason, "elapsed_seconds": elapsed}
    first = out.strip().splitlines()[0].lower() if out.strip() else ""
    status = "CERTIFIED-SAT-EXTERNAL" if first == "sat" else "CERTIFIED-UNSAT-EXTERNAL" if first == "unsat" else "INCONCLUSIVE"
    return {"solver": "z3", "available": True, "status": status, "returncode": rc, "elapsed_seconds": elapsed, "stdout_tail": out[-1000:], "stderr_tail": err[-1000:]}


def available():
    return {
        "minisat": shutil.which("minisat") is not None,
        "kissat": shutil.which("kissat") is not None,
        "z3": shutil.which("z3") is not None,
    }


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("available")
    m = sub.add_parser("minisat"); m.add_argument("cnf"); m.add_argument("--timeout", type=float, default=10)
    k = sub.add_parser("kissat"); k.add_argument("cnf"); k.add_argument("--timeout", type=float, default=10)
    z = sub.add_parser("z3"); z.add_argument("smt2"); z.add_argument("--timeout", type=float, default=10)
    args = ap.parse_args()
    if args.cmd == "available": res = available()
    elif args.cmd == "minisat": res = adapter_minisat(args.cnf, args.timeout)
    elif args.cmd == "kissat": res = adapter_kissat(args.cnf, args.timeout)
    else: res = adapter_z3_smt2(args.smt2, args.timeout)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
