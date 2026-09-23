# Release manifest

## Repository / DOI

- Repository URL: https://github.com/MIKEAA2020/halting-physics
- DOI / archival identifier: to be assigned before publication
- Release tag: halting_physics_workspace_v4
- Date frozen: 2026-09-22

## Environment

- OS: Debian GNU/Linux 13 (trixie), kernel 5.10.134, glibc 2.41
- Python: 3.12.14 (harness and CP-SAT runner)
- Compiler for source-built solvers: gcc 14.2.0 (-O3)
- External solvers:
  - minisat 2.2 series, arminbiere mirror commit 16982a5, built with the
    standard gcc compatibility patch on `core/SolverTypes.h` (default argument
    removed from the `mkLit` friend declaration; default moved to the inline
    definition)
  - kissat 4.0.4, commit 8af8e56
  - z3 5.1.0 (pip package `z3-solver`)
  - OR-Tools CP-SAT 9.15.6755 (pip package `ortools`)
  - HiGHS MILP 1.15.1 (pip package `highspy`)
- Hardware for the recorded experiments: 2-core Intel Xeon virtual
  machine, 4.1 GiB RAM

## Required reproduction commands

```bash
make reproduce
```

or, with explicit solver locations for the external baseline steps:

```bash
PATH="<solvers>/bin:<solvers>/venv/bin:$PATH" \
EXTERNAL_ECD_Z3=<solvers>/venv/bin/z3 \
EXTERNAL_ECD_CPSAT_PYTHON=<solvers>/venv/bin/python \
EXTERNAL_ECD_HIGHS_PYTHON=<solvers>/venv/bin/python \
  python3 mechanics_baseline_sweep.py \
    --out reports/mechanics_external_baseline_sweep.json
```

The recorded mechanics baseline sweep was executed in five case chunks with
`--only <keys>` and `--merge`, because the recording environment terminates
sessions that run longer than ten minutes; the chunked invocation is
equivalent to a single full invocation and the merged report is the
recorded artifact.

Expected primary outputs:

- `repro_report.json`
- `reports/benchmark_sweep.json`
- `reports/certificate_size_vs_width.svg`
- `reports/verify_time_vs_certificate_size.svg`
- `reports/external_baseline_sweep.json`
- `reports/external_baselines.json` (smoke gate; `COMPLETE_WITH_AVAILABLE_SOLVERS` in the recorded environment)
- `reports/mechanics_benchmarks.json` (phase 4)
- `reports/sparsification_study.json` (phase 5)
- `reports/mechanics_external_baseline_sweep.json` (phase 6)

Recorded protocols: the external baseline protocol of release v3 (60 s
wall-clock timeout, 3 GiB address-space cap, three repetitions per solver
and instance with median reported, single-threaded deterministic
configurations, CP-SAT with `num_workers=1` and `random_seed=1`, identical
instances encoded by `baseline_encode.py`, external SAT models verified
natively as policies, external UNSAT answers cross-checked against verified
`DP-REFUTATION` certificates) applies unchanged to the mechanics
comparative study; the native pipeline runs as an isolated process under
the same timeout and address-space cap and emits and re-verifies its
certificate. FE preprocessing (model generation, certified relation
generation, and independent verification) is recorded separately in the
phase 4 report and excluded from both native and external timings.

## Claim boundary

This release certifies finite explicit-table examples, exact finite affine
algebraic models, and declared exact rational structural models (pin-jointed
trusses with rational directions and grounded mass-spring chains). The
attached reports support reproducibility, cross-checking, and
status-agreement claims on the recorded instance families and sizes, and
the sparsification ladder soundness and monotonicity claims. They do not
support a claim of practical superiority over the external solvers: at the
recorded sizes the compiled SAT solvers complete in milliseconds on the
width-bounded families; on the dense-influence family at n=16 two external
solvers exceeded the fixed limit while two others and the native pipeline
answered within it, a per-instance observation on one family. The
sparsification study records that the calibrated families certify only at
or near the full retained radius; no practical width-reduction benefit is
claimed. Continuum-mechanics validation is outside the certified scope.

## Files to archive

- source scripts: `*.py`, `Makefile`, `reproduce.sh`
- examples: `examples/*.json`, `examples/*.cnf`, generated baseline
  encodings, with two documented exclusions: the dense-chain n=16 baseline
  encodings (`mech_dense16_*.cnf`, `.lp`, `_cpsat.json`, regenerable in
  seconds by `baseline_encode.py` from the archived instances) and the
  duplicate native DP certificates (byte-identical to the archived phase 4
  certificates; the study report references the phase 4 files)
- reports: `repro_report.json`, `reports/*.json`, `reports/*.svg`
- documentation: `README.md`, `ARTIFACT_MANIFEST.md`, `ARTIFACT_APPENDIX.md`,
  this release manifest
