# Verification of `humanized halting.txt` against the latest manuscript

Baseline checked: `/home/user/uploads/humanized halting.txt`  
Latest formal manuscript checked against: `/home/user/manuscript-revised-v8.tex`

## Executive assessment

`humanized halting.txt` is useful as a reader-facing orientation document, but it is not a faithful replacement baseline for the current journal manuscript. It is heavily condensed, uses informal pedagogical devices, has obsolete section numbering and citation numbering, and omits many formal definitions, hypotheses, caveats, and results added in the latest manuscript versions.

The latest manuscript already incorporates the legitimate accessibility improvements from the humanized text in formal journal style: the introduction now explains the guiding local-to-global question; the relation-to-established-frameworks section explicitly situates the paper relative to database joins, sheaf-theoretic contextuality, Bell/Fine/local polytopes, Weihrauch reducibility, domain theory, extensive-form games, and partial-order concurrency; and the section openings for context diagrams, distributed selectors, Bell coupling, effectivity, and causal arenas are more readable.

The uploaded humanized file should therefore be treated as a draft reader's guide or expository sketch, not as a manuscript baseline.

## Major technical misalignments

### 1. Loss codomain is wrong

In the humanized file, Definition 3.1 gives

\[
\ell:R\times Y\to[0,\infty).
\]

The latest manuscript uses

\[
\ell:R\times Y\to[0,\infty].
\]

The extended codomain is intentional and aligns static prediction losses with arena losses. The humanized file would reintroduce the earlier codomain inconsistency.

### 2. Exactness is treated too implicitly

The latest manuscript distinguishes a typed prediction game from an exact typed prediction game. The humanized version does not clearly preserve this convention throughout. In particular, zero-loss selector statements should explicitly assume exactness.

### 3. The proof of the prediction-game selector representation is incomplete

The humanized proof says to apply the selector lemma with policy class \(S_\Pi\), but does not define

\[
S_\Pi=\{s_\pi:\pi\in\Pi\}\subseteq(R\times A)^Z.
\]

The latest manuscript includes this principal-selector image and therefore type-checks.

### 4. Compactness theorem statement/proof mismatch

The humanized theorem states closedness of \(\operatorname{Val}_\varepsilon(w)\), but its proof invokes lower semicontinuity without listing it as an assumption. The latest manuscript states both the closed-sublevel assumption and lower semicontinuity as a sufficient condition.

### 5. Past-factorisation interface gap reappears

The humanized file defines a cut interface \(I_\tau\) but does not state whether it is the game interface or a new interface for a cut-indexed game. The latest manuscript fixes this by saying that `cor:pastcone` applies to the game whose interface is \(I_\tau\), or to the original game when \(I_\tau=I\).

### 6. Incorrect claim about fibre-indexed presentations and \(\mathsf D\)

The humanized file says:

> Both presentations recover the same capability predicate. But they diagnose failures differently. The fibre-indexed presentation can show \(\mathsf D\) (if contexts overlap); the terminal presentation cannot.

This is incorrect. The fibre-indexed single-observer presentation is discrete and has no compatibility obstruction in ZFC. \(\mathsf D\) appears in overlapping contextual/distributed incidence diagrams, not in the discrete fibre-indexed presentation.

### 7. Acyclic gluing is overstated

The humanized text says acyclic structures always glue. The current theorem requires acyclicity plus separator/projection consistency. The latest manuscript uses the safer phrase “separator-consistent local tables.”

### 8. Triangle obstruction is described as “topological” without support

The parity triangle is a combinatorial parity-cycle obstruction. It can be related to topological or cohomological methods in broader settings, but the theorem in this article proves only the parity contradiction. The current manuscript avoids overclaiming.

### 9. Bell citations and numbering are inconsistent

The humanized text cites Fine as `[8]`, but its reference list has Fine at `[5]`. It also cites `[19]` for Weihrauch while the reference list has only 18 entries. The LaTeX manuscript uses keyed citations and has no undefined citations.

### 10. Weihrauch explanation is too absolute

The humanized file says the task “cannot be done by any algorithm, but can be done with a \(\mathsf{WKL}\)-oracle.” The correct statement is representation-sensitive: the multivalued operator has Weihrauch degree \(\mathsf{WKL}\). Some particular instances may have computable solutions; the fixed DNR instance is not itself a Weihrauch-complete input-uniform problem. The latest manuscript states this distinction.

### 11. Primitive-recursive separation is underspecified

The humanized summary does not distinguish the recursive Ackermann-style class-separation example from the primitive-recursive presentation language used in the \(\Sigma^0_3\)-completeness theorem. The latest manuscript explicitly separates these.

### 12. \(\Sigma^0_3\)-completeness is too compressed

The humanized version omits the index-set convention, malformed-code convention, decidability of well-formedness, fixed pairing of policy indices, and tagged universal variables. These are present in the latest manuscript.

### 13. Recall theorem loses the global-recall qualification

The humanized theorem says “with information recall,” but the latest manuscript correctly says “global predictor-level information recall.” The distinction from player-relative perfect recall is essential.

### 14. One-shot and finite-II equivalences lose diagnostic caveats

The humanized version says distributed selectors and one-shot arenas are equivalent for capability, but it does not consistently preserve the caveat that this is not a diagnostic equivalence between the CSP incidence presentation and the full arena patch-site presentation.

### 15. Formal verification section is much less precise

The humanized file shortens the formal-verification section and drops the detailed list of which results are not machine-checked. The latest manuscript is more accurate about artifact scope.

## Significant content dropped or condensed relative to the latest manuscript

The humanized file omits or substantially condenses the following legitimate content from the latest formal manuscript:

1. Full LaTeX theorem/proposition numbering and labels.
2. Observational policy quotient details, including saturation caveat.
3. Full robust section/display-map semantics.
4. Monotonicity and interface-refinement hypotheses in full typed form.
5. Robust singleton-validity sets and robust fibre-intersection lemma.
6. Randomised-choice instantiation details.
7. Complete context-diagram formalism with subfunctorial descent systems.
8. Initial-object collapse in its non-subfunctor and subfunctor forms.
9. Effective and bounded realisation maps in full generality.
10. Tolerance-filtered diagrams and endpoint membership caveat.
11. Capability/global-family/diagnostic equivalence distinctions.
12. Global-family functoriality under admissibility-preserving natural transformations.
13. Diagnostic-data versus certificate-data distinction.
14. Obstruction spectrum, compression thresholds, idempotence, and Boolean signature.
15. Full diagnostic partition proof.
16. Constraint-datum invariance and solution-saturated recovery.
17. One-observer recovery with correct common-choice terminology.
18. Finite distributed NP-completeness proof details.
19. Full empirical support packaging, including restricted supports on all downward-closed contexts.
20. Empirical packaging/distributed-selector comparison.
21. Full finite solution-count theorem.
22. Source integration as a distributed selector and source-integration diagnostics.
23. \(\#\mathrm P\)-completeness of counting source integrations and compatible families.
24. Affine global-assignment clarification and cokernel proof details.
25. Empty-non-tree-edge convention for holonomy.
26. Bell matrix definition and rational Farkas certificate details.
27. Represented-space conventions for Weihrauch results.
28. Fixed computable tree versus input-uniform represented tree distinction.
29. Deterministic-time resource separation with union over constant factors.
30. Full \(\Sigma^0_3\) construction and many-one hardness proof.
31. Path-characterisation lemma for arena reachability.
32. Full backward-solvability recursion.
33. Quotient backward induction and record congruence.
34. Information-saturated patch formalism and behavioural-coordinate sheaf.
35. Capability monotonicity under information refinement.
36. Reachable-action collapse criterion.
37. World-scheduled one-pass arenas.
38. Explicit-table NP-completeness proof by direct explicit-arena reduction.
39. Static-compilation composition theorem.
40. Complete finite-poset operational semantics, including complete-profile loss.
41. Operational decoupling and observation-preserving no-go theorem.
42. Trace-relative past factorisation and trace-slice obstruction.
43. Bounded-height countable arena definitions and effective cover/locator theorem.
44. WKL upper bound for represented causal selection.
45. Full formal-verification scope statement.

Because of these omissions, the humanized file is not suitable as a full manuscript baseline.

## Content from the humanized file worth retaining conceptually

The following ideas are useful and are already incorporated in the latest manuscript in a more formal style:

1. The opening intuition: observing through an interface forces equal treatment of worlds with the same observation.
2. The distinction between local failure, compatibility failure, effectivity failure, and resource failure.
3. The explanation that presentation relativity is structural rather than an error.
4. The local-assignment/global-section intuition for context diagrams.
5. The distributed-observation intuition: overlapping contexts require agreement.
6. The Bell explanation in terms of a probability measure over deterministic response tables.
7. The computability explanation: set-theoretic valid sections may exist without computable selectors.
8. The causal explanation: arenas are fixed before strategies and perfect-information cases are governed by backward induction.

The latest manuscript preserves these points without using informal “Inspector” narration, self-referential headings, or change-log language.

## Material not suitable for the journal manuscript as written

The following features of the humanized file conflict with the requested journal style:

- “Layout” table with informal navigation language.
- Running examples named “The Inspector” and “The Team.”
- “In plain terms,” “Back to the Inspector,” “What this teaches,” and similar pedagogical callouts.
- Informal phrases such as “If you read only one lemma,” “no matter how clever,” and “This is the single most important example.”
- Mixed-gender pronoun drift in the Inspector example.
- Numbered bracket citations that do not align with the bibliography.
- Markdown formatting rather than the article’s LaTeX theorem environment.

These can be useful for talks, a blog post, lecture notes, or an extended reader’s guide, but not for the formal manuscript.

## Conclusion

`humanized halting.txt` should not replace `manuscript-revised-v8.tex`. It is a condensed expository synopsis with several technical misalignments and many omissions. The current manuscript already contains the legitimate humanizing content in a more accurate form. No additional restoration from `humanized halting.txt` is needed in the formal article, except possibly continued light polishing of section-opening prose in the same restrained style used in v8.
