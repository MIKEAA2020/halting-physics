#!/usr/bin/env python3
"""Optional external-solver adapter with INCONCLUSIVE timeout discipline.

This wrapper is intentionally generic. It runs a declared command on an encoded
instance and records SAT/UNSAT/UNKNOWN only when the solver output contains a
recognised token. Timeouts, missing executables, and unrecognised output are
reported as INCONCLUSIVE.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, time
from pathlib import Path

SAT_TOKENS = ["SATISFIABLE", "s SATISFIABLE", "OPTIMAL", "FEASIBLE"]
UNSAT_TOKENS = ["UNSATISFIABLE", "s UNSATISFIABLE", "INFEASIBLE"]
UNKNOWN_TOKENS = ["UNKNOWN", "INCONCLUSIVE"]


def classify(text: str) -> str:
    up = text.upper()
    # Check UNSAT before SAT because UNSATISFIABLE contains SATISFIABLE.
    if any(tok in up for tok in UNSAT_TOKENS):
        return "CERTIFIED-UNSAT-EXTERNAL"
    if any(tok in up for tok in SAT_TOKENS):
        return "CERTIFIED-SAT-EXTERNAL"
    if any(tok in up for tok in UNKNOWN_TOKENS):
        return "INCONCLUSIVE"
    return "INCONCLUSIVE"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--output", default=None)
    ap.add_argument("cmd", nargs=argparse.REMAINDER, help="command after --, e.g. -- minisat file.cnf")
    args=ap.parse_args()
    cmd=args.cmd
    if cmd and cmd[0] == "--":
        cmd=cmd[1:]
    if not cmd:
        result={"solver": args.name, "status": "INCONCLUSIVE", "reason": "no command supplied"}
    elif shutil.which(cmd[0]) is None:
        result={"solver": args.name, "status": "INCONCLUSIVE", "reason": f"executable {cmd[0]!r} not found", "command": cmd}
    else:
        start=time.time()
        try:
            proc=subprocess.run(cmd, text=True, capture_output=True, timeout=args.timeout)
            elapsed=time.time()-start
            text=(proc.stdout or "") + "\n" + (proc.stderr or "")
            result={
                "solver": args.name,
                "status": classify(text),
                "returncode": proc.returncode,
                "elapsed_seconds": elapsed,
                "command": cmd,
                "stdout_tail": (proc.stdout or "")[-2000:],
                "stderr_tail": (proc.stderr or "")[-2000:],
            }
        except subprocess.TimeoutExpired as e:
            result={"solver": args.name, "status": "INCONCLUSIVE", "reason": "timeout", "timeout_seconds": args.timeout, "command": cmd, "stdout_tail": (e.stdout or "")[-2000:] if isinstance(e.stdout, str) else "", "stderr_tail": (e.stderr or "")[-2000:] if isinstance(e.stderr, str) else ""}
    payload=json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(payload+"\n")
    print(payload)

if __name__=="__main__": main()
