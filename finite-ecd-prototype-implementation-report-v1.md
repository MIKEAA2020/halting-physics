# Finite ECD prototype implementation report v1

## Implemented

The prototype at `/home/user/finite_ecd_prototype/` has been extended with two new certificate layers.

### 1. Tree-decomposition dynamic-programming certificates

Implemented in `finite_ecd.py`:

- `tree-decomp`: emits a trivial one-bag `TREE-DECOMP` certificate;
- `verify-tree-decomp`: checks bag variables, tree connectivity, factor containment, and running-intersection property;
- `td-solve`: computes a tree-decomposition DP over explicit finite tables and emits either:
  - `DP-OPTIMUM`, or
  - `DP-REFUTATION`;
- `verify-dp`: independently recomputes and checks all message tables and the root optimum/refutation.

The DP supports optional variable-value costs via `value_costs` and certifies minimum cost when the instance is satisfiable.

### 2. Exact affine FE-row certificates

Implemented in `affine_fe.py`:

- exact rational affine response evaluation;
- `FE-ROW` generation;
- `FE-ROW-BATCH` generation;
- verifier for individual rows and batches;
- derived finite ECD instance generation from safe rows.

The example model is the exact two-spring system:

\[
u(f,a_1,a_2)=\frac{f-a_1-a_2}{2},
\qquad |u|\le 0.25.
\]

It generates the expected safe relations:

\[
R_1=\{(0,1),(1,0)\},
\qquad
R_2=\{(1,1)\}.
\]

## New example files

- `examples/tiny_cost_sat.json`
- `examples/tiny_cost_tree_decomp.json`
- `examples/tiny_cost_dp_certificate.json`
- `examples/bad_tiny_cost_dp_certificate.json`
- `examples/two_spring_affine_model.json`
- `examples/two_spring_fe_rows.json`
- `examples/two_spring_fe_instance.json`
- `examples/bad_two_spring_fe_rows.json`
- `examples/two_spring_dp_refutation_certificate.json`

## Reproducibility gate

`run_repro_checks.py` now checks:

- exact two-spring generation;
- same-observation unsat;
- split-observation sat;
- fibre conflict verification;
- corrupted fibre certificate rejection;
- sensor repair optimality and verification;
- corrupted sensor repair rejection;
- tree-decomposition verification;
- DP optimum generation and verification;
- DP refutation generation and verification;
- corrupted DP certificate rejection;
- affine FE-row generation and verification;
- corrupted FE-row rejection.

The latest `repro_report.json` records all expected statuses.

## Current scope limitations

This remains a correctness harness, not a performance solver. The tree decomposition emitted by default is trivial. No SAT/CP-SAT/MILP baseline comparison is implemented. The FE-row generator certifies an exact finite affine algebraic model only; it does not certify continuum discretization error.
