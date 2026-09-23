#!/usr/bin/env python3
"""Summarize finite ECD instance/decomposition/certificate size and verification time."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
from finite_ecd import Instance, load_json, validate_tree_decomp, verify_dp_certificate


def weighted_width(inst: Instance, decomp: dict) -> int:
    ww = 0
    for xs in decomp.get("bags", {}).values():
        s = 0
        for x in xs:
            d = len(inst.domains[x])
            s += (d - 1).bit_length()
        ww = max(ww, s)
    return ww


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instance")
    ap.add_argument("--decomp", default=None)
    ap.add_argument("--certificate", default=None)
    args = ap.parse_args()
    raw = load_json(args.instance)
    inst = Instance.from_json(raw)
    out = {
        "instance": args.instance,
        "variables": len(inst.variables),
        "domain_value_count": sum(len(inst.domains[x]) for x in inst.variables),
        "factors": len(inst.factors),
        "factor_rows": sum(len(f.relation) for f in inst.factors),
        "instance_bytes": Path(args.instance).stat().st_size,
    }
    if args.decomp:
        dec = load_json(args.decomp)
        if "tree_decomp" in dec: dec = dec["tree_decomp"]
        t0 = time.perf_counter(); ok, errors = validate_tree_decomp(inst, dec); t1 = time.perf_counter()
        widths = [len(xs)-1 for xs in dec.get("bags", {}).values()]
        out.update({
            "tree_decomp": args.decomp,
            "bags": len(dec.get("bags", {})),
            "width": max(widths) if widths else None,
            "weighted_width": weighted_width(inst, dec),
            "tree_decomp_bytes": Path(args.decomp).stat().st_size,
            "tree_decomp_verify_status": "VERIFIED" if ok else "REJECTED",
            "tree_decomp_verify_errors": errors,
            "tree_decomp_verify_seconds": t1-t0,
        })
    if args.certificate:
        cert = load_json(args.certificate)
        t0 = time.perf_counter(); ok, errors = verify_dp_certificate(inst, raw, cert); t1 = time.perf_counter()
        out.update({
            "certificate": args.certificate,
            "certificate_type": cert.get("type"),
            "certificate_status": cert.get("status"),
            "certificate_bytes": Path(args.certificate).stat().st_size,
            "certificate_verify_status": "VERIFIED" if ok else "REJECTED",
            "certificate_verify_errors": errors,
            "certificate_verify_seconds": t1-t0,
            "optimum_cost": cert.get("optimum_cost"),
        })
    print(json.dumps(out, indent=2))

if __name__ == "__main__": main()
