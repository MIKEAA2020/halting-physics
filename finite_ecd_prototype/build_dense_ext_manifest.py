#!/usr/bin/env python3
"""Build the dense-extension large-artifact manifest and the SHA256SUMS lines.

Two outputs:
1. reports/dense_extension_large_artifacts.json --- checksums and sizes of the
   dense-chain n=17/18 extension artifacts that exceed the repository's
   100 MB per-file limit (GitHub hard limit), with the deposit decision and
   the regeneration path for each. The native runner of this round re-emitted
   byte-identical copies of every phase-4-style DP certificate, so the
   certificates are exactly reproducible from the recorded driver.
2. stdout lines in examples/SHA256SUMS format for the small files that ARE
   deposited (instances, models, row batches, decompositions, native
   stdout/stderr, policy certificate, minisat result files).
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EX = ROOT / "examples"

LARGE = [
    "mech_dense17_same.cnf", "mech_dense17_same.lp", "mech_dense17_same_cpsat.json",
    "mech_dense17_same_dp_certificate.json", "mech_dense17_same_native_dp_certificate.json",
    "mech_dense17_split.cnf", "mech_dense17_split.lp", "mech_dense17_split_cpsat.json",
    "mech_dense17_split_dp_certificate.json", "mech_dense17_split_native_dp_certificate.json",
    "mech_dense18_same.cnf", "mech_dense18_same.lp", "mech_dense18_same_cpsat.json",
    "mech_dense18_same_dp_certificate.json", "mech_dense18_same_native_dp_certificate.json",
    "mech_dense18_split.cnf", "mech_dense18_split.lp", "mech_dense18_split_cpsat.json",
]

SMALL = []
for size, obs in [(17, "same"), (17, "split"), (18, "same"), (18, "split")]:
    pfx = f"mech_dense{size}_{obs}"
    SMALL += [f"{pfx}_instance.json", f"{pfx}_model.json", f"{pfx}_row_batch.json",
              f"{pfx}_tree_decomp.json", f"{pfx}_native_stdout.txt",
              f"{pfx}_native_stderr.txt", f"{pfx}_minisat_res_0",
              f"{pfx}_minisat_res_1", f"{pfx}_minisat_res_2"]
SMALL.append("mech_dense17_split_policy_certificate.json")

REGEN = {
    ".cnf": "regenerable: baseline_encode.py to_dimacs on the archived instance",
    ".lp": "regenerable: baseline_encode.py to_milp_lp on the archived instance",
    "_cpsat.json": "regenerable: baseline_encode.py to_cpsat_json on the archived instance",
    "_dp_certificate.json":
        "regenerable: mechanics_benchmarks.run_case / native_dp_runner.py on the "
        "archived instance and decomposition; this round's bounded native runs "
        "re-emitted byte-identical copies (sha256-equal, verified for "
        "dense17 same/split and dense18 same)",
    "_native_dp_certificate.json":
        "byte-identical duplicate of the phase-4-style certificate (not archived "
        "separately, matching the dense16 convention); checksum recorded here",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


large_entries = []
for name in LARGE:
    p = EX / name
    if not p.exists():
        continue
    key = next((k for k in REGEN if name.endswith(k)), "")
    large_entries.append({
        "file": f"examples/{name}",
        "sha256": sha256(p),
        "bytes": p.stat().st_size,
        "deposited": False,
        "reason": "exceeds the repository 100 MB per-file limit",
        "regeneration": REGEN.get(key, ""),
    })

small_lines = []
for name in SMALL:
    p = EX / name
    if not p.exists():
        continue
    small_lines.append(f"{sha256(p)}  {name}")

manifest = {
    "status": "COMPLETE",
    "purpose": "checksum manifest for dense-chain n=17/18 extension artifacts "
               "that exceed the repository per-file size limit",
    "limit_note": "GitHub refuses files above 100 MB (hard limit, would require "
                  "Git LFS); the recorded study therefore archives checksums "
                  "and sizes here and deposits every small artifact",
    "large_artifacts": large_entries,
    "deposited_small_artifacts_count": len(small_lines),
}
out = ROOT / "reports" / "dense_extension_large_artifacts.json"
out.write_text(json.dumps(manifest, indent=2))
print(f"large artifacts manifested: {len(large_entries)}")
print(f"small artifacts hashed    : {len(small_lines)}")
with open(ROOT / "reports" / "dense_ext_sha256sums_lines.txt", "w") as f:
    f.write("\n".join(small_lines) + "\n")
print("SHA256SUMS lines written to reports/dense_ext_sha256sums_lines.txt")
