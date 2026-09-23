# Finite ECD prototype implementation report v2

## New in v2

This extends the previous prototype report with three requested items.

## 1. Sparsification certificate checker

Implemented in:

```text
/home/user/finite_ecd_prototype/affine_fe.py
```

New commands:

```bash
python3 affine_fe.py sparsify MODEL.json RETAINED.json
python3 affine_fe.py verify-sparsify MODEL.json CERTIFICATE.json
```

The checker computes exact rational omitted-term intervals for affine rows

\[
y_i(a)=d_i+\sum_x g_{ix}a_x.
\]

For retained variables \(J_i\), it computes

\[
\underline\eta_i=\sum_{x\notin J_i}\min_{v\in D_x}g_{ix}v,
\qquad
\overline\eta_i=\sum_{x\notin J_i}\max_{v\in D_x}g_{ix}v.
\]

Each retained assignment gets an exact response interval. The inner sparse relation keeps retained assignments whose full interval is safe; the outer sparse relation keeps retained assignments whose interval intersects the safe interval.

Example files:

```text
examples/two_spring_retained_a1.json
examples/two_spring_sparsification_certificate.json
examples/bad_two_spring_sparsification_certificate.json
```

Verified status:

- valid sparsification certificate: `VERIFIED`;
- corrupted sparsification certificate: `REJECTED`.

## 2. Nontrivial path/tree decomposition examples

Added path-decomposition examples with two bags:

```text
examples/path3_sat.json
examples/path3_tree_decomp.json
examples/path3_dp_optimum_certificate.json
examples/path3_unsat.json
examples/path3_unsat_tree_decomp.json
examples/path3_dp_refutation_certificate.json
```

The satisfiable path instance verifies a nontrivial supplied decomposition and emits:

```text
DP-OPTIMUM, CERTIFIED-OPT, optimum_cost = 1
```

The unsatisfiable path instance emits:

```text
DP-REFUTATION, CERTIFIED-UNSAT
```

Both DP certificates verify independently.

## 3. Baseline encoders

Added:

```text
/home/user/finite_ecd_prototype/baseline_encode.py
```

Supported output formats for Boolean explicit-table instances:

- `dimacs` for SAT;
- `milp-lp` for MILP solvers accepting LP format;
- `cpsat-json`, a minimal forbidden-tuple JSON representation for future CP-SAT translation.

Example generated files:

```text
examples/path3_sat.cnf
examples/path3_sat.lp
examples/path3_sat_cpsat.json
```

These are encoders only. No performance comparison is claimed.

## Updated reproducibility gate

`run_repro_checks.py` now also checks:

- sparsification generation and verification;
- corrupted sparsification rejection;
- nontrivial path decomposition verification;
- path DP optimum verification;
- path DP refutation verification;
- SAT/MILP/CP-SAT baseline encoder execution.

The latest `/home/user/finite_ecd_prototype/repro_report.json` records all expected statuses.

## Remaining limits

- The DP implementation is still intended for tiny explicit instances.
- The default decomposition emitter is trivial, although supplied nontrivial decompositions now verify and run.
- Baseline encoders do not invoke external solvers.
- Sparsification is exact affine finite-model certification, not continuum validation.
