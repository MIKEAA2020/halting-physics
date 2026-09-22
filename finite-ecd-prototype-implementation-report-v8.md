# Finite ECD prototype implementation report v8

## New in v8

This implements the mechanics benchmark suite phases 4--6 of the
experimental roadmap: an exact rational mechanics front end with certified
influence rows, mechanics benchmark families with observation variants,
the width-adaptive sparsification study, and the comparative scaling study
on mechanics-derived instances under the fixed external-baseline protocol.

## 1. Exact rational mechanics front end

Added:

```text
mechanics_fe.py
```

Two declared model kinds, both exact rational:

- pin-jointed planar trusses with rational node coordinates and 3-4-5 member
  directions (rational direction cosines), declared axial stiffnesses,
  node-force actuators, self-equilibrated axial member-pair (pre-tension)
  actuators, member-force and node-displacement monitors;
- grounded scalar mass-spring chains with node-force and spring-pair
  actuators and the same monitor types.

Certificates emitted and verified:

- `MECH-SOLVE`: per-scenario base-state solves. The verifier re-assembles
  the stiffness matrix with independently written assembly code and checks
  `K u = F` exactly by substitution, proving the base states without
  re-running the generator's elimination.
- `MECH-ROW-BATCH`: per-(scenario, monitor) rows with exact rational
  constants and sparse actuator influence coefficients, plus the derived
  finite relation tables. The verifier regenerates every row and relation
  through its own assembly (dense Gauss-Jordan with pivoting versus the
  generator's dyad accumulation; an independent chain assembly) and its own
  solvers, and compares. Rows whose support exceeds the relation-enumeration
  cap are marked `RELATION-TABLE-LIMIT`; the cap is recorded in the
  certificate so the verifier reproduces the decision.
- `MECH-SPARSIFY-BATCH`: scope-restricted sparsification certificates with
  per-row omitted intervals, inner and outer counts, and the inner and outer
  finite instances. Ladder verification checks nesting, the inner-cylinder
  inclusion, and the outer projection; the inner-extension check uses the
  two per-term extreme completions, which are binding for all others because
  the response is linear in the omitted actuator values.
- `verify_policy_rows`: exact row-level verification of a structural
  actuator assignment against the certified rows (used for inner-policy
  extension checks).

## 2. Mechanics benchmark families (phase 4)

Added:

```text
mechanics_gen.py
mechanics_benchmarks.py
```

Families (all with two load scenarios and Boolean actuator domains):

| Family | Model | Actuators | Monitors | Measured structure |
|---|---|---|---|---|
| ten-bar | 10-bar cantilever, 3x4 bays, 3-4-5 diagonals | four vertical node forces at the free nodes | ten member forces | dense influence (width 3) |
| chain-pretension | grounded mass-spring chain, unit springs | pre-tension pair per spring | all spring forces | exactly local influence (width 0 at every size) |
| dense-chain | grounded chain, alternating stiffnesses 1 and 2 | node force per node | mid-chain displacement | dense influence (width n-1) |
| lattice | cross-braced two-row lattice, 3x4 cells | pre-tension pairs on verticals and diagonals | all member forces | dense influence; width 5, 11, 17, 23 for C=1..4 |

Observation variants follow the two-spring convention: `same` (both load
scenarios share one command instance) and `split` (a separating sensor gives
each scenario its own command copy). Decompositions are constructed by a
deterministic minimum-fill elimination heuristic and validated by the
tree-decomposition verifier. Instances carry per-actuator value costs, so
`DP-OPTIMUM` reports the minimum number of active actuators.

Recorded gate (`reports/mechanics_benchmarks.json`):

```json
{
  "cases": 20,
  "row_batches_verified": 20,
  "decompositions_verified": 18,
  "dp_certificates_verified": 18,
  "policies_verified": 9,
  "refutations_certified": 9,
  "relation_table_limit_cases": 2,
  "corrupted_row_batches_rejected": 8,
  "corrupted_dp_certificates_rejected": 8
}
```

Every `same` instance is refuted with a verified `DP-REFUTATION` and every
`split` instance solved with a verified `DP-OPTIMUM` policy, including the
1024-spring chain (refutation certified without enumerating assignments) and
the two-column lattice (width 11). Lattice column counts three and four are
recorded with certified influence scopes and widths (17 and 23) but no
instances: their relation tables exceed the enumeration limit and are marked
`RELATION-TABLE-LIMIT`. The ten-bar family is cross-validated against the
exact affine row generator of `affine_fe.py` (derived instances agree), and
its same-observation instance carries a brute-force sensor-repair
certificate (`CERTIFIED-OPT`, one threshold sensor).

A performance fix in `finite_ecd.py` was required for these sizes:
`td_dynamic_program` previously re-enumerated every child bag for every
assignment of a parent bag (quadratic in the bag-table product); it now
precomputes separator-indexed child summaries, and the `Factor.allowed` set
is cached. The change is semantics-preserving: the recorded
external-baseline sweep reproduces byte-identically after the fix
(120/120 status agreement), and the smoke gate is unchanged.

## 3. Width-adaptive sparsification study (phase 5)

Added:

```text
sparsification_study.py
```

Retained-scope ladders by structural proximity: a row's retained scope at
radius r keeps the actuators anchored within member-graph distance r of the
monitored member or node; the full radius is the no-sparsification
ablation. For every rung the study verifies the sparsification certificate,
verifies pairwise ladder monotonicity with the previous rung, solves the
inner and outer instances with verified DP certificates, and classifies the
bracket: `CERTIFIED-SAT` (inner policy extended by zeros on the omitted
actuators and verified exactly against the full certified rows),
`CERTIFIED-UNSAT` (outer refutation, sound because outer relations contain
the true relations), or `INCONCLUSIVE` (inner unsatisfiable while outer
satisfiable). Both observation variants are evaluated per rung.

Recorded study (`reports/sparsification_study.json`):

```json
{
  "families": 6,
  "rungs": 20,
  "sparsify_certificates_verified": 20,
  "ladder_steps_verified": 14,
  "inner_dp_certificates_verified": 20,
  "outer_dp_certificates_verified": 20,
  "same_brackets_certified_unsat": 9,
  "same_brackets_inconclusive": 11,
  "split_brackets_certified_sat": 9,
  "split_brackets_inconclusive": 11,
  "policies_verified_against_full_rows": 9
}
```

Recorded tradeoff (mean unresolved fraction, the share of outer rows that
are not inner rows, per family and radius): dense-chain n=12 decreases
monotonically 1.0, 1.0, 1.0, 1.0, 0.0 across radii 0..full; lattice C=1
0.33, 0.15, 0.0, 0.0; lattice C=2 0.64, 0.27, 0.0; lattice C=3 0.70, 0.34
(dense instance beyond the relation limit). The chain-pretension family
needs no sparsification: its exact influence scopes are singletons, and the
full-radius rung certifies at width 0. On these calibrated families the
brackets certify only at (or near) the full radius: the omitted-interval
tails dominate the safety windows at small radii, so aggressive
sparsification is sound but inconclusive. The study reports this honestly;
it does not claim a practical width-reduction benefit.

## 4. Comparative scaling study on mechanics instances (phase 6)

Added:

```text
native_dp_runner.py
mechanics_baseline_sweep.py
```

The fixed external-baseline protocol (60 s timeout, 3 GiB address-space cap,
three repetitions with median timing, single-threaded deterministic
configurations, identical encodings, native cross-checking) is applied to
fourteen Boolean instances derived from the mechanics families. The native
pipeline runs as a bounded isolated process that loads the instance, runs
the DP, re-verifies the certificate, and reconstructs and verifies a policy
when satisfiable, so native and external wall-clock figures cover comparable
whole-process pipelines. FE preprocessing is accounted separately from the
phase 4 report and excluded from both sides.

A latent call bug in `external_baseline_sweep.py` was fixed (the HiGHS
version probe called `ighs_python` instead of the `[highs_python]` command
list; it only triggered when HiGHS ran from a separate interpreter without
`highspy` importable in the harness interpreter).

The recorded run was executed in case chunks with `--only` and `--merge`
(equivalent to a single full invocation) because the environment terminates
long-running sessions; the merged report is the recorded artifact.

Recorded summary (`reports/mechanics_external_baseline_sweep.json`):

```json
{
  "instances": 14,
  "native_certificates_verified": 14,
  "native_policies_verified": 7,
  "native_inconclusive": 0,
  "external_runs": 70,
  "external_sat_cross_checked": 34,
  "external_unsat_cross_checked": 33,
  "external_inconclusive": 3,
  "external_rejected": 0,
  "status_agreement_with_native": 67
}
```

Recorded observations: on the width-bounded and small-width families every
solver answers in milliseconds and the native Python pipeline is slower in
wall-clock, consistent with the recorded external-baseline sweep. On the
dense-influence family at n=16 (encoding 130,942 clauses), minisat exceeds
the 60 s limit on both observation variants and HiGHS exceeds it on the
unsatisfiable variant, while kissat answers in 3.8 s, z3 in 1.7 s, and the
native DP certifies the refutation in 7.2 s wall-clock (2.2 s DP, 3.1 s
verification, 57 MB certificate). CP-SAT returned unknown within its limit
on the unsatisfiable dense instance. These are per-instance observations on
one family and size; the study makes no performance-superiority claim. The
native certificates for the dense family grow as 2^n (57 MB and 116 MB at
n=16), which is the recorded cost of the certificate-emitting pipeline and
the honest boundary of the dense family in this artifact.

## 5. Reproduction gate updated

- `Makefile` and `reproduce.sh` include the gated steps
  `mechanics-benchmarks`, `sparsification-study`, and `mechanics-baselines`
  in `make reproduce`; with no external solver installed the mechanics
  baseline report is `INCONCLUSIVE`.
- `run_repro_checks.py` adds mechanics smoke checks: ten-bar row-batch
  verification, corrupted row-batch rejection, same-observation refutation,
  split-observation optimum, sensor-repair certification, and the
  sixteen-spring chain refutation.
- `README.md` documents the mechanics layer, the three study commands, and
  the chunked invocation note.

All gate components were re-executed in the recorded environment: the
external-baseline sweep reproduces its recorded summary exactly; the
mechanics benchmark suite, sparsification study, and mechanics baseline
sweep produce the recorded reports above.

## 6. Release manifest refreshed

`RELEASE_MANIFEST.md` now records release tag `halting_physics_workspace_v4`
with the mechanics study outputs added to the expected outputs and the files
to archive, the chunked mechanics-baseline invocation, the exclusion note
for regenerable dense-chain encodings and duplicate native certificates, and
the unchanged claim boundary. The DOI field remains open until an archival
identifier is assigned at publication time.

## 7. Companion manuscript update

The companion article reports the three studies in dedicated sections: the
mechanics benchmark suite (families, protocol, results, and the sensor
structure), the width-adaptive sparsification study (ladder protocol, the
recorded tradeoff, and the inconclusiveness finding), and the comparative
scaling study on mechanics instances (protocol, results, and the claim
boundary). Both the article and the artifact appendix are versioned as new
files; earlier versions are unchanged.
