#!/usr/bin/env python3
"""Run controlled-width benchmark sweeps and emit JSON reports."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run_json(cmd):
    p = subprocess.run([PY, *cmd], cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def run_one(family, size, prefix, width=None, cols=None):
    gen_cmd = ["benchmark_gen.py", family, str(size), prefix]
    if width is not None: gen_cmd += ["--width", str(width)]
    if cols is not None: gen_cmd += ["--cols", str(cols)]
    gen = run_json(gen_cmd)
    inst = f"{prefix}_instance.json"; dec = f"{prefix}_tree_decomp.json"; cert = f"{prefix}_dp_certificate.json"; summ = f"{prefix}_summary.json"
    dp = subprocess.run([PY, "finite_ecd.py", "td-solve", inst, "--decomp", dec], cwd=ROOT, text=True, capture_output=True)
    Path(ROOT / cert).write_text(dp.stdout)
    summary = run_json(["report_summary.py", inst, "--decomp", dec, "--certificate", cert])
    Path(ROOT / summ).write_text(json.dumps(summary, indent=2))
    return {"family": family, "size": size, "prefix": prefix, "generator": gen, "dp_returncode": dp.returncode, "summary": summary}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/benchmark_sweep.json")
    args = ap.parse_args()
    (ROOT / "reports").mkdir(exist_ok=True)
    cases = []
    for n in [4, 6, 8]: cases.append(run_one("path", n, f"examples/sweep_path{n}"))
    for n in [6, 8, 10]: cases.append(run_one("band", n, f"examples/sweep_band{n}_w2", width=2))
    for cols in [3, 4, 5]: cases.append(run_one("grid", 2, f"examples/sweep_grid2x{cols}", cols=cols))
    out = {"status": "COMPLETE", "cases": cases}
    Path(ROOT / args.out).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
