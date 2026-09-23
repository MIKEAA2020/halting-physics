# Artifact appendix: finite ECD prototype

## A. Instance format

A finite explicit-table ECD instance is a JSON object:

```json
{
  "variables": ["x0", "x1"],
  "domains": {"x0": [0, 1], "x1": [0, 1]},
  "value_costs": {"x0": {"0": 0, "1": 1}},
  "factors": [
    {"name": "neq", "scope": ["x0", "x1"], "relation": [[0, 1], [1, 0]]}
  ]
}
```

- `variables`: ordered policy variables.
- `domains`: finite domain for each variable.
- `factors`: explicit permitted tuples on ordered scopes.
- `value_costs`: optional nonnegative value costs for DP optimum certificates.

All main prototype claims are explicit-table claims.

## B. Native certificate schemas

### `POLICY`

```json
{"type": "POLICY", "assignment": {"x0": 0, "x1": 1}}
```

Verified by checking every factor row.

### `FIBRE-CONFLICT`

Certifies that every action in one observation fibre is excluded by at least one named scenario.

### `SENSOR-REPAIR`

Certifies a selected sensor set for tiny one-shot examples. Current optimality certificates are brute-force enumeration certificates for small instances.

### `TREE-DECOMP`

```json
{
  "type": "TREE-DECOMP",
  "root": "b0",
  "bags": {"b0": ["x0", "x1"]},
  "edges": [],
  "factor_to_bag": {"neq": "b0"}
}
```

Verifier checks factor containment, tree connectivity, and running intersection.

### `DP-OPTIMUM` and `DP-REFUTATION`

Contain a `TREE-DECOMP`, message tables, root status, and optimum cost when satisfiable. The verifier recomputes all message tables; solver logs are not trusted.

### `FE-ROW` and `FE-ROW-BATCH`

Exact rational affine row certificates. Each row records action assignment, exact response interval, safety interval, and `SAFE`/`UNSAFE` classification. The batch includes the derived finite ECD instance.

### `SPARSIFICATION-BATCH`

Records retained scopes, exact omitted-term intervals, response intervals, and derived inner/outer sparse finite instances.

### Sparsification ladder certificate

Checked by comparing a coarse and fine `SPARSIFICATION-BATCH` for retained scopes `J subset J'`: coarse inner cylinders must refine into fine inner rows, and fine outer rows must project into coarse outer rows.

## C. Baseline encodings

`baseline_encode.py` emits, for Boolean explicit-table instances:

- DIMACS CNF;
- LP-format MILP;
- minimal CP-SAT forbidden-tuple JSON.

These are encoders only. They do not constitute solver comparisons.

## D. External solver discipline

External solver output is handled in two stages:

1. `solver_adapters.py` or `external_solver_adapter.py` records solver availability, timeout, and raw status.
2. `cross_check_external.py` requires a native ECD certificate before accepting SAT or UNSAT.

Missing solvers, timeouts, and unrecognized output are `INCONCLUSIVE`.

## E. Reproduction

From the artifact directory:

```bash
make reproduce
```

or equivalently:

```bash
./reproduce.sh
```

This runs smoke checks, controlled-width benchmark sweeps, and SVG plot generation.
