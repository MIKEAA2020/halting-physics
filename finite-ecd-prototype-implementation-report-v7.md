# Finite ECD prototype implementation report v7

## New in v7

This implements the external-baseline experiment items: fixed-hardware baseline
runs with installed external solvers on identical finite instances, with native
certificate cross-checking, and the corresponding reproduction-gate and
release-manifest updates.

## 1. External solvers installed and recorded

The following solvers were built or installed for the recorded experiment and
are documented in the release manifest:

| Solver | Version / source | Invocation |
|---|---|---|
| minisat | 2.2 series, arminbiere mirror commit 16982a5, gcc 14.2.0 -O3, standard gcc compatibility patch on `SolverTypes.h` | `minisat -mem-lim=3072 -cpu-lim=60 cnf result` |
| kissat | 4.0.4, commit 8af8e56, gcc 14.2.0 -O3 | `kissat --time=60 cnf` |
| z3 | Z3 5.1.0 (pip `z3-solver`) | `z3 -T:60 cnf` (DIMACS input) |
| CP-SAT | OR-Tools 9.15.6755 (pip `ortools`) | isolated process, `num_workers=1`, `random_seed=1`, `max_time_in_seconds=60` |
| HiGHS | HiGHS 1.15.1 (pip `highspy`) | isolated process, `threads=1`, `time_limit=60`, LP-format input |

Recorded hardware: 2-core Intel Xeon virtual machine, 4.1 GiB RAM, Debian 13
(trixie), kernel 5.10.134, glibc 2.41, harness Python 3.12.14.

## 2. Fixed-hardware external baseline sweep

Added:

```text
/home/user/finite_ecd_prototype/external_baseline_sweep.py
/home/user/finite_ecd_prototype/cpsat_runner.py
/home/user/finite_ecd_prototype/highs_runner.py
```

Protocol fixed for the reported experiment:

- timeout: 60 s wall clock per external run;
- address-space cap: 3 GiB applied to every external solver process;
- repetitions: three per solver and instance; median wall-clock reported
  (min/max retained); timings are whole-process and include solver startup;
- instances: identical Boolean explicit-table instances from the
  controlled-width families (path-neq up to n=2048, binary-tree-neq up to 1023
  variables, banded-chain-w2 up to n=2048, grid-neq 2xC up to 512 variables)
  plus an unsatisfiable odd-ring-neq family (n up to 1025) with a supplied
  chordal-style path decomposition of width 2;
- encodings: DIMACS CNF, the minimal CP-SAT forbidden-tuple encoding, and the
  LP-format MILP encoding from `baseline_encode.py`, so every solver sees the
  same finite relation data;
- native side: tree-decomposition DP timed, certificate independently
  re-verified and timed, policy reconstructed from the certificate and
  verified for satisfiable instances;
- cross-checking: every external SAT model is parsed, converted to a policy on
  the original instance, and verified natively; every external UNSAT answer is
  cross-checked against a verified `DP-REFUTATION` certificate.

Invocation for the recorded run:

```bash
PATH="<solvers>/bin:<solvers>/venv/bin:$PATH" \
EXTERNAL_ECD_CPSAT_PYTHON=<solvers>/venv/bin/python \
  python3 external_baseline_sweep.py --out reports/external_baseline_sweep.json
```

Output:

```text
/home/user/finite_ecd_prototype/reports/external_baseline_sweep.json
```

## 3. Recorded results

Summary of the recorded run:

```json
{
  "instances": 24,
  "native_certificates_verified": 24,
  "native_policies_verified": 19,
  "external_runs": 120,
  "external_sat_cross_checked": 95,
  "external_unsat_cross_checked": 25,
  "external_inconclusive": 0,
  "external_rejected": 0,
  "status_agreement_with_native": 120
}
```

All 120 external runs agreed with the native certificates; 95 external SAT
models were verified natively as policies; 25 external UNSAT answers were
cross-checked against verified `DP-REFUTATION` certificates; no run was
inconclusive or rejected. Peak resident set size of any external run was at
most about 101 MiB, far below the 3 GiB cap. At these certificate-study sizes
the compiled SAT solvers finish in milliseconds (startup-dominated), the
CP-SAT process takes roughly 0.35--0.62 s and the HiGHS process roughly
0.11--0.27 s including interpreter startup and model construction, and the
reference Python DP completes in 0.001--0.69 s depending on family and size.
These timings support reproducibility and cross-checking claims only; no
external-solver performance superiority claim is made, and none is supported
by these sizes.

## 4. Reproduction gate updated

- `Makefile` and `reproduce.sh` now include the gated step
  `external-baselines` in `make reproduce`; with no solver available the
  emitted report is `INCONCLUSIVE`.
- `run_external_baselines.py` now runs z3 directly on the DIMACS smoke
  instance (z3 reads DIMACS natively), so all three adapter solvers execute
  when installed; the smoke report status is `COMPLETE_WITH_AVAILABLE_SOLVERS`
  in the recorded environment.
- `README.md` documents the sweep, the environment variables
  (`EXTERNAL_ECD_MINISAT`, `EXTERNAL_ECD_KISSAT`, `EXTERNAL_ECD_Z3`,
  `EXTERNAL_ECD_CPSAT_PYTHON`, `EXTERNAL_ECD_HIGHS_PYTHON`), and the output
  file.

The full gate was re-executed in the recorded environment:

```text
make reproduce   # smoke checks, benchmark sweep, plots, external baseline sweep
```

All native checks report `VERIFIED`; the external baseline sweep reports the
summary above.

## 5. Release manifest frozen

Added:

```text
/home/user/finite_ecd_prototype/RELEASE_MANIFEST.md
```

The manifest records the repository URL
(https://github.com/MIKEAA2020/halting-physics), the release tag
`halting_physics_workspace_v3`, the recorded environment (OS, Python, compiler,
solver versions, hardware), the required reproduction commands, the expected
primary outputs including `reports/external_baseline_sweep.json`, the claim
boundary, and the files to archive. The DOI field remains open until an
archival identifier is assigned at publication time.

## 6. Companion manuscript update

The companion article reports the experiment in a dedicated external-baseline
subsection with the fixed protocol, a results table, and the claim boundary.
The artifact appendix documents the fixed configuration and the sweep command.
Both are versioned as new files; earlier versions are unchanged.
