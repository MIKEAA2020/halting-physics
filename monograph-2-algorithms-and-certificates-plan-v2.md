# Second monograph / focused article plan

## Working monograph title

**Algorithms and Certificates for Finite Effective Causal Descent: Width, Counting, Compression, and Certified Mechanical Synthesis**

## Focused article title for applied mechanics

**Certifying Finite Effective Causal Descent for Sensor-Limited Mechanical Systems**

Alternative, more theory-forward title:

**Algorithms and Certificates for Finite Effective Causal Descent: Complexity, Width-Based Tractability, and Applications to Sensor-Limited Mechanics**

## Editorial identity

The companion work should not read as a shortened version of the foundational monograph. It should be a proof-producing finite synthesis paper. The editorial message is:

> Finite effective causal descent is a diagnostic-preserving, proof-producing synthesis pipeline for finite mechanical decision systems under partial observation, with explicit complexity boundaries and numerically certified mechanics data.

The paper should omit the first monograph's broad computability, Bell/contextuality, DNR/PA, Weihrauch, and general causal-composition developments except where needed for definitions. The new contribution should be algorithmic and certifying.

## Central finite problem

Input:

- finite scenario or world set;
- finite observation maps / information states;
- finite action domains;
- local admissibility relations from mechanics, safety, equilibrium, interface, or implementation constraints;
- optional implementation catalogues and resource budgets;
- explicit relation tables, forbidden-tuple tables, or certified finite-element-generated relations.

Output:

1. certified safe policy;
2. certified absence of policy in the declared finite model;
3. certified set-only or over-budget outcome;
4. inconclusive result when numerical or resource bounds are insufficient.

The synthesis problem should be presented as finite ECD over an observation quotient: one decision variable per information state, with factors encoding local and global constraints.

## Core finite presentation

Let \(X\) be finite policy variables, each with finite domain \(D_x\). A finite descent presentation is

\[
\mathcal P=(X,(D_x)_{x\in X},(S_i,R_i)_{i=1}^m),
\]

where \(S_i\subseteq X\) and

\[
R_i\subseteq\prod_{x\in S_i}D_x.
\]

A global policy is

\[
\Gamma(\mathcal P)=\{a\in\prod_xD_x:a|_{S_i}\in R_i\ \forall i\}.
\]

For explicit finite tables,

\[
\Gamma_{\mathrm{set}}=\\Gamma_{\mathrm{eff}}
\]

unless effectiveness is defined by a declared finite implementation catalogue. Therefore the finite paper must define effectiveness by implementability in a catalogue: lookup table memory, decision tree depth, certified reduced controller, communication protocol, approved code fragment, etc.

## Wildcard implementation compilation

For controller \(j\), let \(\mathcal L_j\) be a finite implementation catalogue with evaluation

\[
\operatorname{eval}_j(\ell,o)
\]

and cost \(c_j(\ell)\). Introduce implementation variables

\[
\ell_j\in \mathcal L_j\cup\{\bot\}.
\]

The wildcard \(\bot\) is compatible with any policy behaviour and has infinite cost. Real implementations satisfy

\[
x_{j,o}=\operatorname{eval}_j(\ell_j,o)
\quad(o\in O_j).
\]

Then:

- every set-theoretic policy extends with \(\bot\);
- finite-cost extensions are exactly effectively realised policies;
- bounded realisability is minimum finite implementation cost at most \(B\);
- complete policy catalogues need not be materialised.

This is a distinctive finite analogue of the monograph's realisation-image layer.

## Theorem package A: finite complexity frontier

### A1. Polynomial local fibre selection

For one-shot observation map \(o:W\to O\), finite action set \(A\), and scenario admissible action sets \(S_w\subseteq A\), a policy exists iff

\[
\bigcap_{w:o(w)=o_0}S_w\ne\varnothing
\]

for every realised observation \(o_0\). With bit-vector action sets this is computable in \(O(|W||A|/\omega)\).

If a fibre fails, there is a conflict certificate of at most \(|A|\) scenarios, one excluding each action. The bound is tight.

Minimum-cardinality fibre conflicts should be treated carefully: finding a minimum core is Set-Cover-like and can be NP-hard; the algorithm should promise bounded or inclusion-minimal cores, not minimum cardinality unless explicitly solved.

### A2. Finite synthesis complexity

For explicit finite relation tables:

| Problem | Complexity |
|---|---:|
| Verify proposed assignment | P |
| Unary constraints | P |
| Boolean binary constraints | P via 2-SAT |
| Boolean ternary constraints | NP-complete |
| 3-element domains, binary inequality constraints | NP-complete via graph 3-colouring |
| Nonexistence of global assignment | coNP-complete |
| Counting global assignments | \(\#\mathrm P\)-complete |

The NP-completeness results should be stated even under nonempty local relation promises to show the hardness is gluing/global compatibility, not local impossibility.

### A3. Promise hardness for the tiers

Develop reductions showing:

- effective realisability is NP-hard even under \(\Gamma_{\mathrm{set}}\ne\varnothing\), when effectiveness is a finite implementation catalogue;
- bounded realisability is NP-hard even under \(\Gamma_{\mathrm{eff}}\ne\varnothing\), when a cost budget is imposed.

These reductions require care: finite effectiveness must be catalogue-based, not ordinary computability.

### A4. Succinct diagram checking

For explicit restriction maps, diagram compatibility is polynomial. If maps are Boolean circuits, diagram compatibility becomes coNP-complete by circuit equivalence. This separates explicit finite ECD from succinct presentations.

## Theorem package B: width-based algorithms and certificates

### B1. Tree-decomposition dynamic programming

Let \(G_\mathcal P\) be the primal graph and let \((T,(B_t))\) be a tree decomposition of width \(w\). With maximum domain size \(d\), feasibility is decidable in

\[
O((n+m)d^{w+1})
\]

up to table and indexing factors. The dynamic program should compute both feasibility and minimum implementation cost using a diagnostic semiring.

### B2. Weighted state-space width

For heterogeneous domains, use

\[
\lambda(T)=\max_t\sum_{x\in B_t}\lceil\log_2|D_x|\rceil.
\]

The DP bound becomes

\[
\operatorname{poly}(|I|,|T|)2^{\lambda(T)}.
\]

This prevents support packaging from looking artificially low-width when tuple domains become large.

### B3. Diagnostic semiring

Use a semiring-like value

\[
(s,c)\in\{0,1\}\times(\mathbb N\cup\{\infty\})
\]

where:

- \(s=1\) means set-theoretic feasibility;
- finite \(c\) records minimum implementation cost;
- \(c=\infty\) means set-feasible but not effectively realised under the catalogue.

The root value distinguishes:

- no set section;
- set-only section;
- effective over budget;
- bounded success.

### B4. DP refutation certificates

A negative certificate should contain:

- validated tree decomposition;
- factor-to-bag assignment;
- separator message tables;
- recurrence values for all bag assignments;
- root infeasibility value.

The verifier recomputes every recurrence. For fixed width and domain size this gives polynomial-size, independently checkable refutations. No universal polynomial refutation claim should be made; that would imply \(\mathrm{NP}=\mathrm{coNP}\).

### B5. Inclusion-minimal obstruction cores

Core extraction:

1. start with all factors used by a refutation;
2. delete one factor at a time;
3. re-solve;
4. retain deletions that preserve the same failure;
5. output one refutation for the final core and one satisfying deletion witness for each remaining member.

This uses at most \(m+1\) solver calls. It yields inclusion-minimal, not minimum-cardinality, cores.

## Theorem package C: acyclicity and join-tree methods

For permitted-tuple relations with an \(\alpha\)-acyclic hypergraph, semijoin / join-tree propagation decides feasibility and extracts a witness in polynomial time in explicit relation size.

The paper should not oversell this as a new CSP algorithm. Its role is as a certificate-producing ECD subroutine and as a bridge to mechanical decomposition.

Need caution:

- forbidden-tuple encodings may be exponentially smaller than permitted-tuple tables;
- expanding forbidden to permitted tuples can destroy polynomiality;
- acyclicity of the physical mesh is not automatically acyclicity of the policy-factor hypergraph after observation identification.

## Theorem package D: budget and sensor repair hardness

### D1. Action-budget realisability

With fibrewise presentations, asking whether one can use at most \(\beta\) distinct actions is a hitting-set / set-cover problem:


action subset \(A'\) of size \(\le\beta\) must hit every feasible fibre action set.

Consequences:

- NP-complete;
- logarithmic approximation by greedy;
- W[2]-hard parameterized by \(\beta\);
- FPT in total action alphabet size.

### D2. Sensor selection / observation architecture

For one-shot fibres, a sensor set must hit every conflict core. For a conflict \(C\), define

\[
E_C=\{s:s\text{ separates at least two worlds in }C\}.
\]

A selected sensor family works iff it hits every relevant \(E_C\). This is exact for one-shot fibre models.

Minimum sensor selection is NP-complete even when policy synthesis is easy. This is important: observation-architecture optimisation is a separate hard problem.

### D3. Certificate-driven sensor cuts

Use lazy hitting-set generation:

1. solve current sensor-selection ILP;
2. run fibre synthesis under selected sensors;
3. if failure, extract a small conflict core;
4. add the hitting constraint;
5. repeat.

If exact master problems are solved, the first successful sensor set is globally optimal. No polynomial iteration bound should be claimed unless proved.

## Theorem package E: certified mechanics front end

### E1. Linear finite-element scenario model

For scenario \(w\):

\[
K_w u_{w,a}=f_w+B_w a.
\]

Pre-actuation observations can be

\[
q(w)=Q(Hu_w^0),\qquad K_wu_w^0=f_w.
\]

For affine response quantities:

\[
y_{e,w}=d_{e,w}+\sum_jG_{e,j,w}a_j.
\]

One factorisation per scenario plus actuator influence solves can generate relation entries without solving for every action tuple in the affine case.

### E2. Residual-based certified relation entries

If \(K\) is symmetric positive definite and

\[
0<\underline\lambda\le\lambda_{\min}(K),
\]

then for residual \(r=f-K\widehat u\):

\[
\|u-\widehat u\|_2\le \frac{\|r\|_2}{\underline\lambda},
\]

and

\[
|c^T(u-\widehat u)|\le \|c\|_2\frac{\|r\|_2}{\underline\lambda}.
\]

This gives certified valid and invalid relation entries. Entries crossing a threshold are unresolved.

### E3. Inner/outer admissibility models

Construct:

- inner safe relation \(R^-\): proved-safe rows;
- outer possible relation \(R^+\): all rows except proved-unsafe rows.

If

\[
R^-_i\subseteq R_i^{\mathrm{true}}\subseteq R_i^+,
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

- inner SAT gives certified safe policy;
- outer UNSAT proves no true finite-model policy;
- inner UNSAT and outer SAT is inconclusive.

### E4. Certified sparsification

For affine response

\[
y_i(a)=d_i+\sum_{x\in S_i}g_{ix}a_x,
\]

retain scope \(J_i\subseteq S_i\) and bound omitted influence:

\[
\underline\eta_i=\sum_{x\in S_i\setminus J_i}\min_{v\in D_x}g_{ix}v,
\qquad
\overline\eta_i=\sum_{x\in S_i\setminus J_i}\max_{v\in D_x}g_{ix}v.
\]

This yields inner and outer relations over smaller scopes. If scopes are enlarged, inner feasible sets grow and outer feasible sets shrink:

\[
\Gamma^-_J\subseteq\Gamma^-_{J'}\subseteq\Gamma^{\mathrm{true}}
\subseteq\Gamma^+_{J'}\subseteq\Gamma^+_J.
\]

This is a central mechanics-specific theorem.

### E5. Limits of physical interpretation

State explicitly:

- FE residual certification validates the discrete algebraic model, not continuum discretization error;
- finite scenario certification validates only the finite scenario set unless uncertainty cells are certified;
- conservative inner failure is not proof of physical impossibility;
- solver timeouts are inconclusive, not resource lower bounds.

## Demonstrator example

Use the two-spring system from the Astra audit:

\[
u(f,a_1,a_2)=\frac{f-a_1-a_2}{2}
\]

with \(f\in\{1,2\}\), \(a_1,a_2\in\{0,1\}\), and \(|u|\le0.25\). This gives:

\[
R_1=\{(0,1),(1,0)\},
\qquad
R_2=\{(1,1)\}.
\]

If both loads have the same observation, the relations are locally nonempty but have empty intersection. A displacement-threshold sensor separates the loads and restores feasibility.

This is a correctness demonstrator, not empirical validation.

## Computational study required before mechanics submission

A JACM or applied-mechanics submission needs implementation and data. The final paper should include:

- implemented solver;
- independent verifier;
- exact small cases checked by enumeration;
- finite-element relation-generation code;
- benchmark mechanical models;
- decomposition certificates;
- policy and refutation certificates;
- corrupted-certificate rejection tests.

### Suggested benchmark families

| Benchmark | Purpose |
|---|---|
| Exact spring and small truss systems | exhaustive correctness and certificate debugging |
| 10-bar truss with quantized sensors | finite-element-to-ECD pipeline |
| Modular frame or mass-spring chain | fixed-width scaling |
| Cross-braced frame or 2D lattice | width-growth boundary |
| Dense influence instances | honest assessment of sparsification limits |
| finite inspection-actuation examples | causal compilation validation |

### Baselines

- exhaustive enumeration on small instances;
- SAT / CP-SAT encoding;
- MILP formulation;
- join-tree semijoin solver where applicable;
- tree-decomposition DP;
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

## Article structure

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

The second monograph/article should supply the finite algorithmic theory and mechanics pipeline. It should not rely on the first monograph's broad philosophical sweep for novelty. Its novelty should be:

1. finite explicit encodings for sensor-limited mechanics;
2. diagnostic-preserving compilation;
3. one-pass diagnostic semiring;
4. width and weighted-width algorithms;
5. proof objects and independent verifier;
6. sensor-repair hitting-set theorem;
7. certified FE inner/outer relation generation;
8. width-adaptive certified sparsification;
9. reproducible computational mechanics benchmarks.

## Current assessment of audit claims

### Strong and worth adopting

- Present the companion work as a certified computational-mechanics method.
- Make Algorithm 3 / width-adaptive certified synthesis central.
- Use explicit finite input encodings and avoid infinite computability material.
- Emphasize policy variables after observation identification.
- Use tree decompositions and weighted state-space width.
- Emit independent certificates, not just solver verdicts.
- Include sensor refinement via hitting set.
- Include inner/outer FE-certified relations.
- Require numerical validation before submission.

### Needs caution or further proof

- Claimed dichotomies via Schaefer/Zhuk are true in fixed-template CSP settings but require careful statement and references.
- The proposed \(\mathsf D^\mathsf P\) gap-detection result needs a fully checked reduction before inclusion as a theorem.
- Uniform acyclicity simultaneously covering set, possibilistic, and probabilistic tiers is plausible via BFMY/Vorob'ev, but must be stated as a known-theorem synthesis with precise consistency hypotheses.
- ETH lower bounds and W[1]/W[2] hardness need exact parameterization statements and references.
- Mechanics nested-dissection claims require graph assumptions connecting the mechanical substructure graph to the policy primal graph.

### Should not be claimed without experiments

- Computational advantage on real mechanical models.
- Certified sparsification effectiveness in practice.
- Scaling superiority over CP-SAT/MILP.
- Applicability to continuum mechanics beyond certified finite model relations.

## Near-term development tasks

1. Formalize finite input model and certificate grammar.
2. Prove the fibre selector algorithm and conflict certificate bound.
3. Prove NP/\(\#\)P frontier for explicit finite synthesis.
4. Develop the diagnostic semiring DP with proof objects.
5. Prove weighted-width complexity bounds.
6. Prove one-shot sensor-repair hitting-set theorem.
7. Prove FE inner/outer relation soundness.
8. Implement a prototype solver and verifier.
9. Generate exact small spring/truss benchmarks.
10. Design reproducibility protocol.
