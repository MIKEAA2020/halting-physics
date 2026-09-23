# Finite ECD prototype implementation report v5

## New in v5

This implements the latest four requested artifact items.

## 1. Optional installed-solver adapters

Added:

```text
/home/user/finite_ecd_prototype/solver_adapters.py
```

The adapter detects and optionally runs specific solvers only when available:

- `minisat` for DIMACS CNF;
- `kissat` for DIMACS CNF;
- `z3` for SMT-LIB2.

Detection command:

```bash
python3 solver_adapters.py available
```

In the current environment the recorded availability is:

```json
{"minisat": false, "kissat": false, "z3": false}
```

Missing solvers are reported as `INCONCLUSIVE`; this is not treated as a benchmark result.

## 2. Certificate-size and verification-time plots

Added:

```text
/home/user/finite_ecd_prototype/plot_reports.py
```

It reads benchmark report JSON and emits SVG plots. Generated files:

```text
/home/user/finite_ecd_prototype/reports/certificate_size_vs_width.svg
/home/user/finite_ecd_prototype/reports/verify_time_vs_certificate_size.svg
```

The plots are simple dependency-free SVG files so they can be viewed without Python plotting libraries.

## 3. Scripted controlled-width benchmark sweeps

Added:

```text
/home/user/finite_ecd_prototype/benchmark_sweep.py
```

It currently sweeps:

- paths of sizes 4, 6, 8;
- banded chains of sizes 6, 8, 10 at width 2;
- 2-by-3, 2-by-4, and 2-by-5 grids using supplied column-pair decompositions.

Generated report:

```text
/home/user/finite_ecd_prototype/reports/benchmark_sweep.json
```

The sweep completed 9 cases and generated per-case summaries.

## 4. Artifact manifest and reproducibility instructions

Added:

```text
/home/user/finite_ecd_prototype/ARTIFACT_MANIFEST.md
```

It records:

- artifact scope;
- main scripts;
- reproduction commands;
- status discipline;
- deposit checklist.

Important reproduction commands:

```bash
python3 run_repro_checks.py
python3 benchmark_sweep.py --out reports/benchmark_sweep.json
python3 plot_reports.py reports/benchmark_sweep.json --outdir reports
```

## Current status

The artifact now has:

- native certificate generation and verification;
- exact affine FE-row and sparsification certificates;
- controlled-width benchmark generation;
- baseline encoders;
- optional external solver wrappers;
- solver-output cross-checks against native certificates;
- report summaries;
- SVG plots;
- reproducibility manifest.

No external baseline performance claim is made, because no external solver was available in the current environment and no fixed-hardware experiment has been run.
