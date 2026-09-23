#!/usr/bin/env python3
"""Offline re-audit of the recorded mechanics external baseline sweep.

Recomputes the summary counters from the per-instance records in
reports/mechanics_external_baseline_sweep.json and compares them with the
recorded summary block. This pins down exactly which runs the recorded
counter mis-bucketed.

Usage: python3 audit_sweep_summary.py [sweep.json]
"""
import json
import sys
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "reports/mechanics_external_baseline_sweep.json"
d = json.load(open(path))
cases = d["cases"]
recorded = d["summary"]


def status_bucket(run):
    """Classify an external run into the four-status vocabulary.

    SAT / UNSAT are status-bearing answers. TIMEOUT and solver-reported
    UNKNOWN (CP-SAT 'unknown') are non-answers: INCONCLUSIVE.
    """
    cl = run.get("classification")
    if cl in ("SAT", "UNSAT"):
        return cl
    return "INCONCLUSIVE"


def answer_evidence(run):
    """Whether the classification is backed by a verified cross-check."""
    cc = run.get("cross_check") or {}
    st = cc.get("status", "")
    if st in ("VERIFIED-SAT", "VERIFIED-UNSAT"):
        return True
    return False


runs = []
for c in cases:
    for r in c["external"]:
        runs.append((c, r))

count = Counter(status_bucket(r) for (_, r) in runs)
agree = 0
non_answers = []
for c, r in runs:
    b = status_bucket(r)
    native_unsat = c["expected"] == "UNSAT"
    if b == "UNSAT" and native_unsat:
        agree += 1
    elif b == "SAT" and not native_unsat:
        agree += 1
    else:
        if b == "INCONCLUSIVE":
            non_answers.append((c["family"], c["size"], c["observation"], r["solver"],
                                r.get("classification"), (r.get("cross_check") or {}).get("status")))

print("=== recomputed from per-instance records ===")
print("total external runs       :", len(runs))
print("SAT (status-bearing)      :", count["SAT"])
print("UNSAT (status-bearing)    :", count["UNSAT"])
print("INCONCLUSIVE (non-answer) :", count["INCONCLUSIVE"])
print("status-bearing agreements :", agree)
print()
print("=== recorded summary block ===")
for k in ("external_runs", "external_sat_cross_checked", "external_unsat_cross_checked",
          "external_inconclusive", "status_agreement_with_native"):
    print(f"{k:26s}: {recorded.get(k)}")
print()
print("=== non-answer runs (per-instance evidence) ===")
for row in non_answers:
    print("  ", row)
print()
print("=== discrepancy ===")
print("recorded UNSAT counter minus recomputed UNSAT:",
      recorded["external_unsat_cross_checked"] - count["UNSAT"])
print("recorded inconclusive minus recomputed      :",
      recorded["external_inconclusive"] - count["INCONCLUSIVE"])
print("recorded agreement minus recomputed         :",
      recorded["status_agreement_with_native"] - agree)
