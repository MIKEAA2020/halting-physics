# Second monograph / focused article plan

## Working monograph title

**Algorithms and Certificates for Finite Effective Causal Descent: Width, Counting, Compression, and Certified Mechanical Synthesis**

## Focused article title for applied mechanics

**Certifying Finite Effective Causal Descent for Sensor-Limited Mechanical Systems**

Alternative, more theory-forward title:

**Algorithms and Certificates for Finite Effective Causal Descent: Complexity, Width-Based Tractability, and Applications to Sensor-Limited Mechanics**

## Editorial identity

The companion work should be a proof-producing finite synthesis and computational-mechanics contribution, not a compressed retelling of the foundational monograph. Its core claim should be:

> Finite effective causal descent is a diagnostic-preserving, proof-producing synthesis pipeline for finite mechanical decision systems under partial observation, with explicit complexity boundaries and numerically certified mechanics data.

The focused article should omit the first monograph's broad computability, DNR/PA, Weihrauch, Bell/contextuality, and general causal-composition developments except where they are needed as background definitions. Its novelty should come from finite algorithms, certificates, mechanical admissibility generation, and reproducible implementation.

## Joint adjudication of the companion audits

### Adopt as central

The following audit recommendations are strong and should drive the companion work:

1. Present the companion as a certified computational-mechanics method.
2. Use finite explicit input encodings and avoid infinite computability material.
3. Put one decision variable at each information state after observation identification.
4. Make the width-based certifying solver and independent verifier central.
5. Use weighted state-space width for heterogeneous domains.
6. Include a diagnostic semiring or equivalent one-pass tiered dynamic program.
7. Include inclusion-minimal obstruction cores and minimum-cost repairs.
8. Include exact one-shot sensor repair by hitting-set constraints.
9. Include certified finite-element inner/outer relation generation.
10. Include width-adaptive certified sparsification.
11. Include a small exact mechanical demonstrator.
12. Require numerical experiments before an applied-mechanics submission.

### Adopt as theorem targets with caution

The following are plausible and valuable, but require careful final proofs and references:

1. Schaefer/Zhuk template dichotomy: valid only for fixed-template CSP settings.
2. \(\mathsf D^\mathsf P\) gap detection: needs a fully checked reduction.
3. Uniform acyclicity across set, support, and probability tiers: should be stated as a synthesis of BFMY/Yannakakis/Vorob'ev under precise consistency hypotheses.
4. ETH, W[1], and W[2] lower bounds: need exact parameterization and references.
5. Nested-dissection mechanics bounds: require hypotheses linking mechanical substructure to the policy primal graph.
6. Claimed practical speedups: require benchmark data.

### Do not claim without experiments or additional modelling

1. Scaling superiority over CP-SAT or MILP.
2. Practical effectiveness of sparsification on real mechanical models.
3. Continuum-mechanics validity from finite-element residual bounds alone.
4. Physical infeasibility from conservative inner-model infeasibility.
5. Timeout as a proof of resource non-realisability.

## Core finite presentation

Let \(X\) be a finite set of policy variables. Each variable \(x\in X\) has a finite nonempty domain \(D_x\). In mechanics, a variable often has the form

\[
x=(j,o),
\]

where \(j\) is a controller, actuator, or decision channel, and \(o\) is an information state produced by the available sensors.

A finite descent presentation is

\[
\mathcal P=(X,(D_x)_{x\in X},(S_i,R_i)_{i=1}^m),
\]

where

\[
S_i\subseteq X,
\qquad
R_i\subseteq\prod_{x\in S_i}D_x.
\]

The global policy space is

\[
\Gamma(\mathcal P)=
\{a\in\prod_{x\in X}D_x:a|_{S_i}\in R_i\text{ for every }i\}.
\]

This is the finite form of set-theoretic global families. In an explicitly finite model, ordinary computability collapses with set-theoretic existence unless effectiveness is defined by a finite implementation catalogue or artifact class.

## Finite effectiveness by implementation catalogues

For controller \(j\), let \(\mathcal L_j\) be a finite implementation catalogue with evaluation map

\[
\operatorname{eval}_j(\ell,o)
\]

and cost \(c_j(\ell)\). Introduce implementation variables

\[
\ell_j\in \mathcal L_j\cup\{\bot\}.
\]

The wildcard \(\bot\) is compatible with any behavioral assignment and has infinite cost. Real implementations satisfy

\[
x_{j,o}=\operatorname{eval}_j(
\ell_j,o)
\qquad(o\in O_j).
\]

Then:

- every set-theoretic policy extends by choosing \(\bot\);
- finite-cost extensions are exactly realised policies in the declared catalogue;
- bounded realisability means minimum finite implementation cost at most \(B\);
- complete policy catalogues need not be materialised.

This is the finite analogue of the monograph's realisation-image layer.

## Theorem package A: local fibres, causal compilation, and complexity

### A1. Finite effective collapse without catalogues

For finite explicitly encoded presentations without a restricted implementation catalogue,

\[
\Gamma_{\mathrm{set}}=\Gamma_{\mathrm{eff}}.
\]

Every satisfying assignment is a finite lookup table and hence computable. This does not make synthesis easy; it separates existence from the computational cost of finding a witness.

### A2. Fibre selector algorithm and small certificates

For one-shot observation map \(o:W\to O\), action set \(A\), and scenario-admissible action sets \(S_w\subseteq A\), an observation-uniform policy exists iff

\[
A_o=igcap_{w:o(w)=o}S_w\ne\varnothing
\]

for every realised observation \(o\). With bit-vector action sets this is computed in

\[
O(|W||A|/\omega).
\]

If a fibre fails, a certificate consists of at most \(|A|\) scenarios in one observation fibre, one excluding each action. The bound is tight.

Finding a minimum-cardinality conflict core is a separate optimization problem and should not be promised unless solved; inclusion-minimal or bounded-size cores are sufficient for certification.

### A3. Reachability-correct causal compilation

For an explicitly represented finite history tree with controller information cells and unsafe leaves, introduce one policy variable for each controller information cell. For each unsafe leaf, read the controller actions along its root-to-leaf path.

- If the same information-cell variable occurs with two different required actions on the path, discard the path: no uniform policy can realise it.
- Otherwise forbid the tuple of information-cell actions occurring on that path.

The resulting forbidden-tuple presentation has global assignments exactly the robustly safe observation-uniform policies.

For a history tree of \(N\) nodes and height \(H\), this compilation has size \(O(NH)\) in the explicit trace representation. It does not imply the same complexity for succinctly represented horizons or exponentially unfolded arenas.

### A4. Finite synthesis complexity frontier

For explicit relation tables:

| Problem | Complexity |
|---|---:|
| Verify proposed assignment | P |
| Unary constraints | P |
| Boolean binary constraints | P via 2-SAT |
| Boolean ternary constraints | NP-complete |
| 3-element domains, binary inequality constraints | NP-complete via graph 3-colouring |
| Nonexistence of global assignment | coNP-complete |
| Counting global assignments | \(\#\mathrm P\)-complete |
| Minimum-cardinality fibre obstruction | NP-hard |

The NP-completeness results should be stated under nonempty-local-relation promises to show that hardness is caused by global compatibility rather than local impossibility.

### A5. Promise hardness for finite effectivity and budget tiers

Develop reductions showing:

- catalogue-effective realisability is NP-hard even when \(\Gamma_{\mathrm{set}}\ne\varnothing\);
- budgeted realisability is NP-hard even when \(\Gamma_{\mathrm{eff}}\ne\varnothing\).

These reductions should use finite artifact catalogues, wildcard implementations, and cost ledgers, not ordinary computability.

### A6. Diagram compatibility

For explicit map tables, declared diagram compatibility is polynomial-time checkable by evaluating each declared equation on each source state. A defect certificate consists of:

- an equation \(p=q\);
- a source state \(s\);
- the unequal values \(\rho_p(s)\ne\rho_q(s)\).

If maps are represented by Boolean circuits, compatibility becomes coNP-complete by circuit equivalence. This separates explicit finite encodings from succinct ones.

## Theorem package B: width-based certifying solver

### B1. Tree-decomposition dynamic program

Let \(G_\mathcal P\) be the primal graph. Given a tree decomposition \((T,(B_t))\) of width \(w\) and maximum domain size \(d\), feasibility is decidable in

\[
O((n+m)d^{w+1})
\]

up to table indexing factors. The same dynamic program computes minimum catalogue cost using the diagnostic semiring below.

### B2. Weighted state-space width

For heterogeneous domains, define

\[
\lambda(T)=
\max_t\sum_{x\in B_t}\lceil\log_2|D_x|\rceil.
\]

The state-table size at bag \(t\) is \(2^{\sum_{x\in B_t}\lceil\log_2|D_x|\rceil}\), giving a sharper bound

\[
\operatorname{poly}(|I|,|T|)2^{\lambda(T)}.
\]

This avoids hiding large tuple domains inside apparently small graph width.

### B3. Diagnostic semiring

Use values

\[
(s,c)
\in
\{0,1\}\times(\mathbb N\cup\{\infty\}),
\]

where \(s=1\) means set-theoretic feasibility and \(c\) is the minimum implementation cost, with \(c=\infty\) meaning no finite-cost implementation in the catalogue.

Operations:

\[
(s,c)\oplus(s',c')=(s\lor s',\min(c,c')),
\]

\[
(s,c)\otimes(s',c')=(s\land s',c+c').
\]

Root value interpretation:

| Root value | Diagnostic meaning |
|---|---|
| \(s=0\) | no set-theoretic global section |
| \(s=1,c=\infty\) | set section exists but no catalogue implementation |
| \(c<\infty\) | effective catalogue implementation exists |
| \(c\le B\) | bounded implementation exists |

### B4. DP proof objects

A negative certificate should include:

- a validated tree decomposition;
- factor-to-bag assignment;
- separator message tables;
- root value;
- enough recurrence entries to recompute the DP independently.

The verifier recomputes the recurrence at every bag assignment. For fixed \((w,d)\), the refutation is polynomial-size. No universal polynomial refutation claim should be made unless \(\mathrm{NP}=\mathrm{coNP}\).

### B5. Inclusion-minimal obstruction cores

Core extraction uses repeated solving:

1. start with the current refuting factor set;
2. remove one factor;
3. re-solve;
4. keep the deletion if the failure persists;
5. for each final core member, retain a satisfying assignment after deleting that member.

At most \(m+1\) solver calls are needed. The output proves inclusion-minimality, not minimum cardinality.

### B6. Minimum-cost policies and repairs

With action costs and nonnegative constraint-relaxation penalties, replace Boolean DP by min-sum DP. The same width dependence applies, with additional arithmetic bit-complexity. The result is a minimum-cost policy or a minimum-weight repair in the declared finite model.

Removing a safety factor is a design diagnosis, not permission to operate under the original safety specification.

## Theorem package C: acyclicity, join trees, and gap detection

### C1. Acyclic permitted-tuple presentations

For permitted-tuple relations with an \(\alpha\)-acyclic hypergraph, semijoin / join-tree propagation decides feasibility and extracts a witness in polynomial time in explicit relation size. The certificate is a semijoin trace plus the final witness or empty relation.

Caution:

- this is an established database/CSP algorithmic result;
- forbidden-tuple encodings may be exponentially smaller than permitted tables;
- expanding forbidden tuples can destroy polynomiality.

### C2. Uniform acyclicity theorem as a synthesis target

A stronger theorem may synthesize BFMY/Yannakakis and Vorob'ev:

- acyclic hypergraph;
- separator-consistent relational supports;
- compatible probability marginals;
- existence of a global relation or probability coupling.

This should be stated as a known-theorem synthesis with precise hypotheses, not as a new database or probability theorem.

### C3. Gap detection

The proposed \(\mathsf D^{\mathsf P}\)-style gap detection result is valuable, but should remain a theorem target until the reductions are fully checked. If proved, it would show that detecting “set/effective success but distributed/presentation failure” sits at a difference-of-NP layer, not simply NP.

## Theorem package D: budget and sensor repair

### D1. Action-budget realisability

For fibrewise presentations, using at most \(\beta\) distinct actions is a hitting-set problem: choose \(A'\subseteq A\) of size at most \(\beta\) hitting each nonempty fibre action set.

Expected consequences:

- NP-complete;
- greedy logarithmic approximation;
- W[2]-hard parameterized by \(\beta\);
- FPT in total action alphabet size.

The W[2] and inapproximability claims require standard references and exact parameter statements.

### D2. Sensor selection by conflict hitting

For one-shot fibre models, a selected sensor set works iff it hits every conflict core. For conflict \(C\), define

\[
E_C=\{s:s\text{ is nonconstant on }C\}.
\]

The exact repair condition is

\[
T\cap E_C\ne\varnothing
\]

for every relevant conflict core \(C\) of size at most \(|A|\). This yields a hitting-set formulation for sensor design.

### D3. Lazy sensor-cut generation

Repeatedly:

1. solve current sensor hitting-set master problem;
2. run fibre synthesis under selected sensors;
3. if synthesis fails, extract a small conflict core;
4. add the corresponding hitting constraint;
5. repeat.

If the master problems are solved exactly, the first feasible sensor set returned is globally optimal. No polynomial iteration bound should be claimed without proof.

### D4. Sensor-design hardness

Minimum sensor selection remains NP-hard even when policy synthesis is polynomial. A Set-Cover reduction using one anchor scenario and one scenario per universe element gives hardness with binary sensor outputs and two actions.

This is a key message: optimizing the observation architecture is not the same problem as synthesizing a policy for a fixed architecture.

## Theorem package E: certified finite-element front end

### E1. Linear finite-element scenario model

For each scenario \(w\):

\[
K_wu_{w,a}=f_w+B_wa.
\]

Pre-actuation observations may be generated from

\[
K_wu_w^0=f_w,
\qquad
q(w)=Q(Hu_w^0).
\]

For affine response quantities,

\[
y_{e,w}=d_{e,w}+\sum_jG_{e,j,w}a_j.
\]

One matrix factorization per scenario plus baseline and actuator influence solves can generate relation entries without a full solve for every action tuple in affine cases.

### E2. Residual-based certified relation entries

If \(K\) is symmetric positive definite and

\[
0<\underline\lambda\le\lambda_{\min}(K),
\]

then, for residual \(r=f-K\widehat u\),

\[
\|u-\widehat u\|_2\le \frac{\|r\|_2}{\underline\lambda},
\]

and

\[
|c^T(u-\widehat u)|\le \|c\|_2\frac{\|r\|_2}{\underline\lambda}.
\]

This certifies safe and unsafe relation rows. Rows crossing a threshold remain unresolved.

### E3. Inner and outer finite models

Define:

- \(R^-\): proved-safe rows;
- \(R^+\): all rows except proved-unsafe rows.

If

\[
R_i^-\subseteq R_i^{\mathrm{true}}\subseteq R_i^+,
\]

then

\[
\Gamma(P^-)
\subseteq
\Gamma(P^{\mathrm{true}})
\subseteq
\Gamma(P^+).
\]

Thus:

- inner SAT gives a certified policy for the true finite model;
- outer UNSAT proves no true finite-model policy;
- inner UNSAT and outer SAT is inconclusive.

### E4. Certified sparsification

For affine response

\[
y_i(a)=d_i+\sum_{x\in S_i}g_{ix}a_x,
\]

retain \(J_i\subseteq S_i\) and bound omitted terms by

\[
\underline\eta_i=\sum_{x\in S_i\setminus J_i}\min_{v\in D_x}g_{ix}v,
\qquad
\overline\eta_i=\sum_{x\in S_i\setminus J_i}\max_{v\in D_x}g_{ix}v.
\]

If retained scopes grow from \(J_i\) to \(J_i'\), then

\[
\Gamma^-_J
\subseteq
\Gamma^-_{J'}
\subseteq
\Gamma^{\mathrm{true}}
\subseteq
\Gamma^+_{J'}
\subseteq
\Gamma^+_J.
\]

This is a central mechanics-specific theorem for width-adaptive synthesis.

### E5. Width-adaptive certified synthesis

Algorithm outcome options:

1. **SAFE POLICY**: inner model is satisfiable; return policy plus mechanical row certificates.
2. **NO POLICY**: outer model is unsatisfiable; return DP refutation plus certified invalidity of excluded rows.
3. **INCONCLUSIVE**: inner UNSAT and outer SAT, or numerical budget exhausted.

The algorithm should refine retained scopes, numerical enclosures, or both. With exact data and finite scopes, support refinement terminates after finitely many steps, but may expose high width.

### E6. Limits of physical interpretation

State explicitly:

- FE residual certification validates the discrete algebraic model, not continuum discretization error;
- finite scenario certification does not cover continuous uncertainty unless uncertainty cells are certified;
- conservative inner failure is not physical impossibility;
- solver timeout is not proof of bounded nonrealisability.

## Demonstrator example

Use the two-spring exact example:

\[
u(f,a_1,a_2)=\frac{f-a_1-a_2}{2}
\]

with \(f\in\{1,2\}\), \(a_1,a_2\in\{0,1\}\), and safety condition \(|u|\le0.25\). Then

\[
R_1=\{(0,1),(1,0)\},
\qquad
R_2=\{(1,1)\}.
\]

If both loads have the same observation, each local scenario is feasible but no observation-uniform command exists. A displacement-threshold sensor separates the loads and restores feasibility. This example supplies:

- exact mechanical admissibility tables;
- observation-induced obstruction;
- inclusion-minimal core;
- sensor repair;
- executable repaired policy.

It is a correctness demonstrator, not a computational benchmark.

## Computational study required before applied-mechanics submission

A theorem-only manuscript is unlikely to fit an applied and computational mechanics venue. The final submission should include:

- implemented solver;
- independent verifier;
- exact small cases checked by exhaustive enumeration;
- finite-element relation-generation code;
- decomposition certificates;
- policy and refutation certificates;
- corrupted-certificate rejection tests.

### Benchmark families

| Benchmark | Purpose |
|---|---|
| Exact spring and small truss systems | exhaustive correctness and certificate debugging |
| 10-bar truss with quantized sensors | FE-to-ECD pipeline |
| Modular frame or mass-spring chain | fixed-width scaling |
| Cross-braced frame or 2D lattice | width-growth boundary |
| Dense influence instances | honest assessment of sparsification limits |
| Finite inspection-actuation examples | causal compilation validation |

### Baselines

- exhaustive enumeration on small instances;
- SAT / CP-SAT encoding;
- MILP formulation;
- join-tree semijoin solver where applicable;
- tree-decomposition dynamic programming;
- width-adaptive certified solver.

### Metrics

Report separately:

- FE preprocessing time;
- relation generation time;
- decomposition construction time;
- DP solve time;
- certificate generation time;
- independent verification time;
- peak memory;
- actual and weighted width;
- unresolved numerical entries;
- policy cost;
- core size;
- sensor-repair size.

Timeouts and unresolved numerical cases should be reported as inconclusive, not merged with proven infeasibility.

## Suggested article structure

1. Introduction: sensor-limited mechanical decisions and observational uniformity.
2. Mechanical motivating problem.
3. Finite ECD formulation and implementation catalogues.
4. Complexity classifications.
5. Width-based certifying algorithms.
6. Certificate extraction and core minimization.
7. Sensor refinement and architecture repair.
8. Certified FE relation generation and width-adaptive sparsification.
9. Numerical results and reproducibility.
10. Limitations and conclusions.

Appendices:

- reductions;
- pseudocode;
- certificate grammar;
- verifier specification;
- FE residual/enclosure details;
- benchmark generation.

## Separation from the first monograph

The first monograph supplies the foundational theory: presentation-relative diagnostics, functoriality, compression, computability, Bell/contextuality, and causal semantics.

The second monograph/article should supply finite algorithmic theory and a mechanics pipeline. It should not rely on the first monograph's broad philosophical sweep for novelty. Its novelty should be:

1. finite explicit encodings for sensor-limited mechanics;
2. diagnostic-preserving compilation;
3. one-pass diagnostic semiring;
4. width and weighted-width algorithms;
5. proof objects and independent verifier;
6. sensor-repair hitting-set theorem;
7. certified FE inner/outer relation generation;
8. width-adaptive certified sparsification;
9. reproducible computational mechanics benchmarks.

## Remaining development tasks

1. Formalize finite input model and certificate grammar.
2. Prove the fibre selector algorithm and conflict certificate bound.
3. Prove the reachability-correct causal compilation theorem.
4. Prove NP/\(\#\)P/coNP frontier for explicit finite synthesis.
5. Develop promise-hardness reductions for catalogue effectiveness and budget boundedness.
6. Develop the diagnostic semiring DP with proof objects.
7. Prove weighted-width complexity bounds.
8. Prove acyclic/join-tree certificate extraction for permitted tables.
9. Fully adjudicate the proposed \(\mathsf D^{\mathsf P}\) gap-detection result.
10. Prove one-shot sensor-repair hitting-set theorem.
11. Prove FE inner/outer relation soundness.
12. Prove width-adaptive certified sparsification.
13. Implement a prototype solver and independent verifier.
14. Generate exact small spring/truss benchmarks.
15. Design and execute reproducible mechanical experiments.
