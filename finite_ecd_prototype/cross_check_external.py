#!/usr/bin/env python3
"""Cross-check optional external solver output against ECD certificates.

Solver logs are never trusted as certificates. This script reads an external
adapter result and verifies an accompanying ECD certificate:
- external SAT requires a POLICY certificate verified on the original instance;
- external UNSAT requires a DP-REFUTATION certificate verified on the instance;
- external INCONCLUSIVE remains INCONCLUSIVE.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from finite_ecd import Instance, load_json, verify_policy, verify_dp_certificate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("external_result")
    ap.add_argument("instance")
    ap.add_argument("--policy", default=None, help="POLICY/CERTIFIED-SAT certificate JSON")
    ap.add_argument("--refutation", default=None, help="DP-REFUTATION certificate JSON")
    args = ap.parse_args()
    ext = load_json(args.external_result)
    raw = load_json(args.instance)
    inst = Instance.from_json(raw)
    status = ext.get("status", "INCONCLUSIVE")
    if status == "CERTIFIED-SAT-EXTERNAL":
        if not args.policy:
            out = {"status": "INCONCLUSIVE", "reason": "external SAT has no independently verified policy certificate"}
        else:
            cert = load_json(args.policy)
            assignment = cert.get("assignment", cert)
            ok, errors = verify_policy(inst, assignment)
            out = {"status": "VERIFIED-SAT" if ok else "REJECTED", "external_status": status, "errors": errors}
    elif status == "CERTIFIED-UNSAT-EXTERNAL":
        if not args.refutation:
            out = {"status": "INCONCLUSIVE", "reason": "external UNSAT has no independently verified refutation certificate"}
        else:
            cert = load_json(args.refutation)
            ok, errors = verify_dp_certificate(inst, raw, cert)
            if ok and cert.get("type") == "DP-REFUTATION":
                out = {"status": "VERIFIED-UNSAT", "external_status": status, "errors": []}
            elif ok:
                out = {"status": "REJECTED", "external_status": status, "errors": ["certificate verifies but is not a DP-REFUTATION"]}
            else:
                out = {"status": "REJECTED", "external_status": status, "errors": errors}
    else:
        out = {"status": "INCONCLUSIVE", "external_status": status, "reason": ext.get("reason", "external result is not certified")}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
