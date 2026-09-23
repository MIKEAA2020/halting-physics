#!/usr/bin/env python3
"""Minimal exact affine row generator and FE-ROW verifier.

This is a finite-model front end, not a continuum mechanics solver. It certifies
rows of explicitly declared affine response models using exact rational
arithmetic.
"""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Tuple


def F(x: Any) -> Fraction:
    if isinstance(x, list) and len(x) == 2:
        return Fraction(int(x[0]), int(x[1]))
    return Fraction(str(x))


def show(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def load(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())


def eval_response(row_model: Dict[str, Any], assignment: Dict[str, Any]) -> Fraction:
    y = F(row_model.get("d", 0))
    coeffs = row_model.get("coeffs", {})
    for x, g in coeffs.items():
        y += F(g) * F(assignment[x])
    return y


def classify(y: Fraction, safe_interval: List[Any]) -> str:
    lo, hi = F(safe_interval[0]), F(safe_interval[1])
    return "SAFE" if lo <= y <= hi else "UNSAFE"


def generate(model: Dict[str, Any]) -> Dict[str, Any]:
    variables = model["variables"]
    domains = {x: model["domains"][x] for x in variables}
    safe_interval = model["safe_interval"]
    rows = []
    relations = []
    for rmodel in model["rows"]:
        safe_actions = []
        for values in itertools.product(*(domains[x] for x in variables)):
            assignment = dict(zip(variables, values))
            y = eval_response(rmodel, assignment)
            status = classify(y, safe_interval)
            if status == "SAFE":
                safe_actions.append(list(values))
            rows.append({
                "type": "FE-ROW",
                "model": model.get("name", "affine-model"),
                "row": rmodel["name"],
                "variables": variables,
                "assignment": assignment,
                "exact": True,
                "response": show(y),
                "interval": [show(y), show(y)],
                "safe_interval": [str(safe_interval[0]), str(safe_interval[1])],
                "classification": status,
            })
        relations.append({"name": rmodel["name"], "scope": variables, "relation": safe_actions})
    instance = {"variables": variables, "domains": domains, "factors": relations}
    return {"type": "FE-ROW-BATCH", "status": "CERTIFIED", "model": model.get("name", "affine-model"), "instance": instance, "rows": rows}


def verify_row(model: Dict[str, Any], cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if cert.get("type") != "FE-ROW":
        errors.append("wrong certificate type")
        return False, errors
    row_name = cert.get("row")
    candidates = [r for r in model.get("rows", []) if r.get("name") == row_name]
    if not candidates:
        errors.append(f"unknown row {row_name!r}")
        return False, errors
    rmodel = candidates[0]
    assignment = cert.get("assignment", {})
    for x in model["variables"]:
        if x not in assignment:
            errors.append(f"missing assignment for {x}")
        elif assignment[x] not in model["domains"][x]:
            errors.append(f"value {assignment[x]!r} outside domain of {x}")
    if errors:
        return False, errors
    y = eval_response(rmodel, assignment)
    interval = cert.get("interval")
    if interval != [show(y), show(y)]:
        errors.append("certified interval does not match exact response")
    expected = classify(y, model["safe_interval"])
    if cert.get("classification") != expected:
        errors.append(f"classification {cert.get('classification')!r} should be {expected!r}")
    if cert.get("response") != show(y):
        errors.append("response value does not match exact response")
    return not errors, errors


def verify_batch(model: Dict[str, Any], cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if cert.get("type") != "FE-ROW-BATCH":
        errors.append("wrong certificate type")
        return False, errors
    for i, row in enumerate(cert.get("rows", [])):
        ok, es = verify_row(model, row)
        if not ok:
            errors.extend([f"row {i}: {e}" for e in es])
    regenerated = generate(model)
    if len(regenerated["rows"]) != len(cert.get("rows", [])):
        errors.append("row count disagrees with regenerated batch")
    if regenerated.get("instance") != cert.get("instance"):
        errors.append("derived finite instance disagrees with regenerated instance")
    return not errors, errors



def interval_for_omitted(model: Dict[str, Any], row_model: Dict[str, Any], retained: List[str]) -> Tuple[Fraction, Fraction]:
    retained_set = set(retained)
    lo = Fraction(0); hi = Fraction(0)
    for x in model["variables"]:
        if x in retained_set:
            continue
        g = F(row_model.get("coeffs", {}).get(x, 0))
        vals = [g * F(v) for v in model["domains"][x]]
        lo += min(vals); hi += max(vals)
    return lo, hi


def generate_sparsification(model: Dict[str, Any], retained_map: Dict[str, List[str]]) -> Dict[str, Any]:
    """Generate exact affine omitted-term sparsification certificates.

    For each row and retained assignment, compute the exact omitted interval.
    Inner rows are retained assignments whose full response interval is contained
    in the safe interval. Outer rows are retained assignments whose response
    interval intersects the safe interval.
    """
    safe_lo, safe_hi = F(model["safe_interval"][0]), F(model["safe_interval"][1])
    cert_rows = []
    inner_factors = []
    outer_factors = []
    for row_model in model["rows"]:
        row_name = row_model["name"]
        retained = retained_map.get(row_name, model["variables"])
        domains = [model["domains"][x] for x in retained]
        eta_lo, eta_hi = interval_for_omitted(model, row_model, retained)
        inner_rel = []
        outer_rel = []
        for values in itertools.product(*domains):
            assignment = dict(zip(retained, values))
            retained_response = F(row_model.get("d", 0))
            for x in retained:
                retained_response += F(row_model.get("coeffs", {}).get(x, 0)) * F(assignment[x])
            resp_lo = retained_response + eta_lo
            resp_hi = retained_response + eta_hi
            inner = safe_lo <= resp_lo and resp_hi <= safe_hi
            outer = not (resp_hi < safe_lo or resp_lo > safe_hi)
            if inner:
                inner_rel.append(list(values))
            if outer:
                outer_rel.append(list(values))
            cert_rows.append({
                "type": "SPARSIFICATION-ROW",
                "model": model.get("name", "affine-model"),
                "row": row_name,
                "retained": retained,
                "assignment": assignment,
                "omitted_interval": [show(eta_lo), show(eta_hi)],
                "retained_response": show(retained_response),
                "response_interval": [show(resp_lo), show(resp_hi)],
                "safe_interval": [show(safe_lo), show(safe_hi)],
                "inner": inner,
                "outer": outer,
            })
        inner_factors.append({"name": row_name, "scope": retained, "relation": inner_rel})
        outer_factors.append({"name": row_name, "scope": retained, "relation": outer_rel})
    retained_vars = []
    for row_model in model["rows"]:
        for x in retained_map.get(row_model["name"], model["variables"]):
            if x not in retained_vars:
                retained_vars.append(x)
    domains_out = {x: model["domains"][x] for x in retained_vars}
    return {
        "type": "SPARSIFICATION-BATCH",
        "status": "CERTIFIED",
        "model": model.get("name", "affine-model"),
        "retained_map": retained_map,
        "rows": cert_rows,
        "inner_instance": {"variables": retained_vars, "domains": domains_out, "factors": inner_factors},
        "outer_instance": {"variables": retained_vars, "domains": domains_out, "factors": outer_factors},
    }


def verify_sparsification(model: Dict[str, Any], cert: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if cert.get("type") != "SPARSIFICATION-BATCH":
        return False, ["wrong certificate type"]
    retained_map = {k: list(v) for k, v in cert.get("retained_map", {}).items()}
    regenerated = generate_sparsification(model, retained_map)
    if regenerated.get("inner_instance") != cert.get("inner_instance"):
        errors.append("inner sparse instance disagrees with regeneration")
    if regenerated.get("outer_instance") != cert.get("outer_instance"):
        errors.append("outer sparse instance disagrees with regeneration")
    if len(regenerated.get("rows", [])) != len(cert.get("rows", [])):
        errors.append("sparsification row count disagrees with regeneration")
        return False, errors
    for i, (r0, r1) in enumerate(zip(regenerated["rows"], cert.get("rows", []))):
        for key in ["row", "retained", "assignment", "omitted_interval", "retained_response", "response_interval", "safe_interval", "inner", "outer"]:
            if r0.get(key) != r1.get(key):
                errors.append(f"row {i} field {key} disagrees with regeneration")
                break
    return not errors, errors


def relation_set(factor: Dict[str, Any]) -> set:
    return {tuple(tuple(v) if isinstance(v, list) else v for v in row) for row in factor.get("relation", [])}


def verify_sparsification_ladder(model: Dict[str, Any], coarse: Dict[str, Any], fine: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Verify rowwise monotonicity for retained scopes J subset J'.

    Checks the certificate-level consequences:
    - J_i subset J'_i for every row;
    - every coarse inner retained tuple has all fine extensions in the fine inner relation;
    - every fine outer tuple projects to a coarse outer tuple.
    This is the finite rowwise form behind Gamma^-_J <= Gamma^-_J' <= true <= Gamma^+_J' <= Gamma^+_J.
    """
    errors: List[str] = []
    ok_c, err_c = verify_sparsification(model, coarse)
    ok_f, err_f = verify_sparsification(model, fine)
    if not ok_c:
        errors.extend(["coarse: " + e for e in err_c])
    if not ok_f:
        errors.extend(["fine: " + e for e in err_f])
    if errors:
        return False, errors
    coarse_map = {k: list(v) for k, v in coarse.get("retained_map", {}).items()}
    fine_map = {k: list(v) for k, v in fine.get("retained_map", {}).items()}
    c_inner = {f["name"]: f for f in coarse["inner_instance"]["factors"]}
    f_inner = {f["name"]: f for f in fine["inner_instance"]["factors"]}
    c_outer = {f["name"]: f for f in coarse["outer_instance"]["factors"]}
    f_outer = {f["name"]: f for f in fine["outer_instance"]["factors"]}
    for row_model in model.get("rows", []):
        name = row_model["name"]
        J = coarse_map.get(name, model["variables"])
        Jp = fine_map.get(name, model["variables"])
        if not set(J) <= set(Jp):
            errors.append(f"row {name}: retained set is not nested")
            continue
        c_in = relation_set(c_inner[name]); f_in = relation_set(f_inner[name])
        c_out = relation_set(c_outer[name]); f_out = relation_set(f_outer[name])
        extra = [x for x in Jp if x not in J]
        # Coarse inner cylinder inclusion into fine inner.
        for crow in c_in:
            base = dict(zip(J, crow))
            for extra_vals in itertools.product(*(model["domains"][x] for x in extra)):
                full = dict(base)
                full.update(dict(zip(extra, extra_vals)))
                ftuple = tuple(full[x] for x in Jp)
                if ftuple not in f_in:
                    errors.append(f"row {name}: coarse inner tuple {crow} has fine extension {ftuple} not inner")
                    break
        # Fine outer projects into coarse outer.
        for frow in f_out:
            full = dict(zip(Jp, frow))
            proj = tuple(full[x] for x in J)
            if proj not in c_out:
                errors.append(f"row {name}: fine outer tuple {frow} projects to {proj}, not coarse outer")
                break
    return not errors, errors

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("model")
    v = sub.add_parser("verify")
    v.add_argument("model")
    v.add_argument("certificate")
    sp = sub.add_parser("sparsify")
    sp.add_argument("model")
    sp.add_argument("retained")
    vsp = sub.add_parser("verify-sparsify")
    vsp.add_argument("model")
    vsp.add_argument("certificate")
    lad = sub.add_parser("verify-sparsify-ladder")
    lad.add_argument("model")
    lad.add_argument("coarse_certificate")
    lad.add_argument("fine_certificate")
    args = parser.parse_args()
    if args.cmd == "generate":
        print(json.dumps(generate(load(args.model)), indent=2))
    elif args.cmd == "verify":
        model = load(args.model)
        cert = load(args.certificate)
        ok, errors = verify_batch(model, cert) if cert.get("type") == "FE-ROW-BATCH" else verify_row(model, cert)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "sparsify":
        model = load(args.model)
        retained = load(args.retained)
        print(json.dumps(generate_sparsification(model, retained["retained_map"]), indent=2))
    elif args.cmd == "verify-sparsify":
        model = load(args.model)
        cert = load(args.certificate)
        ok, errors = verify_sparsification(model, cert)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))
    elif args.cmd == "verify-sparsify-ladder":
        model = load(args.model)
        coarse = load(args.coarse_certificate)
        fine = load(args.fine_certificate)
        ok, errors = verify_sparsification_ladder(model, coarse, fine)
        print(json.dumps({"status": "VERIFIED" if ok else "REJECTED", "errors": errors}, indent=2))


if __name__ == "__main__":
    main()
