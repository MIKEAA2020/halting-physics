#!/usr/bin/env python3
"""Prove the evidence-gated agreement counter is semantics-preserving.

Recomputes status_agreement_with_native from the recorded per-run records
under BOTH the old semantics (classification match only) and the fixed
semantics (classification match AND verified cross-check evidence), for every
recorded sweep. The fixed counter must equal the recorded value in every file,
which shows the root-cause fix changes no recorded number while closing the
latent over-counting hole (REJECTED or INCONCLUSIVE-evidence runs no longer
count as agreement).

Also checks the structural identity that now holds by construction:
status_agreement_with_native == external_sat_cross_checked + external_unsat_cross_checked.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NORM_MECH = lambda s: (s or "").replace("DP-", "").replace("OPTIMUM", "SAT").replace("REFUTATION", "UNSAT")
NORM_EXT = lambda s: (s or "").replace("CERTIFIED-", "").replace("OPT", "SAT")

FILES = [
    ("reports/external_baseline_sweep.json", "dp_status", NORM_EXT),
    ("reports/mechanics_external_baseline_sweep.json", "status", NORM_MECH),
    ("reports/mechanics_external_baseline_sweep_v2.json", "status", NORM_MECH),
]

ok = True
for rel, native_key, norm in FILES:
    p = ROOT / rel
    if not p.exists():
        print(f"SKIP (missing): {rel}")
        continue
    d = json.loads(p.read_text())
    recorded = d["summary"]["status_agreement_with_native"]
    old = fixed = 0
    sat = unsat = 0
    for c in d["cases"]:
        native_status = norm((c.get("native") or {}).get(native_key))
        for e in c.get("external", []):
            cl = e.get("classification")
            cc = (e.get("cross_check") or {}).get("status")
            if cc == "VERIFIED-SAT":
                sat += 1
            if cc == "VERIFIED-UNSAT":
                unsat += 1
            if cl is not None and native_status and cl == native_status:
                old += 1
                if cc in ("VERIFIED-SAT", "VERIFIED-UNSAT"):
                    fixed += 1
    ident = (fixed == sat + unsat)
    status = "OK" if (fixed == recorded and old == fixed and ident) else "MISMATCH"
    if status != "OK":
        ok = False
    print(f"{status}: {rel}")
    print(f"    recorded={recorded}  old-semantics={old}  fixed-semantics={fixed}")
    print(f"    identity agreement == sat_cross({sat}) + unsat_cross({unsat}) = {sat + unsat}: {ident}")

sys.exit(0 if ok else 1)
