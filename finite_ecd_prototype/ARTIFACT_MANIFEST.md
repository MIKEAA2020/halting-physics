# Finite ECD prototype artifact manifest

## Scope

This artifact is a correctness and certificate harness for finite Effective Causal Descent examples. It is not a performance claim and not a continuum-mechanics validator.

## Main scripts

- `finite_ecd.py`: explicit-table instances, policy checks, fibre certificates, sensor repair, tree-decomposition DP certificates.
- `affine_fe.py`: exact rational affine FE-row and sparsification certificates.
- `benchmark_gen.py`: controlled-width benchmark generation.
- `baseline_encode.py`: SAT/MILP/CP-SAT encoders for Boolean explicit-table instances.
- `external_solver_adapter.py`: conservative optional external-solver wrapper.
- `cross_check_external.py`: cross-check external results against native ECD certificates.
- `report_summary.py`: instance/decomposition/certificate summaries.
- `benchmark_sweep.py`: scripted controlled-width sweeps.
- `plot_reports.py`: simple SVG plots from summary JSON files.
- `run_repro_checks.py`: full reproducibility gate.

## Reproduction

From this directory run:

```bash
python3 run_repro_checks.py
python3 benchmark_sweep.py --out reports/benchmark_sweep.json
python3 plot_reports.py reports/benchmark_sweep.json --outdir reports
```

Expected result: JSON reports with verified native certificates and SVG plots under `reports/`.

## Status discipline

- `VERIFIED`, `CERTIFIED-SAT`, `CERTIFIED-UNSAT`, and `CERTIFIED-OPT` require native certificate checks.
- External solver output is cross-checked against native certificates where possible.
- Missing solvers, timeouts, and unrecognised output are `INCONCLUSIVE`.

## Deposit checklist

Before repository deposit, include Python version, OS, commit hash, and the generated `repro_report.json` and `reports/benchmark_sweep.json` files. Do not claim external baseline performance unless fixed hardware, solver versions, and time limits are recorded.
