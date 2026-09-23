# finite_ecd_prototype

Dependency-free prototype for the first companion-monograph certificate layer.

Implemented now:

- explicit finite-table instance loading;
- well-formedness checks;
- policy verification;
- brute-force solving for small instances;
- one-shot fibre conflict certificate generation and verification.

This is not a performance solver. It is a correctness harness for the certificate grammar.

Example commands:

```bash
python3 finite_ecd.py solve examples/two_spring_same_observation.json
python3 finite_ecd.py solve examples/two_spring_split_observation.json
python3 finite_ecd.py fibre-conflict examples/two_spring_fibres.json same
```

Additional checked commands:

```bash
python3 two_spring_generator.py
python3 finite_ecd.py solve examples/generated_two_spring_same.json
python3 finite_ecd.py solve examples/generated_two_spring_split.json
python3 finite_ecd.py sensor-repair examples/two_spring_sensors.json
python3 finite_ecd.py verify-sensor-repair examples/two_spring_sensors.json examples/two_spring_sensor_repair_certificate.json
```

The sensor repair command brute-force enumerates tiny candidate sensor subsets and returns a certificate of optimum size for the two-spring demonstrator.

## Tree-decomposition DP certificates

The prototype now emits and verifies tiny tree-decomposition dynamic-programming certificates:

```bash
python3 finite_ecd.py tree-decomp examples/tiny_cost_sat.json > examples/tiny_cost_tree_decomp.json
python3 finite_ecd.py verify-tree-decomp examples/tiny_cost_sat.json examples/tiny_cost_tree_decomp.json
python3 finite_ecd.py td-solve examples/tiny_cost_sat.json --decomp examples/tiny_cost_tree_decomp.json > examples/tiny_cost_dp_certificate.json
python3 finite_ecd.py verify-dp examples/tiny_cost_sat.json examples/tiny_cost_dp_certificate.json
python3 finite_ecd.py td-solve examples/two_spring_fe_instance.json > examples/two_spring_dp_refutation_certificate.json
python3 finite_ecd.py verify-dp examples/two_spring_fe_instance.json examples/two_spring_dp_refutation_certificate.json
```

Certificate types currently supported:

- `TREE-DECOMP`: bags, edges, root, and factor-to-bag map;
- `DP-OPTIMUM`: message tables certifying the minimum finite assignment cost;
- `DP-REFUTATION`: message tables certifying unsatisfiability.

The implementation is intentionally small and suited to tiny explicit-table instances.

## Exact affine FE-row certificates

The script `affine_fe.py` generates and verifies exact rational affine row certificates:

```bash
python3 affine_fe.py generate examples/two_spring_affine_model.json > examples/two_spring_fe_rows.json
python3 affine_fe.py verify examples/two_spring_affine_model.json examples/two_spring_fe_rows.json
```

Each `FE-ROW` certificate records the scenario row, action assignment, exact response interval, safe interval, and row classification (`SAFE` or `UNSAFE`). The generated batch also contains the finite ECD relation-table instance derived from safe rows.

Run the full current gate with:

```bash
python3 run_repro_checks.py
```

## Sparsification certificates

Exact affine omitted-term sparsification is supported by `affine_fe.py`:

```bash
python3 affine_fe.py sparsify examples/two_spring_affine_model.json examples/two_spring_retained_a1.json > examples/two_spring_sparsification_certificate.json
python3 affine_fe.py verify-sparsify examples/two_spring_affine_model.json examples/two_spring_sparsification_certificate.json
```

The certificate contains exact omitted intervals, response intervals, inner rows, and outer rows. Corrupted sparsification certificates are rejected by the verifier.

## Nontrivial path decomposition examples

The files `examples/path3_sat.json` and `examples/path3_unsat.json` use a two-bag path decomposition:

```bash
python3 finite_ecd.py verify-tree-decomp examples/path3_sat.json examples/path3_tree_decomp.json
python3 finite_ecd.py td-solve examples/path3_sat.json --decomp examples/path3_tree_decomp.json
python3 finite_ecd.py td-solve examples/path3_unsat.json --decomp examples/path3_unsat_tree_decomp.json
```

The satisfiable path instance produces `DP-OPTIMUM` with optimum cost 1. The unsatisfiable path instance produces `DP-REFUTATION`.

## Baseline encoders

The dependency-free script `baseline_encode.py` emits baseline encodings for Boolean explicit-table instances:

```bash
python3 baseline_encode.py dimacs examples/path3_sat.json > examples/path3_sat.cnf
python3 baseline_encode.py milp-lp examples/path3_sat.json > examples/path3_sat.lp
python3 baseline_encode.py cpsat-json examples/path3_sat.json > examples/path3_sat_cpsat.json
```

These are encoders only, not solver comparisons. They are included so future SAT/CP-SAT/MILP comparisons can use identical finite instances.

## Benchmark family generator

`benchmark_gen.py` generates explicit Boolean benchmark families with known width and supplied decompositions:

```bash
python3 benchmark_gen.py path 6 examples/generated_path6
python3 benchmark_gen.py binary-tree 2 examples/generated_btree_depth2
```

Both families have known treewidth 1. The generated decomposition files can be verified and used by `td-solve`.

## Sparsification ladder verification

The verifier can now check rowwise monotonicity for retained scopes `J subset J'`:

```bash
python3 affine_fe.py verify-sparsify-ladder examples/two_spring_affine_model.json \
  examples/two_spring_sparsification_certificate.json \
  examples/two_spring_sparsification_fine_certificate.json
```

It verifies the finite certificate consequences: coarse inner cylinders are contained in fine inner rows, and fine outer rows project into coarse outer rows.

## Optional external solver adapter

`external_solver_adapter.py` wraps optional external solver commands. Missing executables, timeouts, and unrecognised output are reported as `INCONCLUSIVE`:

```bash
python3 external_solver_adapter.py --name minisat --timeout 10 -- minisat examples/path3_sat.cnf
```

No external solver is required for the reproducibility gate.

## Larger exact affine frame example

`examples/four_actuator_frame_affine_model.json` is a larger exact finite affine algebraic example. It generates `FE-ROW` certificates and a finite ECD instance, and the DP certificate verifies.

## External cross-checks

`cross_check_external.py` verifies optional external solver claims against ECD certificates instead of trusting logs:

```bash
python3 cross_check_external.py examples/fake_external_sat.json examples/path3_sat.json --policy examples/path3_policy_certificate.json
python3 cross_check_external.py examples/fake_external_unsat.json examples/path3_unsat.json --refutation examples/path3_dp_refutation_certificate.json
```

SAT claims require a verified policy. UNSAT claims require a verified `DP-REFUTATION`. Without such a certificate, the result is `INCONCLUSIVE`.

## Additional controlled-width families

`benchmark_gen.py` now also supports:

```bash
python3 benchmark_gen.py band 7 examples/generated_band7_w2 --width 2
python3 benchmark_gen.py grid 2 examples/generated_grid2x4 --cols 4
```

The banded-chain family has supplied decomposition width equal to `--width`. The grid family uses a column-pair path decomposition with supplied width `2*rows-1`.

## Summary reports

`report_summary.py` summarizes instance and certificate statistics:

```bash
python3 report_summary.py examples/generated_grid2x4_instance.json \
  --decomp examples/generated_grid2x4_tree_decomp.json \
  --certificate examples/generated_grid2x4_dp_certificate.json
```

Reported fields include instance size, factor rows, width, weighted width, certificate bytes, and verification time.

## Optional installed-solver adapters

`solver_adapters.py` detects and optionally runs installed solvers only when present:

```bash
python3 solver_adapters.py available
python3 solver_adapters.py minisat examples/path3_sat.cnf --timeout 10
python3 solver_adapters.py kissat examples/path3_sat.cnf --timeout 10
python3 solver_adapters.py z3 model.smt2 --timeout 10
```

If a solver is not installed, the adapter reports `INCONCLUSIVE`.

## Benchmark sweeps and plots

Controlled-width benchmark sweeps and simple SVG plots are generated by:

```bash
python3 benchmark_sweep.py --out reports/benchmark_sweep.json
python3 plot_reports.py reports/benchmark_sweep.json --outdir reports
```

Generated plots include:

- `reports/certificate_size_vs_width.svg`
- `reports/verify_time_vs_certificate_size.svg`

## Artifact manifest

See `ARTIFACT_MANIFEST.md` for reproducibility instructions and repository-deposit checklist.

## Fixed-hardware external baseline sweep

`external_baseline_sweep.py` runs the external baseline comparison on identical
finite instances under a fixed protocol, and `cpsat_runner.py` is the isolated
CP-SAT process it drives:

```bash
python3 external_baseline_sweep.py --out reports/external_baseline_sweep.json
```

Solvers are located on `PATH`, or through the environment variables
`EXTERNAL_ECD_MINISAT`, `EXTERNAL_ECD_KISSAT`, `EXTERNAL_ECD_Z3`, and
`EXTERNAL_ECD_CPSAT_PYTHON` (a Python interpreter with `ortools` installed) or `EXTERNAL_ECD_HIGHS_PYTHON` (a Python interpreter with `highspy` installed, driving the HiGHS MILP solver). With
no solver available the report is `INCONCLUSIVE`.

The protocol fixes: a 60 s wall-clock timeout, a 3 GiB address-space cap, and
single-threaded deterministic configurations for every solver. Identical
Boolean explicit-table instances from the controlled-width benchmark families,
plus an unsatisfiable odd-ring family, are encoded with `baseline_encode.py` to
DIMACS CNF and the minimal CP-SAT forbidden-tuple encoding. The native
tree-decomposition DP runs on the same instances with timing; its certificate
is independently re-verified; every external SAT model is parsed, converted to
a policy, and verified natively; every external UNSAT answer is cross-checked
against a verified `DP-REFUTATION` certificate. Timings are whole-process wall
clock, median of three repetitions, and include solver startup.

The command is part of the reproduction gate:

```bash
make reproduce        # or ./reproduce.sh
```

Primary output: `reports/external_baseline_sweep.json`.

## Mechanics benchmark suite (phase 4)

`mechanics_fe.py` converts declared structural models into certified finite
relations with exact rational arithmetic, and verifies them independently:

```bash
python3 mechanics_fe.py generate examples/mech_ten_bar_same_model.json > examples/mech_ten_bar_rows.json
python3 mechanics_fe.py verify examples/mech_ten_bar_same_model.json examples/mech_ten_bar_rows.json
```

Two model kinds are supported: pin-jointed trusses with rational 3-4-5
member directions (node-force and self-equilibrated member-pair actuators,
member-force and node-displacement monitors) and grounded mass-spring chains.
Certificates: `MECH-SOLVE` (base states, verified by exact residual
substitution), `MECH-ROW-BATCH` (exact influence rows and relation tables,
verified by regeneration through independently written assembly and solve
code), `MECH-SPARSIFY-BATCH` (scope-restricted sparsification).

`mechanics_gen.py` declares the benchmark families: the ten-bar cantilever
with quantized load scenarios (same vs split observation), the
pre-tensioned mass-spring chain (bounded width, scales to 1024 springs), the
dense-influence chain (node-force actuators, monitored displacement), and the
cross-braced two-row lattice (width growth with the column count, relation
tables beyond the enumeration limit at three columns). Instances come in
`same` and `split` observation variants; decompositions are constructed by a
deterministic minimum-fill heuristic and validated by the decomposition
verifier. The ten-bar family is cross-validated against the exact affine row
generator of `affine_fe.py`, and its same-observation instance carries a
brute-force sensor-repair certificate.

```bash
python3 mechanics_benchmarks.py --out reports/mechanics_benchmarks.json
```

## Width-adaptive sparsification study (phase 5)

`sparsification_study.py` builds retained-scope ladders by structural
proximity (actuators anchored within member-graph distance r of the monitored
member or node), verifies pairwise ladder monotonicity, solves the inner and
outer finite instances, and classifies the bracket: `CERTIFIED-SAT` (inner
policy extended by zeros and verified against the full certified rows),
`CERTIFIED-UNSAT` (outer refutation), or `INCONCLUSIVE`. The full-radius rung
is the no-sparsification ablation.

```bash
python3 sparsification_study.py --out reports/sparsification_study.json
```

## Comparative scaling study on mechanics instances (phase 6)

`mechanics_baseline_sweep.py` applies the fixed external-baseline protocol to
the mechanics-derived Boolean instances: identical encodings, 60 s timeout,
3 GiB address-space cap, three repetitions with median timing,
single-threaded deterministic configurations, and the same cross-checking
discipline. The native DP runs as a bounded isolated process
(`native_dp_runner.py`). FE preprocessing is accounted separately from the
phase 4 report. Timeouts and unresolved runs are reported as INCONCLUSIVE.

```bash
python3 mechanics_baseline_sweep.py --out reports/mechanics_external_baseline_sweep.json
```

Primary output: `reports/mechanics_external_baseline_sweep.json`. The
recorded run was executed in case chunks with `--only` and `--merge`
(equivalent to a single full invocation); see the release manifest for the
recorded invocation.
