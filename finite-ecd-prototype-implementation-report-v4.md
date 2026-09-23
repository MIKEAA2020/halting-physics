# Finite ECD prototype implementation report v4

## New in v4

This implements the next four requested items after report v3.

## 1. External solver cross-checks without trusting logs

Added:

```text
/home/user/finite_ecd_prototype/cross_check_external.py
```

The cross-checker reads an external solver result and verifies a native ECD certificate:

- external SAT requires a verified policy certificate;
- external UNSAT requires a verified `DP-REFUTATION` certificate;
- missing certificates, timeouts, missing executables, or unrecognised solver output remain `INCONCLUSIVE`.

Example files:

```text
examples/fake_external_sat.json
examples/fake_external_unsat.json
examples/path3_policy_certificate.json
examples/cross_checked_external_sat.json
examples/cross_checked_external_unsat.json
examples/cross_checked_external_sat_no_cert.json
```

Verified statuses:

- external SAT + policy certificate: `VERIFIED-SAT`;
- external UNSAT + DP refutation: `VERIFIED-UNSAT`;
- external SAT without policy certificate: `INCONCLUSIVE`.

## 2. More controlled-width benchmark families

Extended:

```text
/home/user/finite_ecd_prototype/benchmark_gen.py
```

New families:

- `band n --width k`: banded chain with supplied decomposition width `k`;
- `grid rows --cols cols`: grid disequality instance with supplied column-pair path decomposition of width `2*rows-1`.

Example generated files:

```text
examples/generated_band7_w2_instance.json
examples/generated_band7_w2_tree_decomp.json
examples/generated_band7_w2_dp_certificate.json
examples/generated_grid2x4_instance.json
examples/generated_grid2x4_tree_decomp.json
examples/generated_grid2x4_dp_certificate.json
```

All supplied decompositions and DP certificates verify.

## 3. Report generator

Added:

```text
/home/user/finite_ecd_prototype/report_summary.py
```

It summarizes:

- number of variables;
- total domain values;
- number of factors;
- total factor rows;
- instance byte size;
- number of bags;
- ordinary width;
- weighted width;
- decomposition byte size;
- certificate type and byte size;
- certificate verification status;
- verification time;
- optimum cost when present.

Example output:

```text
examples/generated_grid2x4_summary.json
```

## 4. Baseline experiments remain gated

The prototype now has baseline encoders, an external-solver adapter, and a cross-checker. It still does not claim external-solver performance results. Fair baseline experiments should be run only on fixed hardware with fixed encodings and with solver outputs cross-checked against native ECD certificates where possible.

## Updated reproducibility gate

`run_repro_checks.py` now also checks:

- SAT/UNSAT external-result cross-checks;
- external SAT without a certificate is `INCONCLUSIVE`;
- banded-chain benchmark generation and DP verification;
- grid benchmark generation and DP verification;
- summary-report generation.

The latest `repro_report.json` records all expected statuses.
