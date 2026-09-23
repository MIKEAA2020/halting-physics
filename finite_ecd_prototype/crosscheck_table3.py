#!/usr/bin/env python3
"""Cross-check v6 Table 3 (sparsification study) against the recorded JSON.

Verifies every displayed value of the manuscript's Table 3 against
reports/sparsification_study.json, including the compressed rows (finest-rung
values) and the rung inventory claimed in the caption.
"""
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "reports/sparsification_study.json"
d = json.load(open(path))

# manuscript Table 3 rows: (family, size, radius_label, retained, inner_w, unresolved, same, split)
# radius_label uses the manuscript convention; compressed ranges map to finest rung.
MS_ROWS = [
    ("ten-bar", 1, "0", 1.6, 3, 0.50, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("ten-bar", 1, "full", 4.0, 3, 0.00, "CERTIFIED", "CERTIFIED"),
    ("chain-pretension", 64, "0", 1.0, 0, 0.00, "CERTIFIED", "CERTIFIED"),
    ("chain-pretension", 64, "full", 1.0, 0, 0.00, "CERTIFIED", "CERTIFIED"),
    ("dense-chain", 12, "0", 1.0, 0, 1.00, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("dense-chain", 12, "1", 3.0, 2, 1.00, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("dense-chain", 12, "2", 5.0, 4, 1.00, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("dense-chain", 12, "3", 7.0, 6, 1.00, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("dense-chain", 12, "full", 12.0, 11, 0.00, "CERTIFIED", "CERTIFIED"),
    ("lattice", 1, "0", 0.7, 0, 0.33, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("lattice", 1, "1", 3.6, 5, 0.15, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("lattice", 1, "full", 5.6, 5, 0.00, "CERTIFIED", "CERTIFIED"),
    ("lattice", 2, "0", 0.7, 0, 0.64, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("lattice", 2, "1", 6.0, 11, 0.27, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("lattice", 2, "full", 12.0, 11, 0.00, "CERTIFIED", "CERTIFIED"),
    ("lattice", 3, "0", 0.7, 0, 0.70, "INCONCLUSIVE", "INCONCLUSIVE"),
    ("lattice", 3, "1", 6.7, 14, 0.34, "INCONCLUSIVE", "INCONCLUSIVE"),
]

fams = {}
for f in d["families"]:
    fams.setdefault((f["family"], f["size"]), []).extend(f["rungs"])

print("=== per-value cross-check (manuscript vs recorded) ===")
bad = 0
for fam, size, rad, ret, iw, unf, same, split in MS_ROWS:
    rungs = fams.get((fam, size), [])
    match = [r for r in rungs if str(r["radius"]) == rad]
    if not match:
        print(f"MISSING RUNG: {fam} n={size} radius={rad}")
        bad += 1
        continue
    r = match[0]
    checks = [
        ("retained", ret, r["retained_mean"]),
        ("inner_w", iw, r["inner_width"]),
        ("unresolved", unf, r["unresolved_fraction_mean"]),
        ("same", same, r["same_bracket"].replace("CERTIFIED-UNSAT", "CERTIFIED").replace("CERTIFIED-SAT", "CERTIFIED")),
        ("split", split, r["split_bracket"].replace("CERTIFIED-SAT", "CERTIFIED").replace("CERTIFIED-UNSAT", "CERTIFIED")),
    ]
    for name, ms, rec in checks:
        ok = (abs(ms - rec) < 0.005) if isinstance(ms, float) else (ms == rec)
        if not ok:
            print(f"MISMATCH {fam} n={size} r={rad} {name}: manuscript={ms} recorded={rec}")
            bad += 1
print("mismatches:", bad)

print()
print("=== rung inventory (recorded truth) ===")
total = 0
for (fam, size), rungs in fams.items():
    radii = [str(r["radius"]) for r in rungs]
    total += len(rungs)
    print(f"{fam:18s} n={size:<4} rungs={len(rungs)} radii={radii}")
print("total rungs:", total)

print()
print("=== hidden rung values (compressed away in Table 3) ===")
for fam, size, rad in [("ten-bar", 1, "1"), ("ten-bar", 1, "2"), ("lattice", 1, "2")]:
    r = [x for x in fams[(fam, size)] if str(x["radius"]) == rad][0]
    print(f"{fam} n={size} r={rad}: retained_mean={r['retained_mean']} inner_w={r['inner_width']} "
          f"unresolved={r['unresolved_fraction_mean']} same={r['same_bracket']} split={r['split_bracket']}")

print()
print("=== caption inventory claim check ===")
print("v6 caption claims : ten-bar 5, dense-chain 5, chain 1, lattices 4/3/2 (total 20)")
inv = {k: len(v) for k, v in fams.items()}
print("recorded inventory:", ", ".join(f"{k[0]}({k[1]})={v}" for k, v in inv.items()), f"(total {total})")
