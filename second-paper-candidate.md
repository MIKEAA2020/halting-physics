# Candidate second article: Functorial and compositional effective causal descent

## Working title

Functorial Effective Causal Descent: Morphisms, Composition, and Section Semantics for Prediction Presentations

## Rationale

The current article develops presentation-relative diagnostics and concrete representation theorems for selectors, contextual diagrams, distributed CSPs, finite arenas, and guarded causal posets. A separate article can develop the morphism-level theory: functoriality, compositionality, and categorical semantics of the same constructions. This separation keeps the present article theorem-focused while giving the broader program a precise mathematical target.

## Central aim

Define categories of presentations and structure-preserving morphisms for which the assignment

\[
P\longmapsto
\left(\Gamma_{\mathrm{set}}(P)
\supseteq
\Gamma_{\mathrm{eff}}(P)
\supseteq
\Gamma_{\mathcal B}(P)
\right)
\]

is functorial, and determine which additional local-incidence data are required to preserve diagnostics, certificates, and quantitative spectra.

## Core questions

1. Which morphisms of constrained diagrams preserve global-family spaces?
2. Which morphisms preserve the full diagnostic datum, including objectwise local success?
3. Which morphisms transport certificates rather than only diagnostic labels?
4. Under what conditions is terminal compression an idempotent functor or reflector onto terminal presentations?
5. Which object-level equivalences in the current article lift to equivalences of categories or groupoids?
6. How do parallel, sequential, and guarded-feedback composition interact with the four diagnostics?

## Proposed theorem package

### 1. Category of constrained presentations

Define a category whose objects are constrained diagrams with realisation data and whose morphisms are admissibility-preserving natural transformations together with compatible implementation maps.

Expected theorem: the nested global-family assignment is a functor to the category of nested triples.

### 2. Diagnostic-preserving morphisms

Define diagnostic morphisms as morphisms preserving local-success data in addition to nested global spaces.

Expected theorem: diagnostic isomorphisms preserve and reflect
\(\mathsf L,\mathsf D,\mathsf K,\mathsf R,\checkmark\).

### 3. Certificate-enriched obstruction data

Develop an objectwise local-incidence structure recording local admissible sets, restriction maps, and realisation of local elements by global sections.

Expected theorem: enriched isomorphisms transport local certificates, compatibility certificates, effective witnesses, and bounded witnesses.

### 4. Terminal compression as an idempotent functor

Define a terminal-diagram construction from nested triples and prove

\[
\Gamma\circ\mathrm{Term}=\mathrm{Id},
\qquad
\operatorname{ExtComp}=\mathrm{Term}\circ\Gamma,
\qquad
\operatorname{ExtComp}^2=\operatorname{ExtComp}.
\]

Relate this functorial idempotence to the spectrum-level compression theorem in the present article.

### 5. Empirical-support packaging under specified morphisms

Choose a precise class of empirical-model morphisms, beginning with support isomorphisms and then considering non-invertible reindexing maps.

Expected theorem: support-isomorphism packaging is functorial and preserves global sections and strong contextuality.

### 6. Distributed selectors and blind-order arenas as a groupoid equivalence

Restrict to reduced finite distributed selectors with realised observation sets and to blind-order one-shot arenas in strict normal form.

Expected theorem: the object-level normal form of the current article lifts to an equivalence of groupoids under structure-preserving isomorphisms.

### 7. Arena patch sheaves under arena isomorphisms

Define finite arena isomorphisms preserving worlds, tree structure, nature maps, information sets, choices, and losses.

Expected theorem: the patch-sheaf and activated-validity constructions are functorial under these isomorphisms and preserve pure capability.

### 8. Compositional laws

Develop sufficient conditions for:

- disjoint union / product of independent presentations;
- conjunction of constraints over common variables;
- sequential composition of guarded tasks;
- static compilation composition;
- guarded feedback composition over finite posets.

Expected theorem: capability and the nested success spectra compose under specified independence and resource-separation hypotheses.

## Material not to include without additional source-domain semantics

The second article should not assert broad placements of no-cloning, Bell nonlocality, Gödel incompleteness, distributed consensus, or quantum measurement unless the relevant source-domain morphisms and operational success predicates are fixed. Such examples can be stated as targets for representation theorems, not as consequences of the abstract framework alone.

## Relationship to the current article

The current article supplies the object-level and example-level theory: selector kernels, presentation-relative diagnostics, compression boundaries, finite CSP/contextual/Bell examples, computability and resource separations, finite arenas, and causal-poset realisations.

The second article would supply the morphism-level theory: functoriality, certificate transport, categorical equivalences, and compositional laws.
