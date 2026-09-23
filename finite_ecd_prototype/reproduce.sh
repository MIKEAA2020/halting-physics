#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 run_repro_checks.py
python3 benchmark_sweep.py --out reports/benchmark_sweep.json
python3 plot_reports.py reports/benchmark_sweep.json --outdir reports
# Gated external baseline sweep: runs every solver found on PATH or named by
# EXTERNAL_ECD_MINISAT / EXTERNAL_ECD_KISSAT / EXTERNAL_ECD_Z3 /
# EXTERNAL_ECD_CPSAT_PYTHON / EXTERNAL_ECD_HIGHS_PYTHON. With no solver
# available the report is INCONCLUSIVE.
python3 external_baseline_sweep.py --out reports/external_baseline_sweep.json
python3 mechanics_benchmarks.py --out reports/mechanics_benchmarks.json
python3 sparsification_study.py --out reports/sparsification_study.json
python3 mechanics_baseline_sweep.py --out reports/mechanics_external_baseline_sweep.json
echo "Reproduction complete. See repro_report.json and reports/."
