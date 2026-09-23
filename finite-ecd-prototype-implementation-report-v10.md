# Finite ECD prototype implementation report v10

## New in v10

This round audits the v7 manuscript and appendix v6 against the deposited
artifact ground truth (the recorded JSON reports and the harness source under
`finite_ecd_prototype/`), re-derives every recorded number cited by the
manuscript, and corrects the residual flaws at their root in companion
monograph v8 and artifact appendix v7. No recorded artifact is regenerated or
modified; new documents only.

## 1. Audit method

Every quantitative claim of the v7 manuscript was checked against the
deposited reports with one-off scripts:

- `reports/mechanics_benchmarks.json` (Table 2: 20 cases, 18 constructed,
  20 verified row batches, 18 decompositions, 18 DP certificates, 9
  refutations + 9 optima, 2 RELATION-TABLE-LIMIT rows, DP/verify timings);
- `reports/sparsification_study.json` (Table 3: rung inventory ten-bar 4,
  chain 2, dense 5, lattice 4/3/2 = 20 rungs; 14 verified ladder steps; all
  displayed retained/width/unresolved values and brackets; monotonicity of
  the unresolved fraction; 9 policies verified against full rows);
- `reports/mechanics_external_baseline_sweep.json` (Table 5: all fourteen
  rows' native and external medians; the 34/33/3/0/67 summary; FE
  preprocessing 2.7 s + 2.7 s; certificate sizes 57.1/115.6 MB; SHA-256
  `acd666e3...` confirmed);
- `reports/mechanics_dense_extension_sweep.json` and
  `reports/mechanics_dense_extension.json` (Table 6: all cells; widths
  16/16/17/17; certificate sizes 120.2/243.2/252.5 MB; accounting
  7/3/10/0/7; per-run cross-check statuses);
- `reports/dense_extension_large_artifacts.json` (18 entries; CP-SAT
  encodings 137.68-388.11 MB; DIMACS/LP/DP-certificate entries);
- `reports/external_baseline_sweep.json` (controlled-width study: 24
  instances, 120 runs, 95 SAT + 25 UNSAT, 0 inconclusive, 0 rejected, 120
  agreements, peak external RSS 102572 KiB = 100.2 MiB; per-instance
  medians);
- `diff_reports.py` on the recorded sweep against the v2 replication
  (1135 matching leaf fields, 29 mismatches: 14 certificate file names, 14
  per-case provenance notes present only in the recorded report, and the
  hardware RAM figure 4.1Gi -> 3.9Gi);
- `repro_report.json` and the report status fields for the verification-gate
  table rows;
- the harness source for the limit semantics (`run_with_limits`,
  `run_cpsat`/`run_highs` with `TIMEOUT_SECONDS + 30.0`, `native_run` with
  the same grace, `cpsat_runner.py` UNKNOWN -> INCONCLUSIVE mapping, and
  the evidence-gated `status_agreement_with_native` counter).

## 2. Confirmed correct (no action)

The v7 withdrawal of the v6 "corrected accounting" is confirmed against the
per-instance records and the code; the recorded summary 34/33/3/0/67 is
consistent and the CP-SAT dense-16 same run answered UNSAT at 49.5 s with a
verified cross-check. Tables 2, 3, 5, and 6 match the reports cell by cell,
including the v7 corrections (49.5 s cell; lattice values 0.67/3.56/5.56/
6.67; the true rung inventory). The extension widths, certificate sizes,
accounting, and large-artifact manifest match. The FE preprocessing times,
the replication summary, and the gate-table rows match.

## 3. Residual flaws corrected in v8 / appendix v7

1. v7 still `\input` appendix v5, so the compiled v7 document omitted the
   entire v6 appendix content (audit tools, replication, dense-extension
   section, updated claim boundary) that the v7 body references. v8 inputs
   appendix v7.
2. Table 4 (controlled-width baselines) matched no deposited report: its
   five rows came from an unrecorded session (differences of 2-25 percent
   from the recorded medians, e.g. odd-ring CP-SAT 0.429 recorded vs 0.371
   tabulated). v8 tabulates the recorded medians and names the report in
   the caption; the peak-memory claim becomes the recorded 100.2 MiB (the
   v7 text said "about 101 MiB").
3. The Table 6 caption's UNK definition ("returned UNKNOWN within their
   limit") was factually wrong for the two n=18 CP-SAT cells: the n=18 same
   run was killed at the ninety-second hard process cap (returncode -9, no
   payload), and the n=18 split run returned UNKNOWN after overshooting its
   soft sixty-second solver limit (73.1 s solve time, 90.05 s wall). v8
   relabels the n=18 same cell TMO, redefines UNK/TMO truthfully, and
   discloses the two-tier limit (60 s hard kill for subprocess solvers;
   60 s solver limit + 90 s hard cap with 30 s startup-and-construction
   grace for the in-process CP-SAT/HiGHS runners and the bounded native
   runner) in Subsection 13.1, the Table 6 caption, the observations
   paragraph (dropping the unsupported "model construction consumes a
   substantial share of its budget" claim; the recorded build times are
   4.5-8.2 s against 40-90 s walls), and the appendix protocol paragraph.
4. The replication paragraph claimed "every structural field identical;
   the only differences are certificate file names". The actual
   `diff_reports.py` output is 29 mismatches in three classes (file names,
   recorded-only provenance notes, hardware RAM figure). v8 states all
   three classes and the fuller SHA-256 spot-check list (dense-8/16 same,
   ten-bar same, lattice C2 split, and the three completed dense-17/18
   certificates).
5. The OOM description "about 3.75 GiB resident" mis-converts the kernel
   line `anon-rss:3750608kB` (KiB): the anonymous resident set is 3.58 GiB
   (3.84 GB). v8 quotes the kernel figure and converts correctly (about
   3.6 GiB). The deposited `_FAILED` record's own "3.75 GiB" phrasing is a
   decimal-GiB slip; the record is byte-preserved and is not edited.
6. "Debian GNU/Linux 13" was asserted nowhere in the recorded artifact
   (the protocol block records glibc 2.41, kernel 5.10.134, Python 3.12.14;
   the kernel string is an al8 build). v8 reports exactly the recorded
   fields.
7. The Table 2 scope-only lattice rows tabulated treewidths 17 and 23 while
   the artifact's recorded width field for those cases is the
   influence-scope size (18 and 24 actuators; every certified row's scope
   is the full actuator set, so the primal graph is complete and forces
   treewidth 6C-1). v8 keeps the treewidths and states in the caption what
   is recorded and what is implied.
8. Display-convention slips: the chain-pretension row of Table 3 was
   labelled "0 (= full)" although both rungs certify and the caption's
   compression convention requires "0--full" (displayed so, with the rung
   coincidence explained in the caption); the chain n=8 row of Table 2
   showed a single 0.000 DP/verify pair instead of the recorded
   0.000 / 0.001 values.
9. The two overfull hboxes carried since v5 (the SPARSIFICATION-BATCH cell
   and the Theorem 4.2 proof paragraph) are resolved (an \allowbreak in the
   typewriter token and \emergencystretch 1em); v8 compiles under tectonic
   with zero overfull boxes, all \ref/\cite keys resolved, and no new
   warnings.

## 4. Verification of v8

`tectonic monograph-2-algorithms-and-certificates-v8.tex` (with appendix v7
alongside) compiles with 0 errors and 0 overfull boxes; the remaining
underfull hboxes are the pre-existing narrow-p-column cases of the
certificate grammar table. A structural re-check of the PDF confirms the
appendix A content (instance format through claim boundary, including the
dense-extension subsection) is present, the bibliography resolves, and the
Table 6 marker legend matches the relabelled cells.

## 5. Repository deposit

New files only (nothing overwritten): `companion monograph/
monograph-2-algorithms-and-certificates-v8.tex`, `companion monograph/
companion-artifact-appendix-v7.tex`, this report, plan v22, and the
repository worklog round 4. No recorded artifact, report, or earlier
manuscript version is modified.

## 6. Remaining items

1. the archival DOI is assigned and inserted at publication time
   (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. the release manifest refresh is to be frozen at the next artifact
   release, incorporating the v2 replication and dense-extension outputs;
4. the deposited implementation reports v7 ("about 101 MiB") and v9 (the
   "UNK 90.0 s" presentation of the killed n=18 same CP-SAT run) remain as
   historical records; the v8 manuscript states the recorded values and
   the precise semantics, and this report records the divergence.
