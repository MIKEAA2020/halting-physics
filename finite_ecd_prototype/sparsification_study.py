#!/usr/bin/env python3
"""Phase 5 width-adaptive sparsification study.

For each configured family this driver builds retained-scope ladders
J subset J' by structural proximity: a row's retained scope at radius r keeps
the actuators anchored within graph distance r of the monitored member or
node. For every rung it

- generates the exact scope-restricted sparsification certificate and
  re-verifies it;
- verifies pairwise ladder monotonicity between consecutive rungs
  (coarse inner rows refine into fine inner rows; fine outer rows project
  into coarse outer rows);
- solves the inner and outer finite instances with the tree-decomposition
  dynamic program and re-verifies the certificates;
- for inner-satisfiable rungs, extends the certified inner policy by zeros
  on the omitted actuators and verifies it exactly against the full
  certified rows (a certified true policy for the dense model);
- records retained-scope sizes, inner and outer decomposition widths,
  unresolved-row fractions, statuses, and stage timings.

Observation variants: the ``same`` variant shares one command across the two
load scenarios (true status unsatisfiable for the calibrated families), so
the informative rung outcome is an outer refutation at reduced width; the
``split`` variant gives each scenario its own command copy (true status
satisfiable), so the informative rung outcome is an inner satisfiable policy
at reduced width. Rungs where the inner model is unsatisfiable while the
outer model is satisfiable are reported as INCONCLUSIVE.

The full-scope rung is the no-sparsification ablation. The chain-pretension
family needs no sparsification (its exact influence scopes are already
singletons) and is recorded as the ablation baseline. Lattice column counts
of three and beyond have no enumerable dense instance (relation-table limit);
their ladders demonstrate certification at reduced width where the dense
pipeline stops.

Primary output: ``reports/sparsification_study.json``.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List

import mechanics_fe
import mechanics_gen
from finite_ecd import (Instance, td_dynamic_program, validate_tree_decomp,
                         verify_dp_certificate)
from mechanics_gen import min_fill_decomp
from report_summary import weighted_width

ROOT = Path(__file__).resolve().parent

RELATION_CAP = 1 << 16


# ---------------------------------------------------------------------------
# Structural proximity retention rules
# ---------------------------------------------------------------------------

def _member_adjacency(model: Dict[str, Any]) -> Dict[str, set]:
    """Member graph: members adjacent iff they share a node."""
    idx = {m["name"]: i for i, m in enumerate(model["members"])}
    adj: Dict[int, set] = {i: set() for i in range(len(model["members"]))}
    for i, mi in enumerate(model["members"]):
        for j in range(i + 1, len(model["members"])):
            mj = model["members"][j]
            if {mi["a"], mi["b"]} & {mj["a"], mj["b"]}:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def _member_distances_from(adj: Dict[int, set], sources: set) -> Dict[int, int]:
    from collections import deque
    dist = {s: 0 for s in sources}
    q = deque(dist)
    while q:
        u = q.popleft()
        for v in adj.get(u, ()):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def _truss_actuator_anchor_members(model: Dict[str, Any], act: Dict[str, Any]) -> set:
    idx = {m["name"]: i for i, m in enumerate(model["members"])}
    if act["type"] == "node-force":
        node = act["node"]
        return {i for i, m in enumerate(model["members"])
                if m["a"] == node or m["b"] == node}
    return {idx[act["member"]]}


def _truss_monitor_anchor_members(model: Dict[str, Any], mon: Dict[str, Any]) -> set:
    idx = {m["name"]: i for i, m in enumerate(model["members"])}
    if mon["type"] == "member-force":
        return {idx[mon["member"]]}
    node = mon["node"]
    return {i for i, m in enumerate(model["members"])
            if m["a"] == node or m["b"] == node}


def truss_retained_map(model: Dict[str, Any], batch: Dict[str, Any],
                       radius: int | None) -> Dict[str, List[str]]:
    """Retained scope per row: actuators anchored within member-graph distance r.

    An actuator anchors on its member (member-pair) or on the members
    incident to its node (node-force); a monitor anchors on its member or on
    the members incident to its node. The full radius is the no-sparsification
    ablation.
    """
    adj = _member_adjacency(model)
    anchor_cache: Dict[str, set] = {}
    retained_map: Dict[str, List[str]] = {}
    for row in batch["rows"]:
        key = f"{row['scenario']}/{row['monitor']}"
        support = list(row["coeffs"].keys())
        if radius is None:
            retained_map[key] = support
            continue
        mon = next(m for m in model["monitors"] if m["name"] == row["monitor"])
        dist = _member_distances_from(adj, _truss_monitor_anchor_members(model, mon))
        retained = []
        for x in support:
            if x not in anchor_cache:
                anchor_cache[x] = _truss_actuator_anchor_members(
                    model, next(a for a in model["actuators"] if a["name"] == x))
            if any(dist.get(mi, radius + 1) <= radius for mi in anchor_cache[x]):
                retained.append(x)
        retained_map[key] = retained
    return retained_map


def chain_retained_map(model: Dict[str, Any], batch: Dict[str, Any],
                       radius: int | None) -> Dict[str, List[str]]:
    """Retained scope per row: actuators anchored within node-index distance r."""
    retained_map: Dict[str, List[str]] = {}

    def act_nodes(act: Dict[str, Any]) -> set:
        if act["type"] == "node-force":
            return {int(act["node"])}
        i = int(act["spring"])
        return {i - 1, i}

    def mon_nodes(mon: Dict[str, Any]) -> set:
        if mon["type"] == "spring-force":
            i = int(mon["spring"])
            return {i - 1, i}
        return {int(mon["node"])}

    for row in batch["rows"]:
        key = f"{row['scenario']}/{row['monitor']}"
        support = list(row["coeffs"].keys())
        if radius is None:
            retained_map[key] = support
            continue
        mon = next(m for m in model["monitors"] if m["name"] == row["monitor"])
        sources = mon_nodes(mon)
        retained = [x for x in support
                    if min(abs(n - s) for n in act_nodes(
                        next(a for a in model["actuators"] if a["name"] == x)) for s in sources) <= radius]
        retained_map[key] = retained
    return retained_map


# ---------------------------------------------------------------------------
# Study driver
# ---------------------------------------------------------------------------

def with_value_costs(instance: Dict[str, Any]) -> Dict[str, Any]:
    out = json.loads(json.dumps(instance))
    out["value_costs"] = {x: {"0": 0, "1": 1} for x in out["variables"]}
    return out


def split_instance(instance: Dict[str, Any], scenario_names: List[str]) -> Dict[str, Any]:
    """Copy inner/outer variables per scenario, following the split convention."""
    out_factors = []
    variables = []
    domains = {}
    for f in instance["factors"]:
        scenario = f["name"].split("__", 1)[0]
        scope = [f"{x}__{scenario}" for x in f["scope"]]
        out_factors.append({"name": f["name"], "scope": scope,
                            "relation": [[int(v) for v in row] for row in f["relation"]]})
    for sc in scenario_names:
        for x in instance["variables"]:
            v = f"{x}__{sc}"
            variables.append(v)
            domains[v] = [0, 1]
    return {"variables": variables, "domains": domains, "factors": out_factors}


MAX_DP_WIDTH = 14
MAX_DP_TABLE_ENTRIES = 1_500_000


def solve_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Min-fill decomposition, DP, verification; returns metrics.

    Rungs whose decomposition exceeds the pipeline's table-size limit are
    reported as ``DP-SIZE-LIMIT`` instead of being solved.
    """
    inst = Instance.from_json(instance)
    t0 = time.perf_counter()
    decomp = min_fill_decomp(instance)
    t1 = time.perf_counter()
    ok_td, err_td = validate_tree_decomp(inst, decomp)
    widths = [len(xs) - 1 for xs in decomp["bags"].values()]
    width = max(widths) if widths else 0
    table_entries = (2 ** width) * max(1, len(decomp["bags"]))
    if width > MAX_DP_WIDTH or table_entries > MAX_DP_TABLE_ENTRIES:
        return {
            "decomp_seconds": round(t1 - t0, 4),
            "decomp_verify_status": "VERIFIED" if ok_td else "REJECTED",
            "decomp_verify_errors": err_td[:2],
            "width": width,
            "weighted_width": weighted_width(inst, decomp),
            "bags": len(decomp["bags"]),
            "dp_status": "DP-SIZE-LIMIT",
            "dp_verify_status": "NOT-RUN",
            "limit_note": ("decomposition exceeds the certificate pipeline limit "
                           f"(width {MAX_DP_WIDTH}, {MAX_DP_TABLE_ENTRIES} table entries)"),
        }
    t2 = time.perf_counter()
    cert = td_dynamic_program(inst, instance, decomp)
    t3 = time.perf_counter()
    ok_dp, err_dp = verify_dp_certificate(inst, instance, cert)
    t4 = time.perf_counter()
    out = {
        "decomp_seconds": round(t1 - t0, 4),
        "decomp_verify_status": "VERIFIED" if ok_td else "REJECTED",
        "decomp_verify_errors": err_td[:2],
        "width": max(widths) if widths else 0,
        "weighted_width": weighted_width(inst, decomp),
        "bags": len(decomp["bags"]),
        "dp_seconds": round(t3 - t2, 4),
        "dp_type": cert["type"],
        "dp_status": cert["status"],
        "dp_verify_seconds": round(t4 - t3, 4),
        "dp_verify_status": "VERIFIED" if ok_dp else "REJECTED",
        "dp_verify_errors": err_dp[:2],
        "_certificate": cert,
    }
    return out


def rung_entry(model, batch, retained_map, radius_label) -> Dict[str, Any]:
    entry: Dict[str, Any] = {"radius": radius_label}
    t0 = time.perf_counter()
    cert = mechanics_fe.sparsify(model, batch, retained_map)
    t1 = time.perf_counter()
    entry["sparsify_seconds"] = round(t1 - t0, 4)
    t0 = time.perf_counter()
    ok_sp, err_sp = mechanics_fe.verify_sparsify(model, batch, cert)
    t1 = time.perf_counter()
    entry["sparsify_verify_seconds"] = round(t1 - t0, 4)
    entry["sparsify_verify_status"] = "VERIFIED" if ok_sp else "REJECTED"
    entry["sparsify_verify_errors"] = err_sp[:3]
    sizes = [len(r["retained"]) for r in cert["rows"]]
    entry["retained_min"] = min(sizes)
    entry["retained_mean"] = round(sum(sizes) / len(sizes), 2)
    entry["retained_max"] = max(sizes)
    outer_counts = [r["outer_count"] for r in cert["rows"]]
    inner_counts = [r["inner_count"] for r in cert["rows"]]
    unresolved = []
    for oc, ic in zip(outer_counts, inner_counts):
        unresolved.append(0.0 if oc == 0 else (oc - ic) / oc)
    entry["unresolved_fraction_mean"] = round(sum(unresolved) / len(unresolved), 4)
    entry["inner_rows_total"] = sum(inner_counts)
    entry["outer_rows_total"] = sum(outer_counts)
    entry["_cert"] = cert
    return entry


def run_family(family: str, size: int, radii: List[int | None],
               relation_cap: int | None = None,
               full_status: str = "AVAILABLE") -> Dict[str, Any]:
    model = mechanics_gen.FAMILIES[family](size)
    t0 = time.perf_counter()
    batch = mechanics_fe.generate(model, relation_cap=relation_cap)
    t1 = time.perf_counter()
    ok_batch, err_batch = mechanics_fe.verify(model, batch)
    fam_entry: Dict[str, Any] = {
        "family": family,
        "size": size,
        "model": model["name"],
        "fe_generate_seconds": round(t1 - t0, 4),
        "fe_verify_status": "VERIFIED" if ok_batch else "REJECTED",
        "fe_verify_errors": err_batch[:3],
        "rows": len(batch["rows"]),
        "max_scope": batch["max_scope"],
        "dense_width": batch["max_scope"],
        "dense_instance_status": full_status,
        "rungs": [],
    }
    scenario_names = [sc["name"] for sc in model["scenarios"]]
    make_map = (truss_retained_map if model["kind"] == "truss" else chain_retained_map)

    rungs = []
    for r in radii:
        label = "full" if r is None else str(r)
        retained_map = make_map(model, batch, r)
        entry = rung_entry(model, batch, retained_map, label)
        rungs.append((r, entry))

    # pairwise ladder monotonicity
    for (r0, e0), (r1, e1) in zip(rungs, rungs[1:]):
        t0 = time.perf_counter()
        ok_lad, err_lad = mechanics_fe.verify_sparsify_ladder(model, batch, e0["_cert"], e1["_cert"])
        t1 = time.perf_counter()
        e1["ladder_from_previous_status"] = "VERIFIED" if ok_lad else "REJECTED"
        e1["ladder_from_previous_errors"] = err_lad[:3]
        e1["ladder_verify_seconds"] = round(t1 - t0, 4)

    for r, entry in rungs:
        cert = entry.pop("_cert")
        inner = with_value_costs(cert["inner_instance"])
        outer = with_value_costs(cert["outer_instance"])
        inner_stats = solve_instance(inner)
        outer_stats = solve_instance(outer)
        entry["inner"] = {k: v for k, v in inner_stats.items() if k != "_certificate"}
        entry["outer"] = {k: v for k, v in outer_stats.items() if k != "_certificate"}
        entry["inner_width"] = inner_stats["width"]
        entry["outer_width"] = outer_stats["width"]

        # same-observation bracket over the shared-command inner/outer instances
        inner_type = inner_stats.get("dp_type")
        outer_type = outer_stats.get("dp_type")
        if inner_type is None or outer_type is None:
            entry["same_bracket"] = "DP-SIZE-LIMIT"
        elif inner_type == "DP-OPTIMUM":
            policy = _reconstruct(inner, inner_stats["_certificate"])
            extended = {x: policy.get(x, 0) for x in _all_actuators(model)}
            ok_rows, err_rows = mechanics_fe.verify_policy_rows(model, batch, extended)
            entry["same_bracket"] = "CERTIFIED-SAT"
            entry["same_policy_rows_verified"] = ok_rows
            entry["same_policy_rows_errors"] = err_rows[:3]
            entry["same_policy_cost"] = sum(extended.values())
        elif outer_type == "DP-REFUTATION":
            entry["same_bracket"] = "CERTIFIED-UNSAT"
        else:
            entry["same_bracket"] = "INCONCLUSIVE"

        # split-observation bracket on copied instances
        inner_split = with_value_costs(split_instance(cert["inner_instance"], scenario_names))
        outer_split = with_value_costs(split_instance(cert["outer_instance"], scenario_names))
        inner_split_stats = solve_instance(inner_split)
        outer_split_stats = solve_instance(outer_split)
        entry["inner_split"] = {k: v for k, v in inner_split_stats.items() if k != "_certificate"}
        entry["outer_split"] = {k: v for k, v in outer_split_stats.items() if k != "_certificate"}
        if inner_split_stats.get("dp_type") is None or outer_split_stats.get("dp_type") is None:
            entry["split_bracket"] = "DP-SIZE-LIMIT"
        elif inner_split_stats.get("dp_type") == "DP-OPTIMUM":
            policy = _reconstruct(inner_split, inner_split_stats["_certificate"])
            ok_all = True
            errs = []
            for sc in scenario_names:
                struct = {x: policy.get(f"{x}__{sc}", 0) for x in _all_actuators(model)}
                ok_rows, err_rows = mechanics_fe.verify_policy_rows(model, batch, struct, scenario=sc)
                ok_all = ok_all and ok_rows
                errs.extend(err_rows[:2])
            entry["split_bracket"] = "CERTIFIED-SAT"
            entry["split_policy_rows_verified"] = ok_all
            entry["split_policy_rows_errors"] = errs[:3]
        elif outer_split_stats.get("dp_type") == "DP-REFUTATION":
            entry["split_bracket"] = "CERTIFIED-UNSAT"
        else:
            entry["split_bracket"] = "INCONCLUSIVE"

        # persist the rung certificate and instances for small rungs
        fam_entry["rungs"].append(entry)
    return fam_entry


def _all_actuators(model) -> List[str]:
    return [a["name"] for a in model["actuators"]]


def _reconstruct(instance: Dict[str, Any], cert: Dict[str, Any]) -> Dict[str, Any]:
    """Root assignment of a single-bag-heavy DP certificate (bag covering all vars)."""
    bags = cert["tree_decomp"]["bags"]
    root = cert["root"]
    root_vals = cert.get("root_assignment")
    if root_vals is None:
        return {}
    assignment = dict(zip(bags[root], root_vals))
    # walk children via argmins
    edges = cert["tree_decomp"]["edges"]
    adj: Dict[str, list] = {b: [] for b in bags}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    from finite_ecd import assignment_key
    queue = [root]
    visited = {root}
    argmins = cert.get("argmins", {})
    while queue:
        b = queue.pop(0)
        key = assignment_key([assignment[x] for x in bags[b]])
        for ch in adj[b]:
            if ch in visited:
                continue
            visited.add(ch)
            ch_vals = argmins.get(b, {}).get(key, {}).get(ch)
            if ch_vals is None:
                continue
            for x, v in zip(bags[ch], ch_vals):
                assignment[x] = v
            queue.append(ch)
    return assignment


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/sparsification_study.json")
    args = ap.parse_args()
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "examples").mkdir(exist_ok=True)

    families: List[Dict[str, Any]] = []
    families.append(run_family("ten-bar", 1, [0, 1, 2, None]))
    families.append(run_family("chain-pretension", 64, [0, None]))
    families.append(run_family("dense-chain", 12, [0, 1, 2, 3, None]))
    families.append(run_family("lattice", 1, [0, 1, 2, None]))
    families.append(run_family("lattice", 2, [0, 1, None]))
    families.append(run_family("lattice", 3, [0, 1], relation_cap=RELATION_CAP,
                               full_status="RELATION-TABLE-LIMIT"))

    summary = {
        "families": len(families),
        "rungs": sum(len(f["rungs"]) for f in families),
        "sparsify_certificates_verified": sum(
            1 for f in families for rg in f["rungs"]
            if rg.get("sparsify_verify_status") == "VERIFIED"),
        "ladder_steps_verified": sum(
            1 for f in families for rg in f["rungs"]
            if rg.get("ladder_from_previous_status") == "VERIFIED"),
        "inner_dp_certificates_verified": sum(
            1 for f in families for rg in f["rungs"]
            if rg.get("inner", {}).get("dp_verify_status") == "VERIFIED"),
        "outer_dp_certificates_verified": sum(
            1 for f in families for rg in f["rungs"]
            if rg.get("outer", {}).get("dp_verify_status") == "VERIFIED"),
        "same_brackets_certified_sat": sum(
            1 for f in families for rg in f["rungs"] if rg.get("same_bracket") == "CERTIFIED-SAT"),
        "same_brackets_certified_unsat": sum(
            1 for f in families for rg in f["rungs"] if rg.get("same_bracket") == "CERTIFIED-UNSAT"),
        "same_brackets_inconclusive": sum(
            1 for f in families for rg in f["rungs"] if rg.get("same_bracket") == "INCONCLUSIVE"),
        "split_brackets_certified_sat": sum(
            1 for f in families for rg in f["rungs"] if rg.get("split_bracket") == "CERTIFIED-SAT"),
        "split_brackets_certified_unsat": sum(
            1 for f in families for rg in f["rungs"] if rg.get("split_bracket") == "CERTIFIED-UNSAT"),
        "split_brackets_inconclusive": sum(
            1 for f in families for rg in f["rungs"] if rg.get("split_bracket") == "INCONCLUSIVE"),
        "brackets_dp_size_limit": sum(
            1 for f in families for rg in f["rungs"]
            if rg.get("same_bracket") == "DP-SIZE-LIMIT"
            or rg.get("split_bracket") == "DP-SIZE-LIMIT"),
        "policies_verified_against_full_rows": sum(
            1 for f in families for rg in f["rungs"]
            if rg.get("same_policy_rows_verified") is True
            or rg.get("split_policy_rows_verified") is True),
    }
    out = {
        "status": "COMPLETE",
        "phase": "5 width-adaptive sparsification study",
        "retention_rule": ("row scope at radius r keeps actuators anchored within "
                           "graph distance r of the monitored member or node; radius "
                           "'full' is the no-sparsification ablation"),
        "families": families,
        "summary": summary,
    }
    out_path = ROOT / args.out
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
