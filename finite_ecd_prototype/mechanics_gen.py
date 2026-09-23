#!/usr/bin/env python3
"""Mechanics benchmark families: declared structural models and instances.

Families
--------
- ``ten-bar``: the classic ten-bar cantilever with 3x4 bays and 3-4-5
  diagonals, vertical quantized load scenarios at the tip, four vertical
  node-force actuators, and member-force monitors. Tests the FE-to-ECD
  pipeline and the quantized-sensor structure (same vs split observation).
- ``chain-pretension``: grounded mass-spring chain with a self-equilibrated
  pre-tension pair on every spring and spring-force monitors. The exact
  influence of each pair is local, so the family has bounded width and
  scales in the pipeline.
- ``dense-chain``: grounded mass-spring chain with node-force actuators and a
  monitored mid-chain displacement. The exact influence of every actuator on
  the monitor is nonzero, so the family is a dense-influence stress test.
- ``lattice``: cross-braced two-row lattice with pre-tension pairs on the
  verticals and diagonals and member-force monitors. Influence is dense, so
  decomposition width grows linearly with the column count: the width-growth
  boundary family.

Every family declares two load scenarios. Instances come in two observation
variants following the two-spring convention: ``same`` (both scenarios share
one command instance; observation-uniform policies must satisfy both) and
``split`` (a separating sensor gives each scenario its own command copy).

Decompositions are constructed by a deterministic minimum-fill elimination
heuristic and validated by the tree-decomposition verifier of
``finite_ecd.py``.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import mechanics_fe


# ---------------------------------------------------------------------------
# Structural models
# ---------------------------------------------------------------------------

def ten_bar_model() -> Dict[str, Any]:
    nodes = [
        {"id": "n1", "x": "0", "y": "4", "support": ["x", "y"]},
        {"id": "n2", "x": "0", "y": "0", "support": ["x", "y"]},
        {"id": "n3", "x": "3", "y": "4"},
        {"id": "n4", "x": "3", "y": "0"},
        {"id": "n5", "x": "6", "y": "4"},
        {"id": "n6", "x": "6", "y": "0"},
    ]
    members = [
        {"name": "top_left", "a": "n1", "b": "n3", "k": "1"},
        {"name": "top_right", "a": "n3", "b": "n5", "k": "1"},
        {"name": "bot_left", "a": "n2", "b": "n4", "k": "1"},
        {"name": "bot_right", "a": "n4", "b": "n6", "k": "1"},
        {"name": "vert_mid", "a": "n3", "b": "n4", "k": "1"},
        {"name": "vert_tip", "a": "n5", "b": "n6", "k": "1"},
        {"name": "diag_14", "a": "n1", "b": "n4", "k": "1"},
        {"name": "diag_23", "a": "n2", "b": "n3", "k": "1"},
        {"name": "diag_36", "a": "n3", "b": "n6", "k": "1"},
        {"name": "diag_45", "a": "n4", "b": "n5", "k": "1"},
    ]
    return {
        "name": "ten_bar_truss",
        "kind": "truss",
        "nodes": nodes,
        "supports": [{"node": "n1"}, {"node": "n2"}],
        "members": members,
        "actuators": [
            {"name": "act_n3", "type": "node-force", "node": "n3", "components": ["0", "1"]},
            {"name": "act_n4", "type": "node-force", "node": "n4", "components": ["0", "1"]},
            {"name": "act_n5", "type": "node-force", "node": "n5", "components": ["0", "1"]},
            {"name": "act_n6", "type": "node-force", "node": "n6", "components": ["0", "1"]},
        ],
        "scenarios": [
            {"name": "load_low", "forces": [{"node": "n5", "components": ["0", "-1"]}]},
            {"name": "load_high", "forces": [{"node": "n5", "components": ["0", "-2"]}]},
        ],
        "monitors": [{"name": f"force_{m['name']}", "type": "member-force", "member": m["name"]}
                     for m in members],
        "actuator_domain": [0, 1],
        "safe_interval": ["-3/4", "3/4"],
    }


def chain_pretension_model(n: int) -> Dict[str, Any]:
    return {
        "name": f"chain_pretension_{n}",
        "kind": "scalar-chain",
        "nodes": n,
        "springs": [{"name": f"s{i}", "k": "1"} for i in range(1, n + 1)],
        "actuators": [{"name": f"p{i}", "type": "spring-pair", "spring": i, "sign": "-1"}
                      for i in range(1, n + 1)],
        "scenarios": [
            {"name": "load_low", "forces": [{"node": 1, "component": "1"}]},
            {"name": "load_high", "forces": [{"node": n, "component": "1"}]},
        ],
        "monitors": [{"name": f"t{i}", "type": "spring-force", "spring": i}
                     for i in range(1, n + 1)],
        "actuator_domain": [0, 1],
        "safe_interval": ["-1/4", "3/4"],
    }


def dense_chain_model(n: int) -> Dict[str, Any]:
    m = n // 2
    return {
        "name": f"dense_chain_{n}",
        "kind": "scalar-chain",
        "nodes": n,
        "springs": [{"name": f"s{i}", "k": "1" if i % 2 == 1 else "2"} for i in range(1, n + 1)],
        "actuators": [{"name": f"a{i}", "type": "node-force", "node": i, "component": "-1/2"}
                      for i in range(1, n + 1)],
        "scenarios": [
            {"name": "load_low", "forces": [{"node": 1, "component": "1"}]},
            {"name": "load_high", "forces": [{"node": n, "component": "1"}]},
        ],
        "monitors": [{"name": f"u{m}", "type": "node-displacement", "node": m}],
        "actuator_domain": [0, 1],
        "safe_interval": ["1/4", "9/8"],
    }


def lattice_model(C: int) -> Dict[str, Any]:
    nodes = []
    for j in range(C + 1):
        for i in range(3):
            node = {"id": f"n_{j}_{i}", "x": str(3 * j), "y": str(4 * i)}
            if j == 0:
                node["support"] = ["x", "y"]
            nodes.append(node)
    members = []
    for j in range(C):
        for i in range(3):
            members.append({"name": f"h{j}_{i}", "a": f"n_{j}_{i}", "b": f"n_{j+1}_{i}", "k": "1"})
    for j in range(1, C + 1):
        for i in range(2):
            members.append({"name": f"v{j}_{i}", "a": f"n_{j}_{i}", "b": f"n_{j}_{i+1}", "k": "1"})
    for j in range(C):
        for i in range(2):
            members.append({"name": f"d{j}_{i}p", "a": f"n_{j}_{i}", "b": f"n_{j+1}_{i+1}", "k": "1"})
            members.append({"name": f"d{j}_{i}m", "a": f"n_{j}_{i+1}", "b": f"n_{j+1}_{i}", "k": "1"})
    actuators = []
    for m in members:
        is_vertical = m["name"].startswith("v")
        is_diagonal = m["name"].startswith("d")
        if is_vertical or is_diagonal:
            actuators.append({"name": f"pair_{m['name']}", "type": "member-pair",
                              "member": m["name"], "sign": "-1"})
    return {
        "name": f"cross_braced_lattice_{C}",
        "kind": "truss",
        "nodes": nodes,
        "supports": [{"node": f"n_0_{i}"} for i in range(3)],
        "members": members,
        "actuators": actuators,
        "scenarios": [
            {"name": "load_top", "forces": [{"node": f"n_{C}_2", "components": ["1", "0"]}]},
            {"name": "load_bot", "forces": [{"node": f"n_{C}_0", "components": ["1", "0"]}]},
        ],
        "monitors": [{"name": f"force_{m['name']}", "type": "member-force", "member": m["name"]}
                     for m in members],
        "actuator_domain": [0, 1],
        "safe_interval": ["-1", "1/2"],
    }


# ---------------------------------------------------------------------------
# Instance construction
# ---------------------------------------------------------------------------

def _int_values(rel):
    out = []
    for row in rel["relation"]:
        out.append([int(v) for v in row])
    return out


def build_instance(model: Dict[str, Any], batch: Dict[str, Any],
                   observation: str) -> Dict[str, Any]:
    """Build a finite ECD instance from a certified row batch.

    ``same``: one Boolean actuator per structural actuator; every scenario's
    rows constrain the shared command variables.
    ``split``: one Boolean copy per (actuator, scenario); each scenario's
    rows constrain its own copy, realising a separating sensor.
    """
    actuator_names = [a["name"] for a in model["actuators"]]
    scenario_names = [sc["name"] for sc in model["scenarios"]]
    factors = []
    if observation == "same":
        variables = list(actuator_names)
        domains = {x: [0, 1] for x in variables}
        for rel in batch["relations"]:
            factors.append({
                "name": f"{rel['scenario']}__{rel['monitor']}",
                "scope": list(rel["scope"]),
                "relation": _int_values(rel),
            })
    elif observation == "split":
        variables = []
        domains = {}
        for sc in scenario_names:
            for a in actuator_names:
                x = f"{a}__{sc}"
                variables.append(x)
                domains[x] = [0, 1]
        for rel in batch["relations"]:
            scope = [f"{x}__{rel['scenario']}" for x in rel["scope"]]
            factors.append({
                "name": f"{rel['scenario']}__{rel['monitor']}",
                "scope": scope,
                "relation": _int_values(rel),
            })
    else:
        raise ValueError(f"unknown observation variant {observation}")
    value_costs = {x: {"0": 0, "1": 1} for x in variables}
    return {
        "variables": variables,
        "domains": domains,
        "value_costs": value_costs,
        "factors": factors,
        "metadata": {
            "family": model["name"],
            "observation": observation,
            "actuator_count": len(actuator_names),
            "row_count": len(batch["relations"]),
            "max_scope": batch.get("max_scope"),
        },
    }


def min_fill_decomp(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic minimum-fill tree decomposition of the factor scopes."""
    scopes = [list(f["scope"]) for f in instance["factors"]]
    adj: Dict[str, set] = {}
    for scope in scopes:
        for x in scope:
            adj.setdefault(x, set())
        for i, x in enumerate(scope):
            for y in scope[i + 1:]:
                adj[x].add(y)
                adj[y].add(x)
    for x in instance.get("variables", []):
        if x not in adj:
            adj[x] = set()
    remaining = set(adj)
    order: List[str] = []
    fill_edges: Dict[str, List[Tuple[str, str]]] = {}
    while remaining:
        best = None
        best_key = None
        for x in sorted(remaining):
            neigh = sorted(adj[x] & remaining)
            fill = 0
            pairs = []
            for i, u in enumerate(neigh):
                for v in neigh[i + 1:]:
                    if v not in adj[u]:
                        fill += 1
                        pairs.append((u, v))
            key = (fill, len(neigh), x)
            if best_key is None or key < best_key:
                best_key = key
                best = (x, neigh, pairs)
        x, neigh, pairs = best
        order.append(x)
        fill_edges[x] = pairs
        for u, v in pairs:
            adj[u].add(v)
            adj[v].add(u)
        remaining.discard(x)

    bags: Dict[str, List[str]] = {}
    bag_of_var: Dict[str, str] = {}
    elim_pos = {x: i for i, x in enumerate(order)}
    edges: List[List[str]] = []
    for x in order:
        bag_name = f"b_{x}"
        neigh = sorted(adj[x] & {y for y in order if elim_pos[y] > elim_pos[x]})
        bags[bag_name] = [x] + neigh
        bag_of_var[x] = bag_name
        later = [y for y in neigh if elim_pos[y] > elim_pos[x]]
        if later:
            parent_var = min(later, key=lambda y: elim_pos[y])
            edges.append([bag_name, f"b_{parent_var}"])
    # connect disconnected bag components in a chain
    if bags:
        bag_names = list(bags)
        adjacency: Dict[str, set] = {b: set() for b in bag_names}
        for u, v in edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        seen = set()
        components: List[List[str]] = []
        for b in bag_names:
            if b in seen:
                continue
            comp = []
            stack = [b]
            while stack:
                c = stack.pop()
                if c in seen:
                    continue
                seen.add(c)
                comp.append(c)
                stack.extend(adjacency[c] - seen)
            components.append(sorted(comp))
        prev_root = None
        for comp in components:
            root = comp[0]
            if prev_root is not None:
                edges.append([prev_root, root])
            prev_root = root
    factor_to_bag = {}
    for f in instance["factors"]:
        scope = list(f["scope"])
        target = None
        for x in sorted(scope, key=lambda y: elim_pos[y]):
            bag = bag_of_var[x]
            if set(scope) <= set(bags[bag]):
                target = bag
                break
        if target is None:
            for b, xs in bags.items():
                if set(scope) <= set(xs):
                    target = b
                    break
        factor_to_bag[f["name"]] = target
    root = next(iter(bags))
    width = max(len(xs) - 1 for xs in bags.values()) if bags else 0
    return {
        "type": "TREE-DECOMP",
        "root": root,
        "bags": bags,
        "edges": edges,
        "factor_to_bag": factor_to_bag,
        "metadata": {"construction": "deterministic min-fill elimination", "width": width},
    }


def ten_bar_affine_model(model: Dict[str, Any], batch: Dict[str, Any]) -> Dict[str, Any]:
    """Cross-validation model for the exact affine row generator."""
    variables = [a["name"] for a in model["actuators"]]
    rows = []
    for row, rel in zip(batch["rows"], batch["relations"]):
        rows.append({
            "name": f"{row['scenario']}__{row['monitor']}",
            "d": row["constant"],
            "coeffs": dict(row["coeffs"]),
        })
    return {
        "name": "ten_bar_truss_affine",
        "variables": variables,
        "domains": {x: [0, 1] for x in variables},
        "safe_interval": list(model["safe_interval"]),
        "rows": rows,
    }


def ten_bar_sensor_data(model: Dict[str, Any], batch: Dict[str, Any]) -> Dict[str, Any]:
    """Scenario/sensor data for the brute-force sensor-repair demonstrator.

    The admissible set of a scenario is the intersection of all its row
    relations, i.e. the tuples safe under every monitor of that scenario.
    """
    actions = []
    for values in _domain_product(len(model["actuators"])):
        actions.append(list(values))
    scenarios = []
    for sc in model["scenarios"]:
        sets = []
        for rel in batch["relations"]:
            if rel["scenario"] == sc["name"]:
                sets.append({tuple(int(v) for v in row) for row in rel["relation"]})
        admissible = sorted(set.intersection(*sets)) if sets else []
        scenarios.append({
            "name": sc["name"],
            "observation": "coarse",
            "admissible": [list(t) for t in admissible],
        })
    sensors = [{
        "name": "load_cell_threshold",
        "values": {sc["name"]: i for i, sc in enumerate(model["scenarios"])},
    }]
    return {"actions": actions, "scenarios": scenarios, "sensors": sensors}


def _domain_product(arity: int):
    import itertools
    return itertools.product([0, 1], repeat=arity)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

FAMILIES = {
    "ten-bar": lambda size: ten_bar_model(),
    "chain-pretension": lambda size: chain_pretension_model(size),
    "dense-chain": lambda size: dense_chain_model(size),
    "lattice": lambda size: lattice_model(size),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=list(FAMILIES))
    ap.add_argument("size", type=int, help="1 for ten-bar, n for chains, C for lattice")
    ap.add_argument("out_prefix")
    ap.add_argument("--observation", choices=["same", "split"], default="same")
    args = ap.parse_args()
    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    model = FAMILIES[args.family](args.size)
    batch = mechanics_fe.generate(model)
    instance = build_instance(model, batch, args.observation)
    decomp = min_fill_decomp(instance)
    Path(str(prefix) + "_model.json").write_text(json.dumps(model, indent=2))
    Path(str(prefix) + "_row_batch.json").write_text(json.dumps(batch, indent=2))
    Path(str(prefix) + "_instance.json").write_text(json.dumps(instance, indent=2))
    Path(str(prefix) + "_tree_decomp.json").write_text(json.dumps(decomp, indent=2))
    print(json.dumps({
        "model": str(prefix) + "_model.json",
        "row_batch": str(prefix) + "_row_batch.json",
        "instance": str(prefix) + "_instance.json",
        "tree_decomp": str(prefix) + "_tree_decomp.json",
        "variables": len(instance["variables"]),
        "factors": len(instance["factors"]),
        "max_scope": batch["max_scope"],
        "width": decomp["metadata"]["width"],
    }, indent=2))


if __name__ == "__main__":
    main()
