#!/usr/bin/env python3
"""Generate small finite ECD benchmark families with known treewidth.

Families are explicit Boolean table instances with supplied tree decompositions.
They are intended for certificate and encoder tests, not performance claims.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def neq_relation():
    return [[0, 1], [1, 0]]


def path_instance(n: int):
    variables = [f"x{i}" for i in range(n)]
    inst = {
        "variables": variables,
        "domains": {x: [0, 1] for x in variables},
        "value_costs": {x: {"0": 0, "1": 1} for x in variables},
        "factors": [
            {"name": f"neq{i}_{i+1}", "scope": [f"x{i}", f"x{i+1}"], "relation": neq_relation()}
            for i in range(n - 1)
        ],
        "metadata": {"family": "path-neq", "known_treewidth": 1, "known_pathwidth": 1}
    }
    bags = {f"b{i}_{i+1}": [f"x{i}", f"x{i+1}"] for i in range(n - 1)}
    edges = [[f"b{i}_{i+1}", f"b{i+1}_{i+2}"] for i in range(n - 2)]
    decomp = {
        "type": "TREE-DECOMP",
        "root": "b0_1" if n > 1 else "b0",
        "bags": bags if n > 1 else {"b0": ["x0"]},
        "edges": edges,
        "factor_to_bag": {f"neq{i}_{i+1}": f"b{i}_{i+1}" for i in range(n - 1)},
        "metadata": {"width": 1 if n > 1 else 0, "family": "path-neq"}
    }
    return inst, decomp


def binary_tree_edges(depth: int):
    # heap indices 0..2^(d+1)-2, levels 0..depth
    count = 2 ** (depth + 1) - 1
    edges = []
    for i in range(count):
        for child in [2*i + 1, 2*i + 2]:
            if child < count:
                edges.append((i, child))
    return count, edges


def tree_instance(depth: int):
    count, tree_edges = binary_tree_edges(depth)
    variables = [f"x{i}" for i in range(count)]
    inst = {
        "variables": variables,
        "domains": {x: [0, 1] for x in variables},
        "value_costs": {x: {"0": 0, "1": 1} for x in variables},
        "factors": [
            {"name": f"neq{u}_{v}", "scope": [f"x{u}", f"x{v}"], "relation": neq_relation()}
            for u, v in tree_edges
        ],
        "metadata": {"family": "binary-tree-neq", "depth": depth, "known_treewidth": 1}
    }
    bags = {f"b{u}_{v}": [f"x{u}", f"x{v}"] for u, v in tree_edges}
    # Connect edge-bags into a valid tree decomposition. For each non-root
    # internal vertex, child-edge bags attach to the parent-edge bag. Root child
    # edge bags are chained so bags containing x0 are connected.
    bag_edges = []
    root_child_bags = []
    for u, v in tree_edges:
        if u == 0:
            root_child_bags.append(f"b{u}_{v}")
        else:
            parent = (u - 1) // 2
            bag_edges.append([f"b{parent}_{u}", f"b{u}_{v}"])
    for a, b in zip(root_child_bags, root_child_bags[1:]):
        bag_edges.append([a, b])
    root_bag = root_child_bags[0] if root_child_bags else "b0"
    decomp = {
        "type": "TREE-DECOMP",
        "root": root_bag,
        "bags": bags if tree_edges else {"b0": ["x0"]},
        "edges": bag_edges,
        "factor_to_bag": {f"neq{u}_{v}": f"b{u}_{v}" for u, v in tree_edges},
        "metadata": {"width": 1 if tree_edges else 0, "family": "binary-tree-neq"}
    }
    return inst, decomp



def not_all_equal_relation(arity: int):
    import itertools
    return [list(vals) for vals in itertools.product([0, 1], repeat=arity) if len(set(vals)) > 1]


def band_instance(n: int, width: int):
    """Banded chain with window factors of arity width+1 and supplied path decomposition.

    The supplied decomposition has bags [x_i,...,x_{i+width}], so decomposition
    width is exactly width when n > width.
    """
    variables = [f"x{i}" for i in range(n)]
    factors = []
    bags = {}
    f2b = {}
    for i in range(max(1, n - width)):
        scope = [f"x{j}" for j in range(i, min(n, i + width + 1))]
        name = f"window{i}"
        factors.append({"name": name, "scope": scope, "relation": not_all_equal_relation(len(scope))})
        bname = f"b{i}"
        bags[bname] = scope
        f2b[name] = bname
    edges = [[f"b{i}", f"b{i+1}"] for i in range(len(bags)-1)]
    actual_width = max(len(b) for b in bags.values()) - 1
    inst = {
        "variables": variables,
        "domains": {x: [0, 1] for x in variables},
        "value_costs": {x: {"0": 0, "1": 1} for x in variables},
        "factors": factors,
        "metadata": {"family": "banded-chain-not-all-equal", "n": n, "decomposition_width": actual_width}
    }
    decomp = {"type": "TREE-DECOMP", "root": "b0", "bags": bags, "edges": edges, "factor_to_bag": f2b, "metadata": {"width": actual_width, "family": "banded-chain-not-all-equal"}}
    return inst, decomp


def grid_instance(rows: int, cols: int):
    """Grid disequality with supplied column-pair path decomposition.

    Bag j contains columns j and j+1, all rows. Width is at most 2*rows-1.
    """
    variables = [f"x{r}_{c}" for r in range(rows) for c in range(cols)]
    factors = []
    # horizontal and vertical disequality factors
    for r in range(rows):
        for c in range(cols-1):
            factors.append({"name": f"h{r}_{c}", "scope": [f"x{r}_{c}", f"x{r}_{c+1}"], "relation": neq_relation()})
    for r in range(rows-1):
        for c in range(cols):
            factors.append({"name": f"v{r}_{c}", "scope": [f"x{r}_{c}", f"x{r+1}_{c}"], "relation": neq_relation()})
    bags = {}
    if cols == 1:
        bags["b0"] = [f"x{r}_0" for r in range(rows)]
    else:
        for c in range(cols-1):
            bags[f"b{c}"] = [f"x{r}_{cc}" for cc in [c, c+1] for r in range(rows)]
    edges = [[f"b{c}", f"b{c+1}"] for c in range(max(0, cols-2))]
    f2b = {}
    for f in factors:
        scope = set(f["scope"])
        for b, xs in bags.items():
            if scope <= set(xs):
                f2b[f["name"]] = b
                break
    actual_width = max(len(b) for b in bags.values()) - 1
    inst = {
        "variables": variables,
        "domains": {x: [0, 1] for x in variables},
        "value_costs": {x: {"0": 0, "1": 1} for x in variables},
        "factors": factors,
        "metadata": {"family": "grid-neq", "rows": rows, "cols": cols, "supplied_decomposition_width": actual_width}
    }
    decomp = {"type": "TREE-DECOMP", "root": "b0", "bags": bags, "edges": edges, "factor_to_bag": f2b, "metadata": {"width": actual_width, "family": "grid-neq-column-pair"}}
    return inst, decomp

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=["path", "binary-tree", "band", "grid"])
    ap.add_argument("size", type=int, help="path length n, binary-tree depth, band length n, or grid rows")
    ap.add_argument("out_prefix")
    ap.add_argument("--width", type=int, default=2, help="band decomposition width")
    ap.add_argument("--cols", type=int, default=4, help="grid columns")
    args = ap.parse_args()
    if args.family == "path":
        inst, dec = path_instance(args.size)
    elif args.family == "binary-tree":
        inst, dec = tree_instance(args.size)
    elif args.family == "band":
        inst, dec = band_instance(args.size, args.width)
    else:
        inst, dec = grid_instance(args.size, args.cols)
    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    Path(str(prefix) + "_instance.json").write_text(json.dumps(inst, indent=2))
    Path(str(prefix) + "_tree_decomp.json").write_text(json.dumps(dec, indent=2))
    print(json.dumps({"instance": str(prefix) + "_instance.json", "tree_decomp": str(prefix) + "_tree_decomp.json", "metadata": inst["metadata"]}, indent=2))

if __name__ == "__main__":
    main()
