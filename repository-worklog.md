# Repository worklog

Append-only work log for the `halting-physics` repository. Each section
records one deposited round. Files are never overwritten: every revision
is a new versioned file, and recorded artifacts are byte-preserved.

---

## Round 1 — initial deposit of the recorded workspace (release v4 archive)

- Deposited the finite ECD prototype artifact (source, reports, gate
  records) and all examples from the recorded workspace archive, together
  with all prior document creations from the release zips: main monograph
  versions, companion plans v1-v18, implementation reports v1-v7, and the
  auxiliary status documents.
- Deposited `sparsification_study.json` (Table 3 rung values) and the full
  harness source including `mechanics_gen.py`, making the ten-bar
  "3x4 bays" geometry (two bays of 3-by-4 units with 3-4-5 diagonals) and
  the corrupted-certificate rejection counts verifiable from the
  repository.
- No existing file was modified.

---

## Round 2 — companion monograph v6 / artifact appendix v5 (root-fix pass)

- Line-level audit of the v5 companion resolved into a root-fix revision:
  the sensor-repair theorem restated over inclusion-minimal conflict cores,
  the inner-outer soundness proposition proved, the width-DP section
  completed, the sparsification ladder proof completed, cost notions
  separated, Appendix B (standard reductions) and the seventeen-entry
  bibliography added.
- Deposited as new files: `companion monograph/monograph-2-algorithms-and-certificates-v6.tex`,
  `companion monograph/companion-artifact-appendix-v5.tex`, plan v19/v20,
  implementation report v8.
- Kernel of a defect report carried forward from this round: the v6
  footnote claiming the recorded sweep counters were inconsistent with
  the per-instance records (see round 3's audit).

---

## Round 3 — phase-6 replication, dense-family extension, accounting audit (this round)

### Environment and provenance

- Two-core Intel Xeon virtual machine, 3.9 GiB memory, glibc 2.41,
  kernel 5.10.134, Python 3.12.14.
- Solvers rebuilt or pinned to the recorded versions: minisat from the
  arminbiere mirror at commit `16982a5` (gcc 14.2, `-O3`, mkLit
  compatibility patch), kissat 4.0.4 at commit `8af8e56` (gcc 14.2,
  `-O3`), z3 5.1.0, OR-Tools CP-SAT 9.15.6755, HiGHS 1.15.1.
- GitHub access token persisted in the working environment credential
  store.

### Phase-6 sweep replication

- The full fourteen-instance comparative scaling study was re-executed in
  case chunks (`--only` / `--merge`, equivalent to a single invocation)
  with all five solvers at version-exact provenance.
- Result: `finite_ecd_prototype/reports/mechanics_external_baseline_sweep_v2.json`
  reproduces the recorded summary exactly (14 native certificates, 7
  policies, 34/33/3/0/67) and every structural field; the re-emitted
  native certificates are byte-identical to the archived phase-4
  certificates (SHA-256 equality verified for dense8/16, ten-bar,
  lattice C2, and the dense-17/18 extension certificates).

### Dense-family extension n=17/18

- `dense_extension_generate.py` (recorded phase-4 driver, per-case
  checkpointing) generated the four extension cases. FE row batches and
  decompositions verified for all four (widths 16, 16, 17, 17). DP
  certificates verified for three: 17 same REFUTATION (120.2 MB), 17
  split OPTIMUM with verified policy (243.2 MB), 18 same REFUTATION
  (252.5 MB). The 18 split case hit the machine's physical memory during
  in-process certificate emission and is recorded as DP-MEMORY-LIMIT
  (exit 137; kernel log: `Out of memory: Killed process 8298 (python3)
  total-vm:3816532kB, anon-rss:3750608kB`, i.e. about 3.75 GiB resident
  during message construction); model, certified row batch, instance,
  and validated decomposition are archived, with the failure record
  `reports/dense_ext_gen_dense_18_split_FAILED.json`.
- `dense_extension_sweep.py` (fixed phase-6 protocol, per-(case, solver)
  checkpointing) recorded 20 external runs over the four instances:
  seven verified satisfiable models, three verified unsatisfiable
  answers, ten inconclusive runs, no rejections, seven agreements with
  the native certificates. The bounded native run of 18 split raised
  `MemoryError` at the 3 GiB address-space cap (63.3 s wall; traceback
  archived in `examples/mech_dense18_split_native_stderr.txt`).
- Result: `finite_ecd_prototype/reports/mechanics_dense_extension.json`
  and `finite_ecd_prototype/reports/mechanics_dense_extension_sweep.json`.

### Harness accounting audit and root fix

- The v6 footnote and plan v20 item 6 claimed the recorded mechanics
  sweep counters (34/33/3/67) were inconsistent with the per-instance
  records, hypothesizing a CP-SAT UNKNOWN run bucketed with the
  unsatisfiable answers, and proposed a "corrected accounting" of
  32/4/66. The forensic audit refutes this on four grounds: the recorded
  per-instance records show the CP-SAT dense-16 same run answered UNSAT
  (49.5 s) with a verified cross-check; the replication answers the same
  (50.3 s); `cpsat_runner.py` maps UNKNOWN to INCONCLUSIVE by
  construction so it cannot be bucketed with UNSAT; and the recorded
  artifact is byte-identical (SHA-256 `acd666e3...`) across the
  release-v4 archive, the recorded-reports extraction, the live
  prototype, and the repository. The 32/4/66 "correction" is itself a
  documentation error and is withdrawn in the v7 manuscript.
- Root fix in the harness code: `status_agreement_with_native` is now
  gated on verified cross-check evidence in `external_baseline_sweep.py`,
  `mechanics_baseline_sweep.py`, and `dense_extension_sweep.py`.
  `verify_accounting_fix.py` proves the change semantics-preserving on
  every recorded sweep (recorded = old = fixed semantics).
- The recorded `reports/mechanics_external_baseline_sweep.json` is
  deliberately not regenerated: it is already consistent, and
  regeneration would overwrite the user's original artifact.

### Documents and deposits of this round

- New versions only: companion monograph v7 (compiles under tectonic with
  no new typographical warnings relative to v6), artifact appendix v6,
  implementation report v9, plan v21, and this worklog.
- Prototype deposits: the two extension drivers, the manifest builder,
  and the audit tools (`audit_sweep_summary.py`,
  `crosscheck_table3.py`, `diff_reports.py`, `verify_accounting_fix.py`)
  under `finite_ecd_prototype/`; the v2 replication report and eight
  extension reports under `finite_ecd_prototype/reports/`; thirty-seven
  small dense-17/18 example artifacts with `examples/SHA256SUMS`
  extended; the large-artifact checksum manifest
  `reports/dense_extension_large_artifacts.json` covering the eighteen
  artifacts above the repository's 100 MB per-file limit (dense-17/18
  encodings and DP certificates, regenerable from the archived instances
  and decompositions).
- Harness bug-fix commit: the evidence-gated agreement counter in
  `external_baseline_sweep.py` and `mechanics_baseline_sweep.py`.

### Remaining items

1. archival DOI assigned and inserted at publication time;
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope;
3. release manifest refresh to be frozen at the next artifact release,
   incorporating the v2 replication and dense-extension outputs.
