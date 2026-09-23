# Candidate second article: Functorial and compositional effective causal descent

## Working title

Functorial Effective Causal Descent: Morphisms, Composition, and Section Semantics for Prediction Presentations

## Central thesis

A broad class of prediction, synthesis, inference, and control tasks can be treated as effective local-to-global section problems once their observation contexts, admissibility constraints, implementation maps, and resource filters are specified. The first article develops the object-level diagnostic theory. The second article should develop the morphism-level theory: functoriality, certificate transport, compositionality, and representation theorems.

The guiding distinction is:

\[
\text{capability preservation}
\quad\neq\quad
\text{diagnostic preservation}
\quad\neq\quad
\text{certificate preservation}.
\]

## Core formal object

Define an effective causal section presentation as data

\[
P=(\mathcal C,\mathcal A,\LocalAdm^\varepsilon,
\mathrm{Impl}_{\mathrm{eff}},\mathrm{Impl}_{\mathcal B},
\sigma_{\mathrm{eff}},\sigma_{\mathcal B}),
\]

where:

- \(\mathcal C\) is a context category or site;
- \(\mathcal A:\mathcal C\to\mathbf{Set}\) is an assignment functor, or equivalently a presheaf under the opposite-arrow convention;
- \(\LocalAdm^\varepsilon(c)\subseteq\mathcal A(c)\) are tolerance-indexed local validity/admissibility sets;
- \(\sigma_{\mathrm{eff}}\) and \(\sigma_{\mathcal B}\) are realization maps into the ambient family space;
- the nested global spaces are

\[
\Gamma_{\mathrm{set}}^\varepsilon(P)
\supseteq
\Gamma_{\mathrm{eff}}^\varepsilon(P)
\supseteq
\Gamma_{\mathcal B}^\varepsilon(P).
\]

A more structured version may separate local validity \(\mathsf V^\varepsilon\) from structural admissibility \(\mathsf A\):

\[
\Gamma(\mathcal C,\mathsf A\cap\mathsf V^\varepsilon).
\]

This separation is useful for nonanticipation, no-signalling, protocol legality, and architectural constraints that are not themselves computability or resource conditions.

## Principal theorem targets

### 1. Global-family functor

Define a category \(\mathbf{Pres}_{\mathcal C}\) of constrained presentations over a fixed context category. A morphism

\[
f:P\to Q
\]

should consist of:

1. a natural transformation \(\alpha:\mathcal A^P\Rightarrow\mathcal A^Q\);
2. admissibility preservation

   \[
   \alpha_c(\LocalAdm_P^\varepsilon(c))
   \subseteq
   \LocalAdm_Q^\varepsilon(c);
   \]

3. compatible maps on effective and bounded implementation objects.

Expected theorem:

\[
P\mapsto
(\Gamma_{\mathrm{set}}^\varepsilon(P)
\supseteq
\Gamma_{\mathrm{eff}}^\varepsilon(P)
\supseteq
\Gamma_{\mathcal B}^\varepsilon(P))
\]

is a functor to the category of nested triples.

### 2. Diagnostic-preserving and certificate-preserving morphisms

Define three increasingly strong morphism classes:

1. capability morphisms: preserve strategy/policy spaces and worldwise loss;
2. diagnostic morphisms: preserve the obstruction datum

   \[
   (\lambda_\varepsilon,
   \Gamma_{\mathrm{set}}^\varepsilon
   \supseteq
   \Gamma_{\mathrm{eff}}^\varepsilon
   \supseteq
   \Gamma_{\mathcal B}^\varepsilon);
   \]

3. certificate morphisms: preserve objectwise local sets, restriction maps, and local-to-global incidence.

Expected theorem: diagnostic isomorphisms preserve and reflect

\[
\mathsf L_\varepsilon,
\mathsf D_\varepsilon,
\mathsf K_\varepsilon,
\mathsf R_\varepsilon,
\checkmark_\varepsilon.
\]

Certificate isomorphisms additionally transport finite local certificates, parity certificates, affine certificates, holonomy certificates, and Farkas-type certificates when the relevant algebraic structure is included.

### 3. Terminal compression as an idempotent functor

Define a terminal-diagram functor

\[
\mathrm{Term}:\mathbf{Nested}\to\mathbf{Pres}_{\mathbf 1}
\]

and a global-family functor

\[
\Gamma:\mathbf{Pres}_{\mathcal C}\to\mathbf{Nested}.
\]

Expected theorem:

\[
\Gamma\circ\mathrm{Term}=\mathrm{Id}_{\mathbf{Nested}},
\qquad
\operatorname{ExtComp}=\mathrm{Term}\circ\Gamma,
\qquad
\operatorname{ExtComp}^2=\operatorname{ExtComp}.
\]

This gives the categorical form of the compression-spectrum theorem in the first article.

### 4. Obstruction spectra and decompression fibres

Study the fibre of terminal compression over a compressed spectrum. If

\[
\operatorname{Spec}(\operatorname{ExtComp}(P))
=(S_D,S_D,S_K,S_R),
\]

then the missing datum is any upward-closed \(S_L\supseteq S_D\). Thus decompression has three levels:

1. label decompression: choose the local-success bit \(\lambda\);
2. spectrum decompression: choose \(T_{\mathsf L}\supseteq T_{\mathsf D}\);
3. certificate decompression: choose local incidence and witness structure.

Expected theorem: terminal compression forgets precisely the \(\mathsf D\)-gap at the spectral level and the compatibility-certificate structure at the certificate level.

### 5. Empirical-support packaging under specified morphisms

Define a groupoid of finite empirical support models with:

- measurement bijections;
- context bijections;
- outcome bijections;
- support preservation.

Expected theorem: downward-closed support packaging is functorial on this groupoid and preserves global sections and strong contextuality.

Then consider non-invertible morphisms separately. A non-invertible theory must choose between inverse-image reindexing, direct-image pushforward, and support saturation. These choices lead to different preservation theorems.

### 6. Distributed selectors and blind-order arenas as a groupoid equivalence

Define a groupoid of reduced finite distributed selector problems, where each observation set equals its active image. Define a groupoid of blind-order one-shot arenas in strict normal form.

Expected theorem:

\[
\mathsf N:\mathbf{Dist}_{\mathrm{red}}ightleftarrows
\mathbf{Blind}:\mathsf{Dist}
\]

is an equivalence of groupoids. The equivalence preserves pure strategies, worldwise zero-one loss, and capability. It need not preserve arbitrary diagnostic presentations unless local incidence data are transported.

### 7. Arena patch sheaves under arena isomorphisms

Define arena isomorphisms preserving:

- worlds;
- rooted tree structure;
- node type;
- nature maps;
- information sets;
- choice sets;
- loss tables.

Expected theorem: the patch-sheaf and activated-validity constructions are functorial under arena isomorphisms. The induced sheaf isomorphisms preserve global activated-valid strategies and pure capability.

A broader simulation-style theory should be separated from the isomorphism-level theorem because it requires a direction for strategy transport and loss comparison.

### 8. Static compilations as a category

The first article contains the basic composition law. A second article can develop refinements:

- observation-preserving static compilations;
- resource-overhead-aware compilations;
- diagnostic-preserving compilations;
- certificate-preserving compilations.

Expected theorem: observation-preserving compilations compose when intermediate interfaces match, and resource-overhead functions compose by the relevant monoidal operation.

### 9. Constraint-system composition

Develop compositionality for finite distributed selectors and CSP presentations:

- conjunction over a common variable set;
- disjoint union over independent variable sets;
- pullback/fibre product of presentations over shared interfaces;
- hiding/existential projection of internal variables.

Expected theorems:

\[
\mathrm{Sol}(P\wedge Q)=\mathrm{Sol}(P)\cap\mathrm{Sol}(Q),
\]

\[
\mathrm{Sol}(P\sqcup Q)\\cong
\mathrm{Sol}(P)\times\mathrm{Sol}(Q),
\]

with corresponding laws for diagnostic outcomes under suitable local-nonemptiness and independence assumptions.

### 10. Parallel, sequential, and guarded-feedback composition

Develop a composition theory for effective causal section presentations.

#### Parallel composition

For independent presentations with product loss aggregation, prove sufficient conditions for

\[
\mathrm{Cap}(P)\land\mathrm{Cap}(Q)
\Rightarrow
\mathrm{Cap}(P\otimes Q).
\]

The converse requires hypotheses excluding shared resources, shared randomness, or correlated implementations.

#### Sequential composition

Sequential composition should be formulated by dependent sums or a Kleisli construction, since the second task's interface can depend on the first task's realised report-action pair.

Expected theorem: if a valid section of the first presentation and a compatible family of valid continuation sections for the second presentation exist, then the sequential composite has a valid section.

#### Guarded feedback

Feedback should be guarded by a well-founded dependency relation. The operational poset theorem from the first article supplies the model case. A second article can characterize when section semantics, implementation maps, and resource bounds are preserved under guarded feedback.

## Representation and completeness program

### 1. Behavioral equivalence

Define prediction-relevant behavioral equivalence between games or operational systems. Two systems should be equivalent when they induce isomorphic:

- validity objects;
- admissible global sections;
- implementation images;
- worldwise loss profiles;
- resource filters, up to declared overhead.

This equivalence is weaker than equality of dynamics and stronger than mere equality of yes/no capability.

### 2. Effective-section representation theorem

Formulate a theorem of the form:

\[
\mathbf{Game}_{\mathrm{rep}}/{\simeq_{\mathrm{pred}}}
\simeq
\mathbf{EffCausalSec}_{\mathrm{rep}}.
\]

This requires explicit representability conditions. Separate versions may be needed for:

- finite tabular systems;
- total computable systems;
- partial computable systems;
- cellular automata;
- probabilistic kernels;
- quantum instruments.

The converse construction should build a canonical game from a represented section problem without asserting unrestricted physical realizability.

### 3. Unique first-failure theorem

For a fixed presentation, task, realization map, and resource model, every failure has a unique first failed level:

\[
\mathsf L,
\mathsf D,
\mathsf K,
\mathsf R.
\]

Mechanism-specific certificates, such as cone separation, diagonalization, contextuality, infeasible couplings, and resource lower bounds, witness levels but do not replace the first-failure classification.

## Source-domain representation targets

These targets should be included only after their source-domain semantics and morphisms are fixed.

### 1. Quantum contextuality and Bell nonlocality

Possibilistic contextuality can be represented by support-valued descent. Probabilistic Bell nonlocality requires convex or distributional descent, such as finite probability simplices and coupling diagrams.

Potential theorem: a finite empirical model is strongly contextual exactly when its support-packaging presentation has a \(\mathsf D\) outcome. For general Bell nonlocality, local-polytope membership is equivalent to existence of a global probability coupling.

### 2. Distributed computing and protocol complexes

Define a functor from protocol complexes or task complexes to finite or simplicial section presentations. The target is to represent consensus and set-agreement impossibilities as compatibility, effectivity, or resource obstructions depending on the task and model.

No such placement should be asserted without preserving process views, carrier maps, task specifications, and protocol legality.

### 3. Decentralized control and synthesis

Contexts can be agents' observation histories; admissibility can express nonanticipation and architecture constraints; validity can express robust or expected performance; implementation maps can express controller synthesis in a chosen language.

Potential theorem: modular controller specifications produce \(\mathsf D\) exactly when locally admissible controller fragments have no compatible nonanticipatory joint law.

### 4. Gödel-style diagonal arguments

A Gödel placement requires a precise candidate-decider construction and assumptions distinguishing:

- theoremhood from truth;
- consistency, soundness, \(\omega\)-consistency, or \(1\)-consistency;
- internal representability from external correctness.

A safe formulation is a reduction theorem: from a candidate total decider satisfying specified representability and correctness assumptions, construct a selector instance on which it fails.

### 5. No-cloning and no-broadcasting

No-cloning and no-broadcasting should be treated as restrictions on implementation morphisms or process-theoretic transformations, not as local fixed-point contradictions. A representation theorem would require a process theory with tensor product, states, channels, and a declared success predicate.

## Quantitative and resource enrichment

Extend the obstruction spectrum to resource- and overhead-sensitive morphisms. For a morphism with tolerance overhead \(\rho\), seek implications of the form

\[
\varepsilon\in T_\chi(P)
\Rightarrow
\rho(\varepsilon)\in T_\chi(Q).
\]

For composition, track resource budgets by monoidal operations, e.g.

\[
B_{P\otimes Q}=B_P\oplus B_Q.
\]

This should remain a threshold/spectrum theory, not an additive physical decomposition unless a specific loss and resource doctrine proves additivity.

## Reverse-mathematical and Weihrauch directions

The first article gives WKL upper/equivalence results for binary fibre selection and nested-prefix selection. A second article can ask for exact degrees of broader causal selection classes:

- bounded-height arenas with prefix-correlated validity;
- locally finite arenas with no infinite plays;
- represented patch-sheaf selection;
- computable covers with and without locators;
- distinctions between pointwise computable local sections and uniformly computable matching families.

Potential theorem target: identify a natural represented causal selection problem with Weihrauch degree \(\mathsf{WKL}\), or prove strict upper/lower bounds for bounded-height subclasses.

## Application targets

The source-integration application in the first article can be extended to:

- database repair and inconsistency localization;
- probabilistic data fusion and marginal coupling;
- privacy-constrained integration;
- multi-agent planning under partial observations;
- modular program synthesis.

Each application should specify the presentation, diagnostics, certificates, and morphisms before asserting a placement.

## Deliverables for the second article

A focused second article could contain the following theorem sequence:

1. Category of constrained presentations and global-family functor.
2. Diagnostic and certificate morphisms.
3. Terminal compression as an idempotent functor and decompression fibre theorem.
4. Empirical-support packaging functoriality for support isomorphisms.
5. Groupoid equivalence between reduced distributed selectors and blind-order arenas.
6. Patch-sheaf functoriality under arena isomorphisms.
7. Composition laws for conjunction, disjoint union, static compilation, and guarded feedback.
8. Quantitative spectrum transport under tolerance/resource overhead.
9. One substantial source-domain representation theorem, preferably for finite source integration, probabilistic coupling, or a simple distributed-computing task.

## Exclusion principles

The second article should avoid unrestricted cross-domain claims. A source theorem should be placed in the diagnostic taxonomy only relative to:

- a declared source category;
- a declared target presentation category;
- a translation functor or relation;
- preservation properties;
- a task/evaluation doctrine;
- a proof that the translated obstruction has the claimed diagnostic outcome.

This prevents contrived encodings from turning non-instance claims into syntactic assertions.
