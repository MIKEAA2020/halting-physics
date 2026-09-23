# Finite ECD prototype implementation report v3

## New in v3

This implements the next four requested items.

## 1. Benchmark family generator with known width

Added:

```text
/home/user/finite_ecd_prototype/benchmark_gen.py
```

Supported families:

- `path n`: Boolean disequality path, known treewidth/pathwidth 1;
- `binary-tree depth`: Boolean disequality binary tree, known treewidth 1.

Example generated files:

```text
examples/generated_path6_instance.json
examples/generated_path6_tree_decomp.json
examples/generated_path6_dp_certificate.json
examples/generated_btree_depth2_instance.json
examples/generated_btree_depth2_tree_decomp.json
examples/generated_btree_depth2_dp_certificate.json
```

Both generated decompositions verify, and their DP certificates verify.

## 2. Sparsification ladder monotonicity checker

Extended:

```text
/home/user/finite_ecd_prototype/affine_fe.py
```

New command:

```bash
python3 affine_fe.py verify-sparsify-ladder MODEL.json COARSE_CERT.json FINE_CERT.json
```

The checker verifies the rowwise finite consequences of \(J\subseteq J'\):

- each coarse retained set is contained in the corresponding fine retained set;
- every coarse inner tuple has all fine extensions in the fine inner relation;
- every fine outer tuple projects into the coarse outer relation.

Example files:

```text
examples/two_spring_sparsification_certificate.json
examples/two_spring_sparsification_fine_certificate.json
```

Verified status:

```text
VERIFIED
```

## 3. Optional external-solver adapter

Added:

```text
/home/user/finite_ecd_prototype/external_solver_adapter.py
```

The adapter runs a declared external command with a timeout and classifies results conservatively. Missing executables, timeouts, and unrecognised output are all reported as:

```text
INCONCLUSIVE
```

Example file:

```text
examples/external_missing_solver_result.json
```

The missing-solver test correctly reports `INCONCLUSIVE`. This preserves the rule that a timeout or failed external run is not evidence of infeasibility.

## 4. Larger exact affine frame example

Added:

```text
examples/four_actuator_frame_affine_model.json
examples/four_actuator_frame_fe_rows.json
examples/four_actuator_frame_fe_instance.json
examples/four_actuator_frame_dp_certificate.json
```

This is a four-actuator, three-row exact affine finite algebraic model. It is a larger finite-model demonstration than the two-spring example. The FE-row batch verifies, the derived finite instance is generated, and the DP optimum certificate verifies.

No continuum mechanics validity is claimed; this remains exact finite algebraic certification.

## Updated reproducibility gate

`run_repro_checks.py` now additionally checks:

- generated path benchmark decomposition and DP certificate;
- generated binary-tree benchmark decomposition and DP certificate;
- sparsification ladder verification;
- external missing-solver adapter result `INCONCLUSIVE`;
- four-actuator affine frame FE-row and DP certificates.

The latest `repro_report.json` records all expected statuses.

## Remaining limits

- The benchmark library is intentionally small.
- External solver adapter does not prove solver correctness; it only standardizes process status handling.
- Baseline encoders are present, but no performance comparison is claimed.
- Larger mechanics examples are exact finite algebraic examples, not continuum validation.
