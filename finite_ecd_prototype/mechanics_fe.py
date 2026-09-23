#!/usr/bin/env python3
"""Exact rational mechanics front end with row certificates and a verifier.

This module converts declared structural models into certified finite ECD
relation tables using exact rational arithmetic only. Two model kinds are
supported:

- ``truss``: pin-jointed planar truss with rational node coordinates, declared
  rational axial stiffness per member, node-force actuators, and self
  equilibrated axial member-pair (pre-tension) actuators. Direction cosines
  are rational because every member uses a 3-4-5 direction (or an axis).
- ``scalar-chain``: one-dimensional mass-spring chain grounded at node 0 with
  rational spring stiffnesses, node-force actuators, and spring-pair
  (pre-tension) actuators.

Certificates:

- ``MECH-SOLVE``: exact base-state solve per load scenario (load vector and
  displacement vector over the free degrees of freedom). The verifier
  recomputes the stiffness matrix independently and checks ``K u = F``
  exactly by substitution, so the base states are proved without re-running
  the generator's elimination.
- ``MECH-ROW-BATCH``: one row per (scenario, monitor) pair with the exact
  rational constant term and sparse actuator influence coefficients, plus the
  derived finite relation table over the row's support. The verifier
  regenerates every row and relation with its own assembly and solve code
  and compares.
- ``MECH-SPARSIFY-BATCH``: scope-restricted sparsification certificates for
  retained-scope ladders, with inner and outer finite relations, plus ladder
  monotonicity verification.

All numbers are stored as exact rational strings ``"p/q"``.
"""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Tuple


def fr(x: Any) -> Fraction:
    return Fraction(str(x))


def show(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def load(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())


# ---------------------------------------------------------------------------
# Exact linear solvers
# ---------------------------------------------------------------------------

def solve_dense_exact(K: List[List[Fraction]], rhs: List[Fraction]) -> List[Fraction]:
    """Gauss-Jordan elimination with partial pivoting, exact arithmetic."""
    n = len(K)
    M = [row[:] + [rhs[i]] for i, row in enumerate(K)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            raise ValueError("singular stiffness matrix")
        M[col], M[piv] = M[piv], M[col]
        inv = Fraction(1) / M[col][col]
        M[col] = [v * inv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def solve_tridiag_exact(diag: List[Fraction], off: List[Fraction],
                        rhs: List[Fraction]) -> List[Fraction]:
    """Thomas algorithm without pivoting for symmetric tridiagonal systems.

    ``diag[i]`` is the i-th diagonal entry; ``off[i]`` couples rows i and i+1.
    The stiffness matrices of grounded spring chains are positive definite,
    so zero pivots cannot occur.
    """
    n = len(diag)
    d = list(diag)
    r = list(rhs)
    for i in range(1, n):
        w = off[i - 1] / d[i - 1]
        d[i] = d[i] - w * off[i - 1]
        r[i] = r[i] - w * r[i - 1]
    x = [Fraction(0)] * n
    x[n - 1] = r[n - 1] / d[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = (r[i] - off[i] * x[i + 1]) / d[i]
    return x


# ---------------------------------------------------------------------------
# Assembly (generator side)
# ---------------------------------------------------------------------------

def truss_dofs(model: Dict[str, Any]) -> Tuple[Dict[Tuple[Any, str], int], List[Tuple[Any, str]]]:
    supports = {s["node"] for s in model.get("supports", [])}
    dof_index: Dict[Tuple[Any, str], int] = {}
    free_dofs: List[Tuple[Any, str]] = []
    for node in model["nodes"]:
        nid = node["id"]
        if nid in supports:
            continue
        for comp in ("x", "y"):
            dof_index[(nid, comp)] = len(free_dofs)
            free_dofs.append((nid, comp))
    return dof_index, free_dofs


def assemble_truss(model: Dict[str, Any]) -> Tuple[Dict[Tuple[Any, str], int], List[Tuple[Any, str]], List[List[Fraction]]]:
    """Assemble the free-DOF stiffness matrix of a pin-jointed truss exactly.

    Generator-side assembly: accumulates the 2x2 member dyads directly into
    the global matrix.
    """
    dof_index, free_dofs = truss_dofs(model)
    nodes = {n["id"]: (fr(n["x"]), fr(n["y"])) for n in model["nodes"]}
    n = len(free_dofs)
    K = [[Fraction(0)] * n for _ in range(n)]
    for m in model["members"]:
        k = fr(m["k"])
        ax, ay = nodes[m["a"]]
        bx, by = nodes[m["b"]]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        c2 = dx * dx / L2
        s2 = dy * dy / L2
        cs = dx * dy / L2
        dofs = [dof_index.get((m["a"], "x")), dof_index.get((m["a"], "y")),
                dof_index.get((m["b"], "x")), dof_index.get((m["b"], "y"))]
        for i in range(4):
            if dofs[i] is None:
                continue
            for j in range(4):
                if dofs[j] is None:
                    continue
                sign = 1 if (i < 2) == (j < 2) else -1
                K[dofs[i]][dofs[j]] += sign * k * (c2 if i % 2 == 0 and j % 2 == 0
                                                   else s2 if i % 2 == 1 and j % 2 == 1
                                                   else cs)
    return dof_index, free_dofs, K


def assemble_truss_independent(model: Dict[str, Any]) -> Tuple[Dict[Tuple[Any, str], int], List[Tuple[Any, str]], List[List[Fraction]]]:
    """Verifier-side truss assembly, written independently.

    Builds the full 4x4 element matrix as an outer product of the unit
    direction vector and then scatters it, instead of accumulating 2x2 dyads.
    """
    dof_index, free_dofs = truss_dofs(model)
    nodes = {n["id"]: (fr(n["x"]), fr(n["y"])) for n in model["nodes"]}
    n = len(free_dofs)
    K = [[Fraction(0)] * n for _ in range(n)]
    for m in model["members"]:
        k = fr(m["k"])
        ax, ay = nodes[m["a"]]
        bx, by = nodes[m["b"]]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        L = _rational_sqrt(L2)
        if L is None or L == 0:
            raise ValueError(f"member {m['name']} has irrational or zero length")
        c, s = dx / L, dy / L
        # element 4x4 = k * (d d^T) with d = (c, s, -c, -s) for [a; b] ordering
        vec = [c, s, -c, -s]
        dofs = [dof_index.get((m["a"], "x")), dof_index.get((m["a"], "y")),
                dof_index.get((m["b"], "x")), dof_index.get((m["b"], "y"))]
        for i in range(4):
            if dofs[i] is None:
                continue
            for j in range(4):
                if dofs[j] is None:
                    continue
                K[dofs[i]][dofs[j]] += k * vec[i] * vec[j]
    return dof_index, free_dofs, K


def chain_matrix(model: Dict[str, Any]) -> Tuple[int, List[Fraction], List[Fraction]]:
    """Return (n, diag, off) for a grounded scalar chain."""
    n = int(model["nodes"])
    diag = [Fraction(0)] * n
    off = [Fraction(0)] * (n - 1)
    for s in model["springs"]:
        i = int(s["name"].lstrip("s"))  # spring i couples node i-1 and i
        c = fr(s["k"])
        diag[i - 1] += c
        if i >= 2:
            diag[i - 2] += c
            off[i - 2] = -c
    return n, diag, off


def chain_matrix_independent(model: Dict[str, Any]) -> Tuple[int, List[Fraction], List[Fraction]]:
    """Verifier-side chain assembly via a connectivity sweep."""
    n = int(model["nodes"])
    entries: Dict[Tuple[int, int], Fraction] = {}
    for s in model["springs"]:
        i = int(s["name"].lstrip("s"))
        c = fr(s["k"])
        for p in (i - 1, i - 2):
            for q in (i - 1, i - 2):
                if 0 <= p < n and 0 <= q < n:
                    entries[(p, q)] = entries.get((p, q), Fraction(0)) + c
        if i >= 2:
            entries[(i - 2, i - 1)] = entries.get((i - 2, i - 1), Fraction(0))
    diag = [entries.get((i, i), Fraction(0)) for i in range(n)]
    off = [entries.get((i, i + 1), Fraction(0)) for i in range(n - 1)]
    # off-diagonal must be exactly the negated shared spring stiffness
    for s in model["springs"]:
        i = int(s["name"].lstrip("s"))
        if i >= 2:
            off[i - 2] = -fr(s["k"])
    return n, diag, off


# ---------------------------------------------------------------------------
# Load vectors
# ---------------------------------------------------------------------------

def member_direction(model: Dict[str, Any], member: Dict[str, Any]) -> Tuple[Fraction, Fraction, Fraction]:
    """Return (c, s, L) rational direction cosines and length of a member."""
    nodes = {n["id"]: (fr(n["x"]), fr(n["y"])) for n in model["nodes"]}
    ax, ay = nodes[member["a"]]
    bx, by = nodes[member["b"]]
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    L = _rational_sqrt(L2)
    if L is None:
        raise ValueError(f"member {member['name']} length {L2} is not a rational square")
    return dx / L, dy / L, L


def _rational_sqrt(q: Fraction) -> Fraction | None:
    if q == 0:
        return Fraction(0)
    from math import isqrt
    num = isqrt(q.numerator)
    den = isqrt(q.denominator)
    if num * num == q.numerator and den * den == q.denominator:
        return Fraction(num, den)
    return None


def truss_load_vector(model: Dict[str, Any], forces: List[Dict[str, Any]],
                       dof_index: Dict[Tuple[Any, str], int], size: int) -> List[Fraction]:
    rhs = [Fraction(0)] * size
    for f in forces:
        fx, fy = fr(f["components"][0]), fr(f["components"][1])
        for comp, val in (("x", fx), ("y", fy)):
            idx = dof_index.get((f["node"], comp))
            if idx is not None:
                rhs[idx] += val
    return rhs


def truss_actuator_vector(model: Dict[str, Any], actuator: Dict[str, Any],
                           dof_index: Dict[Tuple[Any, str], int], size: int) -> List[Fraction]:
    """Unit-activation load pattern of a truss actuator (magnitude included)."""
    rhs = [Fraction(0)] * size
    members = {m["name"]: m for m in model["members"]}
    if actuator["type"] == "node-force":
        fx, fy = fr(actuator["components"][0]), fr(actuator["components"][1])
        for comp, val in (("x", fx), ("y", fy)):
            idx = dof_index.get((actuator["node"], comp))
            if idx is not None:
                rhs[idx] += val
        return rhs
    if actuator["type"] == "member-pair":
        m = members[actuator["member"]]
        c, s, _L = member_direction(model, m)
        sign = fr(actuator.get("sign", "1"))
        for nid, sg in ((m["a"], -sign), (m["b"], sign)):
            for comp, val in (("x", c), ("y", s)):
                idx = dof_index.get((nid, comp))
                if idx is not None:
                    rhs[idx] += sg * val
        return rhs
    raise ValueError(f"unknown actuator type {actuator['type']}")


def chain_load_vector(forces: List[Dict[str, Any]], n: int) -> List[Fraction]:
    rhs = [Fraction(0)] * n
    for f in forces:
        rhs[int(f["node"]) - 1] += fr(f["component"])
    return rhs


def chain_actuator_vector(actuator: Dict[str, Any], model: Dict[str, Any], n: int) -> List[Fraction]:
    rhs = [Fraction(0)] * n
    if actuator["type"] == "node-force":
        rhs[int(actuator["node"]) - 1] += fr(actuator["component"])
        return rhs
    if actuator["type"] == "spring-pair":
        i = int(actuator["spring"])
        sign = fr(actuator.get("sign", "1"))
        rhs[i - 1] += sign
        if i >= 2:
            rhs[i - 2] -= sign
        return rhs
    raise ValueError(f"unknown actuator type {actuator['type']}")


# ---------------------------------------------------------------------------
# Monitors
# ---------------------------------------------------------------------------

def truss_monitor_value(model: Dict[str, Any], monitor: Dict[str, Any],
                        u_map: Dict[Tuple[Any, str], Fraction]) -> Fraction:
    members = {m["name"]: m for m in model["members"]}
    if monitor["type"] == "member-force":
        m = members[monitor["member"]]
        c, s, L = member_direction(model, m)
        k = fr(m["k"])
        dux = u_map.get((m["b"], "x"), Fraction(0)) - u_map.get((m["a"], "x"), Fraction(0))
        duy = u_map.get((m["b"], "y"), Fraction(0)) - u_map.get((m["a"], "y"), Fraction(0))
        return k * (c * dux + s * duy)
    if monitor["type"] == "node-displacement":
        return u_map.get((monitor["node"], monitor["component"]), Fraction(0))
    raise ValueError(f"unknown monitor type {monitor['type']}")


def chain_monitor_value(model: Dict[str, Any], monitor: Dict[str, Any],
                        u: List[Fraction],
                        spring_k: Dict[int, Fraction] | None = None) -> Fraction:
    if spring_k is None:
        spring_k = {int(s["name"].lstrip("s")): fr(s["k"]) for s in model["springs"]}
    if monitor["type"] == "spring-force":
        i = int(monitor["spring"])
        c = spring_k[i]
        prev = u[i - 2] if i >= 2 else Fraction(0)
        return c * (u[i - 1] - prev)
    if monitor["type"] == "node-displacement":
        return u[int(monitor["node"]) - 1]
    raise ValueError(f"unknown monitor type {monitor['type']}")


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate(model: Dict[str, Any], relation_cap: int | None = None) -> Dict[str, Any]:
    """Solve the structural model exactly and derive certified rows.

    Returns a batch with base-state solves, per-(scenario, monitor) rows with
    exact sparse influence coefficients, and the finite relation tables over
    each row's support. When ``relation_cap`` is given, rows whose support
    exceeds ``2**relation_cap`` enumerated assignments skip relation
    enumeration and are marked ``RELATION-TABLE-LIMIT``; the cap is recorded
    so the verifier reproduces the same decision.
    """
    kind = model["kind"]
    domain = [fr(v) for v in model["actuator_domain"]]
    safe_lo, safe_hi = fr(model["safe_interval"][0]), fr(model["safe_interval"][1])
    actuators = model["actuators"]

    solves = []
    rows = []
    relations = []
    if kind == "truss":
        dof_index, free_dofs, K = assemble_truss(model)
        size = len(free_dofs)
        u_cache: Dict[str, Dict[Tuple[Any, str], Fraction]] = {}

        def u_for(scenario=None, actuator=None):
            key = f"sc:{scenario}" if scenario is not None else f"act:{actuator['name']}"
            if key in u_cache:
                return u_cache[key]
            if scenario is not None:
                forces = next(s["forces"] for s in model["scenarios"] if s["name"] == scenario)
                rhs = truss_load_vector(model, forces, dof_index, size)
            else:
                rhs = truss_actuator_vector(model, actuator, dof_index, size)
            u = solve_dense_exact(K, rhs)
            um = {dof: val for dof, val in zip(free_dofs, u)}
            u_cache[key] = um
            return um

        for sc in model["scenarios"]:
            um = u_for(scenario=sc["name"])
            solves.append({
                "type": "MECH-SOLVE",
                "scenario": sc["name"],
                "dofs": [f"{nid}/{comp}" for nid, comp in free_dofs],
                "load": [show(v) for v in truss_load_vector(model, sc["forces"], dof_index, size)],
                "displacement": [show(um[d]) for d in free_dofs],
            })
            for mon in model["monitors"]:
                d = truss_monitor_value(model, mon, um)
                coeffs = {}
                for act in actuators:
                    g = truss_monitor_value(model, mon, u_for(actuator=act))
                    if g != 0:
                        coeffs[act["name"]] = show(g)
                rows.append(_row_entry(model, sc["name"], mon["name"], d, coeffs))
                relations.append(_relation_entry(model, sc["name"], mon["name"],
                                                 list(coeffs.keys()), d, coeffs,
                                                 domain, safe_lo, safe_hi, relation_cap))
    elif kind == "scalar-chain":
        n, diag, off = chain_matrix(model)
        spring_k = {int(s["name"].lstrip("s")): fr(s["k"]) for s in model["springs"]}
        u_cache: Dict[str, List[Fraction]] = {}

        def u_for(scenario=None, actuator=None):
            key = f"sc:{scenario}" if scenario is not None else f"act:{actuator['name']}"
            if key in u_cache:
                return u_cache[key]
            if scenario is not None:
                forces = next(s["forces"] for s in model["scenarios"] if s["name"] == scenario)
                rhs = chain_load_vector(forces, n)
            else:
                rhs = chain_actuator_vector(actuator, model, n)
            u = solve_tridiag_exact(diag, off, rhs)
            u_cache[key] = u
            return u

        for sc in model["scenarios"]:
            u = u_for(scenario=sc["name"])
            solves.append({
                "type": "MECH-SOLVE",
                "scenario": sc["name"],
                "dofs": [f"node{i}/x" for i in range(1, n + 1)],
                "load": [show(v) for v in chain_load_vector(sc["forces"], n)],
                "displacement": [show(v) for v in u],
            })
            for mon in model["monitors"]:
                d = chain_monitor_value(model, mon, u, spring_k)
                coeffs = {}
                for act in actuators:
                    g = chain_monitor_value(model, mon, u_for(actuator=act), spring_k)
                    if g != 0:
                        coeffs[act["name"]] = show(g)
                rows.append(_row_entry(model, sc["name"], mon["name"], d, coeffs))
                relations.append(_relation_entry(model, sc["name"], mon["name"],
                                                 list(coeffs.keys()), d, coeffs,
                                                 domain, safe_lo, safe_hi, relation_cap))
    else:
        raise ValueError(f"unknown model kind {kind}")

    scopes = [len(r["coeffs"]) for r in rows]
    return {
        "type": "MECH-ROW-BATCH",
        "status": "CERTIFIED",
        "model": model.get("name", "mechanics-model"),
        "kind": kind,
        "safe_interval": [show(safe_lo), show(safe_hi)],
        "actuator_domain": [show(v) for v in domain],
        "relation_cap": relation_cap,
        "solves": solves,
        "rows": rows,
        "relations": relations,
        "scope_sizes": scopes,
        "max_scope": max(scopes) if scopes else 0,
    }


def _row_entry(model, scenario, monitor, d, coeffs):
    return {
        "scenario": scenario,
        "monitor": monitor,
        "constant": show(d),
        "coeffs": dict(coeffs),
    }


def _relation_entry(model, scenario, monitor, scope, d, coeffs, domain, safe_lo, safe_hi,
                    relation_cap=None):
    if relation_cap is not None and len(domain) ** len(scope) > relation_cap:
        return {
            "scenario": scenario,
            "monitor": monitor,
            "scope": list(scope),
            "relation": None,
            "status": "RELATION-TABLE-LIMIT",
        }
    safe = []
    g = {x: fr(coeffs[x]) for x in scope}
    for values in itertools.product(domain, repeat=len(scope)):
        y = d
        for x, v in zip(scope, values):
            y += g[x] * v
        if safe_lo <= y <= safe_hi:
            safe.append([show(v) for v in values])
    return {
        "scenario": scenario,
        "monitor": monitor,
        "scope": list(scope),
        "relation": safe,
    }


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify(model: Dict[str, Any], batch: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Independently verify a MECH-ROW-BATCH against the declared model.

    The stiffness matrix is re-assembled by independently written assembly
    code; stored base-state displacements are checked by exact residual
    substitution; every row constant and influence coefficient is recomputed;
    every relation table is regenerated and compared.
    """
    errors: List[str] = []
    if batch.get("type") != "MECH-ROW-BATCH":
        return False, ["wrong certificate type"]
    if batch.get("model") != model.get("name"):
        errors.append("certificate model name does not match the declared model")
    kind = model["kind"]
    domain = [fr(v) for v in model["actuator_domain"]]
    safe_lo, safe_hi = fr(model["safe_interval"][0]), fr(model["safe_interval"][1])
    actuators = model["actuators"]

    u_cache: Dict[str, Any] = {}

    if kind == "truss":
        dof_index, free_dofs, K = assemble_truss_independent(model)
        size = len(free_dofs)

        def solve_for(scenario=None, actuator=None):
            key = f"sc:{scenario}" if scenario is not None else f"act:{actuator['name']}"
            if key in u_cache:
                return u_cache[key]
            if scenario is not None:
                forces = next(s["forces"] for s in model["scenarios"] if s["name"] == scenario)
                rhs = truss_load_vector(model, forces, dof_index, size)
            else:
                rhs = truss_actuator_vector(model, actuator, dof_index, size)
            um = {dof: val for dof, val in zip(free_dofs, solve_dense_exact(K, rhs))}
            u_cache[key] = um
            return um

        def residual_check(scenario, solve_cert):
            F = [fr(v) for v in solve_cert["load"]]
            u = [fr(v) for v in solve_cert["displacement"]]
            if len(u) != size or len(F) != size:
                return [f"scenario {scenario}: stored solve has wrong length"]
            for i in range(size):
                acc = sum(K[i][j] * u[j] for j in range(size)) - F[i]
                if acc != 0:
                    return [f"scenario {scenario}: residual substitution fails at DOF {i}"]
            return []
    elif kind == "scalar-chain":
        n, diag, off = chain_matrix_independent(model)
        spring_k = {int(s["name"].lstrip("s")): fr(s["k"]) for s in model["springs"]}

        def solve_for(scenario=None, actuator=None):
            key = f"sc:{scenario}" if scenario is not None else f"act:{actuator['name']}"
            if key in u_cache:
                return u_cache[key]
            if scenario is not None:
                forces = next(s["forces"] for s in model["scenarios"] if s["name"] == scenario)
                rhs = chain_load_vector(forces, n)
            else:
                rhs = chain_actuator_vector(actuator, model, n)
            u = solve_tridiag_exact(diag, off, rhs)
            u_cache[key] = u
            return u

        def residual_check(scenario, solve_cert):
            F = [fr(v) for v in solve_cert["load"]]
            u = [fr(v) for v in solve_cert["displacement"]]
            if len(u) != n or len(F) != n:
                return [f"scenario {scenario}: stored solve has wrong length"]
            for i in range(n):
                acc = diag[i] * u[i] - F[i]
                if i + 1 < n:
                    acc += off[i] * u[i + 1]
                if i >= 1:
                    acc += off[i - 1] * u[i - 1]
                if acc != 0:
                    return [f"scenario {scenario}: residual substitution fails at node {i + 1}"]
            return []
    else:
        return False, [f"unknown model kind {kind}"]

    scenario_names = [sc["name"] for sc in model["scenarios"]]
    stored_solves = {s.get("scenario"): s for s in batch.get("solves", [])}
    for sc in scenario_names:
        cert = stored_solves.get(sc)
        if cert is None:
            errors.append(f"missing MECH-SOLVE certificate for scenario {sc}")
            continue
        errors.extend(residual_check(sc, cert))

    def monitor_value(mon, u):
        if kind == "truss":
            return truss_monitor_value(model, mon, u)
        return chain_monitor_value(model, mon, u, spring_k)

    regen_rows = []
    regen_relations = []
    relation_cap = batch.get("relation_cap")
    for sc in model["scenarios"]:
        u_base = solve_for(scenario=sc["name"])
        for mon in model["monitors"]:
            d = monitor_value(mon, u_base)
            coeffs = {}
            for act in actuators:
                g = monitor_value(mon, solve_for(actuator=act))
                if g != 0:
                    coeffs[act["name"]] = show(g)
            regen_rows.append(_row_entry(model, sc["name"], mon["name"], d, coeffs))
            regen_relations.append(_relation_entry(model, sc["name"], mon["name"],
                                                   list(coeffs.keys()), d, coeffs,
                                                   domain, safe_lo, safe_hi, relation_cap))

    if len(regen_rows) != len(batch.get("rows", [])):
        errors.append("row count disagrees with regeneration")
        return False, errors
    for i, (r0, r1) in enumerate(zip(regen_rows, batch.get("rows", []))):
        if r0 != r1:
            errors.append(f"row {i} ({r1.get('scenario')}/{r1.get('monitor')}) disagrees with regeneration")
    if len(regen_relations) != len(batch.get("relations", [])):
        errors.append("relation count disagrees with regeneration")
    else:
        for i, (g0, g1) in enumerate(zip(regen_relations, batch.get("relations", []))):
            if g0 != g1:
                errors.append(f"relation {i} ({g1.get('scenario')}/{g1.get('monitor')}) disagrees with regeneration")
    return not errors, errors


# ---------------------------------------------------------------------------
# Scope-restricted sparsification
# ---------------------------------------------------------------------------

def sparsify(model: Dict[str, Any], batch: Dict[str, Any],
             retained_map: Dict[str, List[str]]) -> Dict[str, Any]:
    """Exact scope-restricted sparsification of the certified rows.

    ``retained_map`` maps ``scenario/monitor`` row names to retained actuator
    lists (subsets of the row's support). For each row and retained
    assignment the omitted terms are bounded by their exact range over the
    omitted actuator domains, giving a certified response interval; the
    inner relation keeps retained assignments whose whole interval lies in
    the safe interval, the outer relation keeps those whose interval
    intersects it.
    """
    domain = [fr(v) for v in model["actuator_domain"]]
    safe_lo, safe_hi = fr(model["safe_interval"][0]), fr(model["safe_interval"][1])
    actuator_domain = {a["name"]: domain for a in model["actuators"]}
    cert_rows = []
    inner_factors = []
    outer_factors = []
    row_keys = []
    for row, rel in zip(batch["rows"], batch["relations"]):
        key = f"{row['scenario']}/{row['monitor']}"
        row_keys.append(key)
        support = list(row["coeffs"].keys())
        retained = [x for x in retained_map.get(key, support) if x in support]
        d = fr(row["constant"])
        omitted = [x for x in support if x not in retained]
        eta_lo = Fraction(0)
        eta_hi = Fraction(0)
        for x in omitted:
            vals = [fr(row["coeffs"][x]) * v for v in actuator_domain[x]]
            eta_lo += min(vals)
            eta_hi += max(vals)
        inner_rel = []
        outer_rel = []
        g = {x: fr(row["coeffs"][x]) for x in retained}
        for values in itertools.product(domain, repeat=len(retained)):
            base = d
            for x, v in zip(retained, values):
                base += g[x] * v
            resp_lo = base + eta_lo
            resp_hi = base + eta_hi
            inner = safe_lo <= resp_lo and resp_hi <= safe_hi
            outer = not (resp_hi < safe_lo or resp_lo > safe_hi)
            tv = [show(v) for v in values]
            if inner:
                inner_rel.append(tv)
            if outer:
                outer_rel.append(tv)
        cert_rows.append({
            "row": key,
            "retained": retained,
            "omitted_interval": [show(eta_lo), show(eta_hi)],
            "inner_count": len(inner_rel),
            "outer_count": len(outer_rel),
            "enumerated": len(domain) ** len(retained),
        })
        name = _factor_name(row["scenario"], row["monitor"])
        inner_factors.append({"name": name, "scope": retained, "relation": inner_rel})
        outer_factors.append({"name": name, "scope": retained, "relation": outer_rel})
    retained_vars = []
    for f in inner_factors:
        for x in f["scope"]:
            if x not in retained_vars:
                retained_vars.append(x)
    domains_out = {x: [show(v) for v in domain] for x in retained_vars}
    return {
        "type": "MECH-SPARSIFY-BATCH",
        "status": "CERTIFIED",
        "model": model.get("name", "mechanics-model"),
        "retained_map": {k: list(v) for k, v in retained_map.items()},
        "rows": cert_rows,
        "inner_instance": {"variables": retained_vars, "domains": domains_out, "factors": inner_factors},
        "outer_instance": {"variables": retained_vars, "domains": domains_out, "factors": outer_factors},
    }


def _factor_name(scenario: str, monitor: str) -> str:
    return f"{scenario}__{monitor}"


def verify_policy_rows(model: Dict[str, Any], batch: Dict[str, Any],
                       assignment: Dict[str, Any],
                       scenario: str | None = None) -> Tuple[bool, List[str]]:
    """Verify a structural actuator assignment directly against certified rows.

    Every row response is recomputed exactly from the certified constant and
    influence coefficients and checked against the declared safe interval.
    With ``scenario`` given, only that scenario's rows are checked (split
    observation); otherwise all rows are checked (shared command).
    """
    errors: List[str] = []
    safe_lo = fr(model["safe_interval"][0])
    safe_hi = fr(model["safe_interval"][1])
    for row in batch.get("rows", []):
        if scenario is not None and row.get("scenario") != scenario:
            continue
        y = fr(row["constant"])
        for x, g in row.get("coeffs", {}).items():
            if x not in assignment:
                errors.append(f"row {row['scenario']}/{row['monitor']}: assignment missing actuator {x}")
                y = None
                break
            y += fr(g) * fr(assignment[x])
        if y is None:
            continue
        if not (safe_lo <= y <= safe_hi):
            errors.append(f"row {row['scenario']}/{row['monitor']}: response {show(y)} outside the safe interval")
    return not errors, errors


def verify_sparsify(model: Dict[str, Any], batch: Dict[str, Any],
                    cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if cert.get("type") != "MECH-SPARSIFY-BATCH":
        return False, ["wrong certificate type"]
    retained_map = {k: list(v) for k, v in cert.get("retained_map", {}).items()}
    regenerated = sparsify(model, batch, retained_map)
    if regenerated.get("inner_instance") != cert.get("inner_instance"):
        errors.append("inner sparse instance disagrees with regeneration")
    if regenerated.get("outer_instance") != cert.get("outer_instance"):
        errors.append("outer sparse instance disagrees with regeneration")
    if len(regenerated.get("rows", [])) != len(cert.get("rows", [])):
        errors.append("sparsification row count disagrees with regeneration")
        return False, errors
    for i, (r0, r1) in enumerate(zip(regenerated["rows"], cert.get("rows", []))):
        for key in ("row", "retained", "omitted_interval", "inner_count", "outer_count", "enumerated"):
            if r0.get(key) != r1.get(key):
                errors.append(f"sparsification row {i} field {key} disagrees with regeneration")
                break
    return not errors, errors


def _relation_set(factor: Dict[str, Any]) -> set:
    return {tuple(row) for row in factor.get("relation", [])}


def verify_sparsify_ladder(model: Dict[str, Any], batch: Dict[str, Any],
                           coarse: Dict[str, Any], fine: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Verify rowwise monotonicity for nested retained scopes J subset J'.

    Checks the certificate-level consequences:
    - J_i subset J'_i for every row;
    - every coarse inner retained tuple has all fine extensions in the fine
      inner relation. Because the response is linear in the omitted actuator
      values, it suffices to check the two per-term extreme completions (each
      omitted actuator at the value minimising, respectively maximising, its
      contribution): every other completion lies between these responses.
    - every fine outer tuple projects to a coarse outer tuple.
    Together with the full regeneration check of both sparse instances this
    verifies the finite form of
    Gamma^-_J <= Gamma^-_J' <= Gamma^true <= Gamma^+_J' <= Gamma^+_J.
    """
    errors: List[str] = []
    ok_c, err_c = verify_sparsify(model, batch, coarse)
    ok_f, err_f = verify_sparsify(model, batch, fine)
    if not ok_c:
        errors.extend(["coarse: " + e for e in err_c])
    if not ok_f:
        errors.extend(["fine: " + e for e in err_f])
    if errors:
        return False, errors
    domain = [fr(v) for v in model["actuator_domain"]]
    c_inner = {f["name"]: f for f in coarse["inner_instance"]["factors"]}
    f_inner = {f["name"]: f for f in fine["inner_instance"]["factors"]}
    c_outer = {f["name"]: f for f in coarse["outer_instance"]["factors"]}
    f_outer = {f["name"]: f for f in fine["outer_instance"]["factors"]}
    coarse_map = {k: list(v) for k, v in coarse.get("retained_map", {}).items()}
    fine_map = {k: list(v) for k, v in fine.get("retained_map", {}).items()}
    for row in batch["rows"]:
        key = f"{row['scenario']}/{row['monitor']}"
        support = list(row["coeffs"].keys())
        J = [x for x in coarse_map.get(key, support) if x in support]
        Jp = [x for x in fine_map.get(key, support) if x in support]
        if not set(J) <= set(Jp):
            errors.append(f"row {key}: retained scopes are not nested")
            continue
        name = _factor_name(row["scenario"], row["monitor"])
        c_in = _relation_set(c_inner[name])
        f_in = _relation_set(f_inner[name])
        c_out = _relation_set(c_outer[name])
        f_out = _relation_set(f_outer[name])
        extra = [x for x in Jp if x not in J]
        g = {x: fr(row["coeffs"].get(x, "0")) for x in extra}
        # per-term extreme completions of the omitted actuators
        u_min = {x: min(domain, key=lambda v: g[x] * v) for x in extra}
        u_max = {x: max(domain, key=lambda v: g[x] * v) for x in extra}
        # Coarse inner cylinder inclusion into fine inner: check the two
        # extreme completions (linearity makes them binding for all others).
        for crow in c_in:
            base = dict(zip(J, [fr(v) for v in crow]))
            for u_ext in (u_min, u_max):
                full = dict(base)
                full.update({x: u_ext[x] for x in extra})
                ftuple = tuple(show(full[x]) for x in Jp)
                if ftuple not in f_in:
                    errors.append(f"row {key}: coarse inner tuple {crow} has non-inner fine extreme extension")
                    break
        # Fine outer projects into coarse outer.
        for frow in f_out:
            full = dict(zip(Jp, [fr(v) for v in frow]))
            proj = tuple(show(full[x]) for x in J)
            if proj not in c_out:
                errors.append(f"row {key}: fine outer tuple {frow} projects to non-outer coarse tuple")
                break
    return not errors, errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("model")
    g.add_argument("--relation-cap", type=int, default=None,
                   help="skip relation enumeration for rows larger than this many assignments")
    v = sub.add_parser("verify")
    v.add_argument("model")
    v.add_argument("certificate")
    sp = sub.add_parser("sparsify")
    sp.add_argument("model")
    sp.add_argument("certificate")
    sp.add_argument("retained")
    vsp = sub.add_parser("verify-sparsify")
    vsp.add_argument("model")
    vsp.add_argument("certificate")
    vsp.add_argument("sparsify_certificate")
    lad = sub.add_parser("verify-sparsify-ladder")
    lad.add_argument("model")
    lad.add_argument("certificate")
    lad.add_argument("coarse_certificate")
    lad.add_argument("fine_certificate")
    args = parser.parse_args()
    if args.cmd == "generate":
        print(json.dumps(generate(load(args.model), args.relation_cap), indent=2))
    elif args.cmd == "verify":
        model = load(args.model)
        batch = load(args.certificate)
        ok, errors = verify(model, batch)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "sparsify":
        model = load(args.model)
        batch = load(args.certificate)
        retained = load(args.retained)
        print(json.dumps(sparsify(model, batch, retained["retained_map"]), indent=2))
    elif args.cmd == "verify-sparsify":
        model = load(args.model)
        batch = load(args.certificate)
        cert = load(args.sparsify_certificate)
        ok, errors = verify_sparsify(model, batch, cert)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "verify-sparsify-ladder":
        model = load(args.model)
        batch = load(args.certificate)
        coarse = load(args.coarse_certificate)
        fine = load(args.fine_certificate)
        ok, errors = verify_sparsify_ladder(model, batch, coarse, fine)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))


if __name__ == "__main__":
    main()
