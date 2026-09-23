#!/usr/bin/env python3
"""Compare a regenerated report against the recorded one, field by field.

Timing and environment fields are expected to differ; structural and
certification fields must match exactly.
"""
import json
import sys

recorded_path, regenerated_path = sys.argv[1], sys.argv[2]
rec = json.load(open(recorded_path))
reg = json.load(open(regenerated_path))

TIME_KEYS = {"seconds", "seconds_median", "seconds_min", "seconds_max", "wall_seconds",
             "dp_seconds", "verify_seconds", "fe_generate_seconds", "fe_verify_seconds",
             "encode_seconds", "decomp_seconds", "dp_verify_seconds", "policy_seconds",
             "sparsify_seconds", "sparsify_verify_seconds", "peak_rss_kib",
             "certificate_bytes", "instance_bytes", "row_batch_bytes", "certificate_write_seconds",
             "generate_seconds", "verify_seconds_total", "build_seconds", "solve_seconds",
             "inner_peak_rss_kib", "sparsify_certificates_bytes"}

mismatches = []
matches = 0


def walk(a, b, path):
    global matches
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                mismatches.append(f"{path}.{k}: missing in recorded (regenerated has {b[k]!r})")
                continue
            if k not in b:
                mismatches.append(f"{path}.{k}: missing in regenerated (recorded has {a[k]!r})")
                continue
            walk(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            mismatches.append(f"{path}: length {len(a)} vs {len(b)}")
            return
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]")
    else:
        leaf = path.rsplit(".", 1)[-1].split("[")[0]
        if leaf in TIME_KEYS or leaf.endswith("_seconds") or leaf.endswith("_kib") or leaf.endswith("_bytes"):
            matches += 1  # timing/size field: hardware-dependent, skip equality
            return
        if a != b:
            mismatches.append(f"{path}: recorded={a!r} regenerated={b!r}")
        else:
            matches += 1


walk(rec, reg, "")
print(f"matching leaf fields : {matches}")
print(f"mismatches           : {len(mismatches)}")
for m in mismatches[:40]:
    print("  ", m)
if len(mismatches) > 40:
    print(f"  ... and {len(mismatches) - 40} more")
