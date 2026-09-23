#!/usr/bin/env python3
"""Prototype finite ECD verifier/solver.

This is deliberately small and dependency-free. It implements the first
certificate layer of the companion plan: explicit-table instances, policy
verification, brute-force solving for small instances, one-shot fibre conflict
certificates, and certificate verification.
"""
from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

Assignment = Dict[str, Any]


def freeze(v: Any) -> Any:
    """Recursively convert JSON lists into tuples for equality/hash keys."""
    if isinstance(v, list):
        return tuple(freeze(x) for x in v)
    if isinstance(v, dict):
        return tuple(sorted((k, freeze(x)) for k, x in v.items()))
    return v


@dataclass(frozen=True)
class Factor:
    name: str
    scope: Tuple[str, ...]
    relation: Tuple[Tuple[Any, ...], ...]

    @property
    def allowed(self) -> set[Tuple[Any, ...]]:
        try:
            return self._allowed_cache
        except AttributeError:
            cache = set(self.relation)
            object.__setattr__(self, "_allowed_cache", cache)
            return cache


@dataclass(frozen=True)
class Instance:
    variables: Tuple[str, ...]
    domains: Dict[str, Tuple[Any, ...]]
    factors: Tuple[Factor, ...]

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "Instance":
        variables = tuple(data["variables"])
        domains = {x: tuple(freeze(v) for v in data["domains"][x]) for x in variables}
        factors = []
        for f in data.get("factors", []):
            factors.append(Factor(
                name=f.get("name", f"factor_{len(factors)}"),
                scope=tuple(f["scope"]),
                relation=tuple(tuple(freeze(v) for v in row) for row in f["relation"]),
            ))
        return Instance(variables, domains, tuple(factors))

    def check_well_formed(self) -> List[str]:
        errors: List[str] = []
        if len(set(self.variables)) != len(self.variables):
            errors.append("duplicate variable name")
        for x in self.variables:
            if x not in self.domains:
                errors.append(f"missing domain for {x}")
            elif not self.domains[x]:
                errors.append(f"empty domain for {x}")
        for f in self.factors:
            for x in f.scope:
                if x not in self.domains:
                    errors.append(f"factor {f.name} mentions unknown variable {x}")
            for row in f.relation:
                if len(row) != len(f.scope):
                    errors.append(f"factor {f.name} has row of wrong arity {row}")
                    continue
                for x, v in zip(f.scope, row):
                    if x in self.domains and v not in self.domains[x]:
                        errors.append(f"factor {f.name} row {row} uses value {v!r} outside D_{x}")
        return errors


def verify_policy(instance: Instance, assignment: Assignment) -> Tuple[bool, List[str]]:
    errors = instance.check_well_formed()
    for x in instance.variables:
        if x not in assignment:
            errors.append(f"assignment missing {x}")
        else:
            assignment[x] = freeze(assignment[x])
            if assignment[x] not in instance.domains[x]:
                errors.append(f"assignment value {assignment[x]!r} outside D_{x}")
    for f in instance.factors:
        if any(x not in assignment for x in f.scope):
            continue
        row = tuple(assignment[x] for x in f.scope)
        if row not in f.allowed:
            errors.append(f"factor {f.name} rejects row {row}")
    return (not errors, errors)


def brute_force_solve(instance: Instance) -> Assignment | None:
    errors = instance.check_well_formed()
    if errors:
        raise ValueError("ill-formed instance: " + "; ".join(errors))
    domains = [instance.domains[x] for x in instance.variables]
    for values in itertools.product(*domains):
        a = dict(zip(instance.variables, values))
        ok, _ = verify_policy(instance, a)
        if ok:
            return a
    return None


def fibre_certificate(actions: List[Any], scenarios: List[Dict[str, Any]], obs_value: Any) -> Dict[str, Any] | None:
    """Return a small conflict certificate for one observation fibre if it fails.

    Each scenario has keys: observation, admissible (list of actions), and optional name.
    """
    fibre = [s for s in scenarios if s["observation"] == obs_value]
    if not fibre:
        return None
    frozen_actions = [freeze(a) for a in actions]
    common = set(frozen_actions)
    for s in fibre:
        common &= {freeze(a) for a in s["admissible"]}
    if common:
        return None
    witnesses = []
    for original_a, a in zip(actions, frozen_actions):
        for s in fibre:
            if a not in {freeze(x) for x in s["admissible"]}:
                witnesses.append({"action": original_a, "scenario": s.get("name", str(len(witnesses)))})
                break
    return {"type": "FIBRE-CONFLICT", "observation": obs_value, "witnesses": witnesses}


def verify_fibre_conflict(actions: List[Any], scenarios: List[Dict[str, Any]], cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if cert.get("type") != "FIBRE-CONFLICT":
        errors.append("wrong certificate type")
    obs = cert.get("observation")
    by_name = {s.get("name", str(i)): s for i, s in enumerate(scenarios)}
    frozen_actions = [freeze(a) for a in actions]
    excluded = set()
    for w in cert.get("witnesses", []):
        a = freeze(w.get("action"))
        name = w.get("scenario")
        s = by_name.get(name)
        if a not in frozen_actions:
            errors.append(f"unknown action {a!r}")
            continue
        if s is None:
            errors.append(f"unknown scenario {name!r}")
            continue
        if s.get("observation") != obs:
            errors.append(f"scenario {name!r} not in observation fibre {obs!r}")
            continue
        if a in {freeze(x) for x in s.get("admissible", [])}:
            errors.append(f"scenario {name!r} does not exclude action {a!r}")
            continue
        excluded.add(a)
    missing = set(frozen_actions) - excluded
    if missing:
        errors.append(f"actions not excluded: {sorted(missing)!r}")
    return (not errors, errors)



def sensor_repair(actions: List[Any], scenarios: List[Dict[str, Any]], sensors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Brute-force minimum sensor repair for tiny one-shot examples.

    A sensor is {"name": str, "values": {scenario_name: value}}.
    This enumerates sensor subsets, refines observations by selected sensor values,
    and checks all resulting fibres by intersection.
    """
    names = [s.get("name", str(i)) for i, s in enumerate(scenarios)]
    base_obs = {s.get("name", str(i)): s["observation"] for i, s in enumerate(scenarios)}
    admissible = {s.get("name", str(i)): {freeze(a) for a in s["admissible"]} for i, s in enumerate(scenarios)}
    frozen_actions = {freeze(a) for a in actions}

    def works(chosen: List[Dict[str, Any]]) -> Tuple[bool, Dict[Any, List[str]]]:
        fibres: Dict[Any, List[str]] = {}
        for name in names:
            key = (base_obs[name],) + tuple(sensor["values"][name] for sensor in chosen)
            fibres.setdefault(key, []).append(name)
        for fibre_names in fibres.values():
            common = set(frozen_actions)
            for name in fibre_names:
                common &= admissible[name]
            if not common:
                return False, fibres
        return True, fibres

    for r in range(len(sensors)+1):
        for idxs in itertools.combinations(range(len(sensors)), r):
            chosen = [sensors[i] for i in idxs]
            ok, fibres = works(chosen)
            if ok:
                return {
                    "type": "SENSOR-REPAIR",
                    "status": "CERTIFIED-OPT",
                    "selected": [s["name"] for s in chosen],
                    "size": r,
                    "fibres": {str(k): v for k, v in fibres.items()},
                    "optimality": "brute-force enumeration of smaller sensor subsets"
                }
    return {"type": "SENSOR-REPAIR", "status": "INCONCLUSIVE"}


def verify_sensor_repair(actions: List[Any], scenarios: List[Dict[str, Any]], sensors: List[Dict[str, Any]], cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Verifier for brute-force optimality certificates on tiny instances."""
    errors: List[str] = []
    selected_names = cert.get("selected", [])
    sensor_by_name = {s["name"]: s for s in sensors}
    if any(name not in sensor_by_name for name in selected_names):
        errors.append("certificate selects an unknown sensor")
        return False, errors
    recomputed = sensor_repair(actions, scenarios, sensors)
    if recomputed.get("status") != "CERTIFIED-OPT":
        errors.append("no optimum found by verifier")
        return False, errors
    if len(selected_names) != recomputed.get("size"):
        errors.append("selected set does not have optimum size")
    # Check selected set itself works, even if it differs from the verifier's lexicographic optimum.
    chosen = [sensor_by_name[name] for name in selected_names]
    names = [s.get("name", str(i)) for i, s in enumerate(scenarios)]
    frozen_actions = {freeze(a) for a in actions}
    for key in set((s["observation"],) + tuple(sensor["values"][s.get("name", str(i))] for sensor in chosen) for i, s in enumerate(scenarios)):
        common = set(frozen_actions)
        for i, scenario in enumerate(scenarios):
            name = scenario.get("name", str(i))
            k = (scenario["observation"],) + tuple(sensor["values"][name] for sensor in chosen)
            if k == key:
                common &= {freeze(a) for a in scenario["admissible"]}
        if not common:
            errors.append(f"selected sensors leave failing fibre {key!r}")
    return (not errors, errors)


INF = None  # JSON-level infinity for DP tables


def thaw_assignment(bag: List[str], values: List[Any]) -> Assignment:
    return {x: freeze(v) for x, v in zip(bag, values)}


def assignment_key(values: Iterable[Any]) -> str:
    return json.dumps(list(values), sort_keys=True)


def make_trivial_tree_decomp(instance: Instance) -> Dict[str, Any]:
    return {
        "type": "TREE-DECOMP",
        "root": "bag0",
        "bags": {"bag0": list(instance.variables)},
        "edges": [],
        "factor_to_bag": {f.name: "bag0" for f in instance.factors},
    }


def validate_tree_decomp(instance: Instance, decomp: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    bags = {name: tuple(xs) for name, xs in decomp.get("bags", {}).items()}
    if not bags:
        errors.append("tree decomposition has no bags")
        return False, errors
    root = decomp.get("root") or next(iter(bags))
    if root not in bags:
        errors.append("root bag is missing")
    for b, xs in bags.items():
        if len(set(xs)) != len(xs):
            errors.append(f"bag {b} has duplicate variables")
        for x in xs:
            if x not in instance.variables:
                errors.append(f"bag {b} mentions unknown variable {x}")
    edges = [tuple(e) for e in decomp.get("edges", [])]
    adj = {b: [] for b in bags}
    for e in edges:
        if len(e) != 2:
            errors.append(f"bad edge {e}")
            continue
        u, v = e
        if u not in bags or v not in bags:
            errors.append(f"edge {e} mentions unknown bag")
            continue
        adj[u].append(v); adj[v].append(u)
    if len(edges) != len(bags) - 1:
        errors.append("bag graph is not a tree: wrong number of edges")
    if bags:
        seen = set()
        stack = [root] if root in bags else [next(iter(bags))]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            stack.extend(v for v in adj.get(u, []) if v not in seen)
        if seen != set(bags):
            errors.append("bag graph is disconnected")
    factor_to_bag = dict(decomp.get("factor_to_bag", {}))
    for f in instance.factors:
        b = factor_to_bag.get(f.name)
        if b is None:
            candidates = [name for name, xs in bags.items() if set(f.scope) <= set(xs)]
            if not candidates:
                errors.append(f"factor {f.name} has no containing bag")
        elif b not in bags:
            errors.append(f"factor {f.name} assigned to unknown bag {b}")
        elif not set(f.scope) <= set(bags[b]):
            errors.append(f"factor {f.name} scope not contained in assigned bag {b}")
    # Running-intersection property for every variable.
    for x in instance.variables:
        containing = {b for b, xs in bags.items() if x in xs}
        if not containing:
            errors.append(f"variable {x} appears in no bag")
            continue
        start = next(iter(containing))
        seen = set(); stack = [start]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            for v in adj.get(u, []):
                if v in containing and v not in seen:
                    stack.append(v)
        if seen != containing:
            errors.append(f"bags containing variable {x} are not connected")
    return not errors, errors


def normalized_factor_assignment(instance: Instance, decomp: Dict[str, Any]) -> Dict[str, str]:
    bags = {name: tuple(xs) for name, xs in decomp.get("bags", {}).items()}
    f2b = dict(decomp.get("factor_to_bag", {}))
    for f in instance.factors:
        if f.name not in f2b:
            for b, xs in bags.items():
                if set(f.scope) <= set(xs):
                    f2b[f.name] = b
                    break
    return f2b


def parse_value_costs(raw: Dict[str, Any]) -> Dict[str, Dict[Any, int]]:
    out: Dict[str, Dict[Any, int]] = {}
    for x, entries in raw.get("value_costs", {}).items():
        out[x] = {}
        if isinstance(entries, list):
            for e in entries:
                out[x][freeze(e["value"])] = int(e["cost"])
        elif isinstance(entries, dict):
            for k, c in entries.items():
                # For scalar JSON values, keys arrive as strings; keep both string and parsed forms where possible.
                out[x][k] = int(c)
                try:
                    out[x][freeze(json.loads(k))] = int(c)
                except Exception:
                    pass
    return out


def bag_assignments(instance: Instance, bag: Tuple[str, ...]) -> List[Tuple[Any, ...]]:
    return list(itertools.product(*(instance.domains[x] for x in bag)))


def td_dynamic_program(instance: Instance, raw: Dict[str, Any], decomp: Dict[str, Any]) -> Dict[str, Any]:
    ok, errors = validate_tree_decomp(instance, decomp)
    if not ok:
        return {"type": "DP-ERROR", "status": "REJECTED", "errors": errors}
    bags = {name: tuple(xs) for name, xs in decomp["bags"].items()}
    root = decomp.get("root") or next(iter(bags))
    edges = [tuple(e) for e in decomp.get("edges", [])]
    adj = {b: [] for b in bags}
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    parent = {root: None}
    order = [root]
    for u in order:
        for v in adj[u]:
            if v not in parent:
                parent[v] = u
                order.append(v)
    postorder = list(reversed(order))
    f2b = normalized_factor_assignment(instance, decomp)
    factors_by_bag = {b: [] for b in bags}
    by_factor = {f.name: f for f in instance.factors}
    for fname, b in f2b.items():
        factors_by_bag[b].append(by_factor[fname])
    value_costs = parse_value_costs(raw)
    messages: Dict[str, Dict[str, Any]] = {}
    argmins: Dict[str, Dict[str, Dict[str, List[Any]]]] = {}
    for b in postorder:
        bag = bags[b]
        p = parent[b]
        parent_bag = bags[p] if p is not None else tuple()
        owned = [x for x in bag if x not in parent_bag]
        children = [v for v in adj[b] if parent.get(v) == b]
        # Separator-indexed child summaries: for every child, precompute the
        # best message value for each separator assignment once, instead of
        # re-enumerating the whole child bag for every assignment of this bag.
        child_summaries = {}
        for ch in children:
            ch_bag = bags[ch]
            sep = tuple(x for x in ch_bag if x in bag)
            ch_table = messages[ch]
            best_by_sep: Dict[Tuple[Any, ...], Any] = {}
            for ch_vals in bag_assignments(instance, ch_bag):
                v = ch_table[assignment_key(ch_vals)]
                if v is None:
                    continue
                ch_alpha = dict(zip(ch_bag, ch_vals))
                sep_vals = tuple(ch_alpha[x] for x in sep)
                cur = best_by_sep.get(sep_vals)
                if cur is None or v < cur[0]:
                    best_by_sep[sep_vals] = (v, list(ch_vals))
            child_summaries[ch] = (sep, best_by_sep)
        table: Dict[str, Any] = {}
        args_for_bag: Dict[str, Dict[str, List[Any]]] = {}
        bag_factors = [(f, f.scope) for f in factors_by_bag[b]]
        for vals in bag_assignments(instance, bag):
            alpha = dict(zip(bag, vals))
            feasible = True
            for f, fscope in bag_factors:
                row = tuple(alpha[x] for x in fscope)
                if row not in f.allowed:
                    feasible = False; break
            if not feasible:
                table[assignment_key(vals)] = None
                continue
            cost = 0
            for x in owned:
                cost += value_costs.get(x, {}).get(alpha[x], 0)
            child_choices: Dict[str, List[Any]] = {}
            for ch in children:
                sep, best_by_sep = child_summaries[ch]
                sep_vals = tuple(alpha[x] for x in sep)
                entry = best_by_sep.get(sep_vals)
                if entry is None:
                    feasible = False; break
                cost += entry[0]
                child_choices[ch] = entry[1]
            if feasible:
                table[assignment_key(vals)] = cost
                args_for_bag[assignment_key(vals)] = child_choices
            else:
                table[assignment_key(vals)] = None
        messages[b] = table
        argmins[b] = args_for_bag
    root_bag = bags[root]
    best = None; best_root_vals = None
    for vals in bag_assignments(instance, root_bag):
        v = messages[root][assignment_key(vals)]
        if v is not None and (best is None or v < best):
            best = v; best_root_vals = list(vals)
    cert_type = "DP-REFUTATION" if best is None else "DP-OPTIMUM"
    cert = {
        "type": cert_type,
        "status": "CERTIFIED-UNSAT" if best is None else "CERTIFIED-OPT",
        "tree_decomp": {
            "type": "TREE-DECOMP",
            "root": root,
            "bags": {b: list(xs) for b, xs in bags.items()},
            "edges": [list(e) for e in edges],
            "factor_to_bag": f2b,
        },
        "root": root,
        "optimum_cost": best,
        "root_assignment": best_root_vals,
        "messages": {
            b: {
                "bag": list(bags[b]),
                "table": [
                    {"assignment": list(vals), "cost": messages[b][assignment_key(vals)]}
                    for vals in bag_assignments(instance, bags[b])
                ],
            }
            for b in bags
        },
        "argmins": argmins,
    }
    return cert


def verify_dp_certificate(instance: Instance, raw: Dict[str, Any], cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if cert.get("type") not in {"DP-REFUTATION", "DP-OPTIMUM"}:
        errors.append("wrong DP certificate type")
        return False, errors
    decomp = cert.get("tree_decomp", {})
    ok, td_errors = validate_tree_decomp(instance, decomp)
    if not ok:
        return False, td_errors
    recomputed = td_dynamic_program(instance, raw, decomp)
    if recomputed.get("type") != cert.get("type"):
        errors.append(f"certificate type {cert.get('type')} disagrees with recomputed {recomputed.get('type')}")
    if recomputed.get("status") != cert.get("status"):
        errors.append("status disagrees with recomputation")
    if recomputed.get("optimum_cost") != cert.get("optimum_cost"):
        errors.append("optimum cost disagrees with recomputation")
    for b, msg in recomputed.get("messages", {}).items():
        given_msg = cert.get("messages", {}).get(b)
        if given_msg is None:
            errors.append(f"missing message table for bag {b}")
            continue
        given_table = {assignment_key(row["assignment"]): row.get("cost") for row in given_msg.get("table", [])}
        for row in msg["table"]:
            k = assignment_key(row["assignment"])
            if given_table.get(k, "MISSING") != row.get("cost"):
                errors.append(f"message mismatch at bag {b}, assignment {row['assignment']}")
                break
    return not errors, errors

def load_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_solve = sub.add_parser("solve")
    p_solve.add_argument("instance")
    p_verify = sub.add_parser("verify-policy")
    p_verify.add_argument("instance")
    p_verify.add_argument("certificate")
    p_fibre = sub.add_parser("fibre-conflict")
    p_fibre.add_argument("fibre_data")
    p_fibre.add_argument("observation")
    p_vfibre = sub.add_parser("verify-fibre")
    p_vfibre.add_argument("fibre_data")
    p_vfibre.add_argument("certificate")
    p_srepair = sub.add_parser("sensor-repair")
    p_srepair.add_argument("sensor_data")
    p_vsrepair = sub.add_parser("verify-sensor-repair")
    p_vsrepair.add_argument("sensor_data")
    p_vsrepair.add_argument("certificate")
    p_td = sub.add_parser("tree-decomp")
    p_td.add_argument("instance")
    p_vtd = sub.add_parser("verify-tree-decomp")
    p_vtd.add_argument("instance")
    p_vtd.add_argument("decomp")
    p_dps = sub.add_parser("td-solve")
    p_dps.add_argument("instance")
    p_dps.add_argument("--decomp", default=None)
    p_vdp = sub.add_parser("verify-dp")
    p_vdp.add_argument("instance")
    p_vdp.add_argument("certificate")
    args = parser.parse_args()

    if args.cmd == "solve":
        inst = Instance.from_json(load_json(args.instance))
        sol = brute_force_solve(inst)
        print(json.dumps({"status": "CERTIFIED-SAT" if sol else "CERTIFIED-UNSAT", "assignment": sol}, indent=2))
    elif args.cmd == "verify-policy":
        inst = Instance.from_json(load_json(args.instance))
        cert = load_json(args.certificate)
        ok, errors = verify_policy(inst, cert["assignment"])
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "fibre-conflict":
        data = load_json(args.fibre_data)
        cert = fibre_certificate(data["actions"], data["scenarios"], args.observation)
        print(json.dumps(cert or {"status": "NO-CONFLICT"}, indent=2))
    elif args.cmd == "verify-fibre":
        data = load_json(args.fibre_data)
        cert = load_json(args.certificate)
        ok, errors = verify_fibre_conflict(data["actions"], data["scenarios"], cert)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "sensor-repair":
        data = load_json(args.sensor_data)
        cert = sensor_repair(data["actions"], data["scenarios"], data["sensors"])
        print(json.dumps(cert, indent=2))
    elif args.cmd == "verify-sensor-repair":
        data = load_json(args.sensor_data)
        cert = load_json(args.certificate)
        ok, errors = verify_sensor_repair(data["actions"], data["scenarios"], data["sensors"], cert)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "tree-decomp":
        data = load_json(args.instance)
        inst = Instance.from_json(data)
        print(json.dumps(make_trivial_tree_decomp(inst), indent=2))
    elif args.cmd == "verify-tree-decomp":
        data = load_json(args.instance)
        inst = Instance.from_json(data)
        decomp = load_json(args.decomp)
        if "tree_decomp" in decomp:
            decomp = decomp["tree_decomp"]
        ok, errors = validate_tree_decomp(inst, decomp)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "td-solve":
        data = load_json(args.instance)
        inst = Instance.from_json(data)
        decomp = load_json(args.decomp) if args.decomp else make_trivial_tree_decomp(inst)
        if "tree_decomp" in decomp:
            decomp = decomp["tree_decomp"]
        print(json.dumps(td_dynamic_program(inst, data, decomp), indent=2))
    elif args.cmd == "verify-dp":
        data = load_json(args.instance)
        inst = Instance.from_json(data)
        cert = load_json(args.certificate)
        ok, errors = verify_dp_certificate(inst, data, cert)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))


if __name__ == "__main__":
    main()
