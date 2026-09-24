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

---

## Round 4 — audit of v7 against the deposited artifact; companion monograph v8 / appendix v7

- A line-level audit of the v7 manuscript and appendix v6 was executed
  against the artifact ground truth now in the repository: every recorded
  number cited by the manuscript was re-derived from the deposited JSON
  reports (mechanics benchmarks, sparsification study, recorded and v2
  sweeps, dense-extension generation and sweep, large-artifact manifest,
  controlled-width external baselines, repro gate) and the harness source
  (limit semantics, CP-SAT status mapping, evidence-gated agreement
  counter).
- Confirmed correct: the withdrawal of the v6 "corrected accounting"; all
  cells of Tables 2, 3, 5, and 6; the extension widths, certificate sizes,
  accounting, and manifest; the FE preprocessing times and the replication
  summary.
- Residual flaws corrected at the root in v8 / appendix v7 (new files;
  nothing overwritten): v7 still input appendix v5 so the compiled v7
  document omitted the entire v6 appendix content; Table 4 carried medians
  from an unrecorded session instead of the recorded report (now
  tabulated from `reports/external_baseline_sweep.json`, with the recorded
  peak memory 100.2 MiB); the extension table's UNK legend was factually
  wrong for the two n=18 CP-SAT cells (one killed at the ninety-second
  hard cap, one UNKNOWN after the soft solver limit was overshot) and is
  relabelled and redefined with the two-tier limit disclosed; the
  replication comparison now states all three mismatch classes found by
  `diff_reports.py` (29 mismatches, not just file names); the OOM resident
  set is quoted from the kernel line and converted correctly (about
  3.6 GiB, not 3.75); the unsourced "Debian GNU/Linux 13" claim is dropped
  in favour of the recorded protocol fields; the scope-only lattice rows
  now state that the artifact records the influence-scope size (18/24)
  while the tabulated 17/23 are the implied treewidths; the chain-pretension
  rung range and the chain n=8 split timings are displayed per the stated
  conventions; the two overfull hboxes carried since v5 are resolved (v8
  compiles with zero overfull boxes).
- Deposited: `companion monograph/monograph-2-algorithms-and-certificates-v8.tex`,
  `companion monograph/companion-artifact-appendix-v7.tex`,
  `finite-ecd-prototype-implementation-report-v10.md`, plan v22, and this
  round's worklog entry. No recorded artifact or earlier version was
  modified.

## Round 5 — Lean-availability statement (main monograph v42) and environment-provenance restoration (companion v9)

- Owner directive: claims whose verification happened but whose sources did
  not persist are factual and stay in the manuscripts; their loss is stated
  in an availability statement, not repaired by deletion. Two mis-corrections
  of the previous round are withdrawn under this rule, and the remaining
  line-level flaws of monograph-revised-v41.tex are fixed at the root.
- Main monograph v42 (new file; v41 unchanged): the Formal verification
  section keeps every Lean claim verbatim and gains an "Artifact
  availability" paragraph — the twenty-four core Lean files,
  theorem_D_tri.lean, research/mathlib/k_game.lean, the twelve Python
  experiments, and the Lean 4.33.0 / Python 3.13 environment did not persist
  and are not in the deposit; the gate was executed and passed, so the
  formal statements are machine-checked but not presently re-executable; the
  repository's available reproduction entry point is the companion
  prototype's make reproduce gate (Python 3.12.14), a separate artifact that
  does not re-run the Lean checks. The audit's earlier "Python 3.13 vs
  3.12.14" conflict is resolved as a non-conflict (different artifacts,
  different environments), so no version number was altered.
- Citation policy completed in v42: Hoeffding 1963, König 1927 (+ Simpson
  2009 for the WKL/RCA_0 usage), Karp 1972 (3SAT), Tovey 1984
  (distinct-variables 3SAT), and Valiant 1979 (#3SAT) are now cited where
  invoked; six bibitems added (28 total), all cited, all resolved.
- All eleven floats of the main monograph are now referenced in the text
  (seven were unreferenced in v41, including the notation table); companion
  naming is unified to "companion algorithmic monograph" with an explicit
  version pin (v8 / appendix v7); prop:nonembedded's definitional first
  claim is restated as such.
- Companion v9 (new file; v8 unchanged): the Debian GNU/Linux 13 platform
  claim dropped in v8 is restored — the recorded protocol block's `os` field
  carries only "glibc 2.41", so the distribution name is an operator-side
  environment fact; v9 states the machine-recorded fields and the
  operator-recorded distribution name separately instead of deleting the
  platform fact. Nothing else changes; appendix v7 is untouched.
- Verification: tectonic compiles v42 (exit 0; 27 overfull / 172 underfull —
  exactly v41's pre-existing profile; zero undefined refs/cites) and v9
  (exit 0; zero overfull; warning list byte-identical to v8's modulo the
  filename). Deposited: `main monograph/monograph-revised-v42.tex`,
  `companion monograph/monograph-2-algorithms-and-certificates-v9.tex`, plan
  v23, and this worklog entry. No recorded artifact or earlier version was
  modified.

---

## Round 6: pedagogical, game-theoretic, and visual enhancements (v10 / v43)

Owner question: do the main or companion monographs merit additional
non-decorative pedagogical/expository/physical/game-theoretic
enhancements, additional non-decorative tables/figures/visual aids, or
supplements with delegation? The assessment round identified six genuine
gaps (and an explicit do-not-add list: no intuition glosses on the
presentation-relative diagnostic, no in-scope game theory beyond the
books' own fences, no timing plots, no forced delegation out of either
book). Implemented in the agreed order:

- Companion v10 (new file; v9 unchanged): Example 6.4 works a
  hand-verifiable four-variable dynamic program end to end (message
  tables nu_1=(1,0), nu_2=(1,1), root value 2, optimal sections
  (1,0,0,1)/(0,1,1,0), brute-force cross-check, DP-OPTIMUM and
  DP-REFUTATION certificate readings, weighted width 2); Figure 1 is a
  five-panel structural schematic of the two-spring demonstrator and the
  four benchmark families drawn after mechanics_gen.py (ten-bar 3x4 bays
  with 3-4-5 diagonals; pretension chain with self-equilibrated pairs;
  dense chain with alternating stiffnesses; two-bay-row cross-braced
  lattice); Section 10 gains a physical reading paragraph mirroring the
  foundational monograph's Bell reading (the obstruction sits in the
  observation map, not the mechanics; the repairing sensor is an
  instrumentation decision with certified justification); Section 9 gains
  Table `tab:ladder-outcomes` with the three certificate-bearing ladder
  outcomes, refinement stability, and the new certified cost bracket
  min_{Gamma^+_J} kappa <= min_{Gamma^true} kappa <= min_{Gamma^-_J}
  kappa. All example arithmetic was machine-verified by brute force
  before insertion; the example is scoped as pedagogical, not a recorded
  artifact run.
- Main v43 (new file; v42 unchanged): Remark 12.59 unifies verified
  certificates with winning pure strategies in the tabular verifier game
  of Theorem 12.40 (policy = winning strategy, refutation = no winning
  strategy, inconclusive = absence of a game-outcome certificate); the
  functorial chapter gains its first commutative diagrams (the naturality
  square of the base-isomorphism definition and the retraction square +
  idempotence triangle of the terminal-compression theorem, via tikzcd);
  the companion version pin is bumped to v10 / appendix v7 per the v23
  remaining-items list.
- Verification: tectonic compiles v10 (zero errors, zero overfull, v9's
  underfull sites unchanged plus one benign site of the grammar table's
  pre-existing class; zero undefined references; figure/table/example
  pages visually verified) and v43 (zero errors, zero undefined
  references; exactly v42's nine overfull lines at shifted positions,
  with the +2/+13/+35/+53 offsets matching the inserted line counts;
  diagram and remark pages visually verified). Appendix v7 is untouched.
- Deposited: `companion
  monograph/monograph-2-algorithms-and-certificates-v10.tex`, `main
  monograph/monograph-revised-v43.tex`, plan v24, and this worklog entry.
  No recorded artifact or earlier version was modified.

## Round 7: four-part owner audit and structural implementation (companion v11 / appendix v8 / main v44)

A five-way line-level audit (remnants ×2, clarity/flow ×2, cross-book
alignment ×1, all spot-verified) found: main v43 remnant-clean with three
moderate defects; companion v10 remnant-clean with one major-severity defect
(the §13↔Appendix A duplication cluster); the roadmap and Conclusion both
omitting the entire functorial tier; one unparseable orphan paragraph in the
definitional heart; and a set of precision-level gaps. The withdrawn-footnote
passage of §13.2 was re-reviewed against the v4-tag artifact source and
confirmed accurate in all four forensic claims.

Implementation per repo convention (new version files, nothing overwritten):

- `companion monograph/companion-artifact-appendix-v8.tex`: §13↔A
  consolidation back-pointers (\ref-based), phase-4 gloss, "new subsection"
  fix; operational content unchanged.
- `companion monograph/monograph-2-algorithms-and-certificates-v11.tex`:
  §13↔A consolidation (§13.1 canonical, replication list and archive-policy
  mechanics delegated), §1 sensor-repair contribution item + roadmap clause +
  main-v44 pin, §9 purpose-first opening + Γ^true binding + numeric-domains
  qualifier move, W/o=obs/O_j/κ notation fixes, §10 seam clause and dedup,
  §12 Table-1 citation + zero-extension gloss, verification-gate table
  captioned as Table 5 with the Remark 3.1 pointer, Table 8 referenced,
  repository URL inserted, withdrawal-footnote micro-edits, \input bumped to
  appendix v8.
- `main monograph/monograph-revised-v44.tex`: roadmap fourth stage + §4
  clause + scope-paragraph companion disclosure + Conclusion final paragraph
  (the bracketing fix), orphan patch-category paragraph relocated to the
  full patch-site collapse corollary, §11 subdivided 6→14 subsections
  (six new headings + three promoted \paragraph units; no theorem numbers
  move), §12.13 orientation sentence, "companion morphism theory" →
  "accompanying", inner–outer twin cross-link, pins bumped to v11/v8,
  repository URL in the availability paragraph, DNR/PA/CHSH/PR expansions +
  Popescu–Rohrlich bibitem, represented-realisation scope clause, §12
  re-derivation citations (def:morphism-levels and the functor proof),
  CHSH recollection compression, def:epsEC commentary relocation +
  punctuation fix, variance-recollection trim, "below" markers,
  rem:ladder/tab:presentations anchor, monograph lexicon unification,
  -ize/-ise and French-spacing normalization, blank-run collapse.
- plan v25 records the audit basis, all changes, verification, and remaining
  items (round-8 incorporation candidates remain owner decisions).

Verification: tectonic compiles main v44 with exactly v43's warning profile
(same nine overfull lines shifted, same 172 underfull lines, zero errors,
zero undefined references) and companion v11 with v10's underfull set and
zero overfull boxes; all new cross-references resolve in both PDFs; the
withdrawal footnote, both version pins, and the two repository URLs render
correctly. No recorded artifact or earlier version was modified.

## Round 8: Round-8 candidate incorporation, register scan, and mutual re-pinning (companion v12 / appendix v9 / main v45)

Owner directives: include the round-8 incorporation candidates only if
highly merited; address remaining plan-v25 points at root cause; address
the withdrawn footnote if there is still defect; scan for meta-commentary,
informal chat jargon, self-referential or editorial comments, over-hedging,
and internal jargon.

- Re-downloaded the workspace release and mined the companion source draft
  again for the six ranked candidates. Adjudication: three included
  (finite effective collapse proposition, relation-to-prior-work passage,
  observation-identification width warning), three declined with documented
  reasons (sensor-design hardness and the FPT framing are gated on writing
  complete reductions; the claim-boundary anchor bibitems would decorate
  declined-scope statements).
- Companion v12: new §1 subsection "Relation to prior work" (seven new
  bibitems, all load-bearing in the passage; honest novelty boundary: the
  engines are classical, the assembly and its recorded execution are the
  contribution); new §2 Proposition (Finite effective collapse) + remark
  (unrestricted catalogues collapse the set/effective distinction; the
  remaining separations are declared-catalogue and budget; a timeout or
  table-size limit is inconclusive, not evidence of non-existence); new §5
  Proposition (Identification can destroy low width) + remark (primal graph
  defined at first use; the matching→quotient construction; the
  graph-colouring hardness instantiation citing gareyjohnson79; width is
  measured after the identifications the interface enforces); §11's
  same/split definition gains the identification cross-reference and the
  minimum-fill heuristic gains the George/Lipton–Tarjan citation; register
  fixes (phase-6 gloss, ETH/FE/OOM expansions, "the artifact release", two
  pre-introduction "artifact report" captions → "the artifact's recorded
  reports", DP-OPTIMUM grammar+width-DP double citation, seven -ize
  normalisations, five quantized→quantised, spaced em-dash); pin bumped to
  main v45; \input appendix v9.
- Appendix v9: the dense-family subsection gains a label and the positional
  "subsection below" self-reference becomes a cross-reference; otherwise
  unchanged.
- Main v45: the relation subsection gains the decentralised-control
  paragraph (Witsenhausen, Papadimitriou–Tsitsiklis, Bernstein et al.;
  three new bibitems, all cited); WKL expanded at first use (abstract and
  §1), CSP parenthesised, MILP expanded; register fixes from the scan
  (realisation/realises, accompanying algorithmic programme, normalised,
  temporal "now" dropped, "The common content of these results"); pins
  bumped to companion v12 / appendix v9.
- Withdrawn-footnote re-verification: counters internally consistent, both
  round-10 micro-edits in place, cross-references resolve, "this article"
  consistent with the companion's self-reference lexicon; verdict: no
  remaining defect, no edit made to the passage.
- Register-scan false positive documented: the appendix's
  VERIFIED-SAT/VERIFIED-UNSAT tokens are genuine recorded artifact field
  values (repro_report.json), correctly documented, retained.

Verification: tectonic compiles main v45 with exactly v44's nine-overfull
profile at shifted positions (identical badness values; zero errors, zero
undefined references) and companion v12 with exactly v11's five-warning
underfull class at shifted positions (zero overfull, zero errors, zero
undefined references); pdftotext confirms every insertion renders,
including both version pins (12/9) and all ten new bibitems; mechanical
checks: 47 labels / 24 cited bibitems (companion + appendix), 302 labels /
32 cited bibitems (main), no duplicate labels, no stale references. No
recorded artifact or earlier version was modified.
