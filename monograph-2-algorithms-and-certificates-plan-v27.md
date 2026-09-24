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

## Development rule for both monographs

The governing rule is:

> **Topological order is the constraint; feasibility is the priority.**

A claim may be developed only after its prerequisites have been fixed. Among the claims whose prerequisites are fixed, develop first the one with the shortest path to a rigorous proof, executable certificate, or reproducible computation. This rule is intended to prevent three common errors:

1. proving a theorem about a presentation and then wording it as a theorem about a bare capability problem;
2. stating an algorithmic or complexity result before the input representation and certificate grammar are fixed;
3. claiming practical computational value before the relevant experiment and independent verification exist.

The rule applies differently to the two works.

| Work | Topological constraint | Feasibility priority |
|---|---|---|
| Foundational monograph | source doctrine -> presentation -> morphism -> invariant/certificate -> effectivity/resource claim | keep only theorems whose hypotheses are explicit; move broad source-domain claims to conjectural modules |
| Finite algorithms/mechanics monograph | finite input model -> certificate grammar -> solver/verifier -> mechanics relation generation -> sparsification/refinement -> experiments | build the smallest independently verifiable computational pipeline before claiming applied scaling |

Accordingly, the companion paper should be developed from the bottom up: exact finite instances and certificates first; certified FE and sparsification second; comparative mechanics performance last.

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

### Adopt as theorem targets with caution, ordered by feasibility

The following are plausible and valuable, but require careful final proofs and references. They should be developed in the order below, because each earlier item either follows from standard finite-CSP technology or can be stated conditionally without new empirical claims.

| Feasibility rank | Claim target | What is needed before it becomes publishable | Safe interim wording |
|---:|---|---|---|
| 1 | Schaefer/Zhuk fixed-template dichotomy | State only for fixed finite constraint languages; cite the relevant dichotomy theorem; separate this from the variable-template explicit-table model used by the algorithms. | ``For fixed-template CSPs, known dichotomy theorems classify tractability; the present explicit finite solver instead reports width-sensitive performance.'' |
| 2 | Acyclic set/support/probability alignment | State the relational part as BFMY/Yannakakis-style join-tree consistency and the probability part under precise Vorob'ev-compatible marginal-consistency hypotheses. | ``Under the standard acyclicity and marginal-consistency hypotheses, local consistency is globally extendable.'' |
| 3 | Conditional nested-dissection mechanics bounds | Prove a graph lemma connecting the mechanical substructure graph, retained influence scopes, and the policy primal graph; report it as conditional on locality and separator assumptions. | ``When certified sparsification produces scopes respecting a separator hierarchy, the DP inherits the corresponding separator width.'' |
| 4 | ETH, W[1], and W[2] lower bounds | Fix the exact parameters, reductions, and citations; avoid mixing action-budget, sensor-budget, treewidth, and domain-size parameters. | ``The optimization variants contain standard set-cover/hitting-set subproblems, so parameterized lower bounds are expected under the corresponding standard parameterizations.'' |
| 5 | \(\mathsf D^\mathsf P\)-style gap detection | Give complete paired reductions for membership and hardness, with all promises stated explicitly. | ``Gap detection is a natural difference-of-NP candidate; this remains a theorem target until the reductions are fully checked.'' |
| 6 | Practical speedups over SAT/CP-SAT/MILP | Implement baselines, run reproducible benchmarks, and report failures and timeouts as inconclusive. | ``The width-based solver exposes structure not visible in black-box encodings; comparative performance is an empirical question.'' |

This ordering should guide the writing. The first two items can plausibly be included as carefully cited background or synthesis theorems. Items 3--5 should remain conditional or appendix-level until the proofs are complete. Item 6 cannot be claimed from theory alone.

### Do not claim yet, ordered by how easy it is to avoid or eventually justify

| Feasibility rank | Forbidden claim | Why it is unsafe | What may be claimed instead | What would be required to strengthen it |
|---:|---|---|---|---|
| 1 | Solver timeout proves bounded non-realisability. | A timeout is not a certificate. | ``The run was inconclusive under the stated resource limit.'' | A checked refutation certificate, an exact exhaustive proof, or a proved lower-bound theorem for the encoded instance family. |
| 2 | Conservative inner-model infeasibility proves physical infeasibility. | Inner UNSAT only says the sufficient safe-row model has no policy. | ``Inner UNSAT and outer SAT is inconclusive; outer UNSAT proves no policy in the certified finite model.'' | Outer-model UNSAT plus certified finite-model coverage; physical claims need a validated modelling link. |
| 3 | FE residual bounds alone establish continuum-mechanics validity. | Residual bounds certify the discrete algebraic solve, not discretization or modelling error. | ``The finite model is certified relative to the chosen discretization and scenario set.'' | A posteriori discretization-error estimates, mesh-refinement evidence, or independent continuum validation. |
| 4 | Certified sparsification is practically useful on real mechanical models. | The theorem gives monotone soundness, not performance or accuracy benefits. | ``Sparsification gives a sound refinement ladder; its computational value is benchmark-dependent.'' | Ablations showing width reduction, certificate preservation, and reduced end-to-end time on representative cases. |
| 5 | The method scales better than CP-SAT or MILP. | Comparative scaling is empirical and instance-dependent. | ``The method has fixed-parameter guarantees in width and produces independently checkable certificates.'' | Reproducible benchmark comparisons against tuned SAT/CP-SAT/MILP baselines, with hardware, seeds, encodings, and all timeouts reported. |

These prohibitions are not stylistic cautions; they are part of the correctness contract. The paper should distinguish three statuses throughout: certified success, certified failure, and inconclusive computation.

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

## Stage 1--2 deliverable: canonical input and certificate grammar

This section upgrades the first two roadmap items from planning notes to a verifier-facing specification. It should become the first technical section of the companion monograph.

### Canonical finite instance schema

A finite ECD instance should be encoded as the following tuple:

\[
I=(X,(D_x)_{x\in X},(S_i,R_i)_{i\in M},O,\operatorname{obs},\mathcal L,c,B).
\]

Here:

- \(X\) is a finite ordered list of policy variables;
- each \(D_x\) is a finite ordered nonempty domain;
- each factor \(i\in M\) has an ordered scope \(S_i\subseteq X\) and an explicit permitted table \(R_i\subseteq\prod_{x\in S_i}D_x\), or equivalently an explicit forbidden table \(F_i\);
- \(O\) records observation states when variables arise from information cells;
- \(\operatorname{obs}\) records the world-to-observation or history-to-information-cell map used to form policy variables;
- \(\mathcal L=(\mathcal L_j)_j\) is the optional finite implementation catalogue;
- \(c:\bigsqcup_j\mathcal L_j	o\mathbb N\) is the implementation cost;
- \(B\in\mathbb N\) is the optional budget.

All tables are part of the input unless a specific succinct encoding is declared. Complexity claims in the main theorem package are therefore explicit-table claims. A succinct circuit, automaton, or FE generator changes the input representation and must be analysed separately.

### Certificate grammar, version 0

The independent verifier should accept only typed certificates. The following grammar is sufficient for the first implementation.

| Certificate type | Data included | Verifier check | Outcome certified |
|---|---|---|---|
| `POLICY` | assignment \(a_x\in D_x\) for each \(x\in X\) | every factor row \(a|_{S_i}\in R_i\) or avoids \(F_i\) | set-theoretic global section |
| `CATALOGUE-POLICY` | policy plus implementations \(\ell_j\in\mathcal L_j\) | catalogue evaluations match all induced policy variables; total cost computed | effective or budgeted section |
| `FIBRE-CONFLICT` | observation value \(o\) and scenarios \(C\subseteq o^{-1}(o)\) with excluded-action witnesses | every action in \(A\) is excluded by at least one scenario in \(C\) | no one-shot observation-uniform selector on that fibre |
| `TREE-DECOMP` | bags, tree edges, factor-to-bag map | running-intersection property and scope containment | valid decomposition for DP certificates |
| `DP-REFUTATION` | decomposition plus separator messages and root table | recurrence recomputation at each bag assignment | unsatisfiability for the declared finite table instance |
| `DP-OPTIMUM` | decomposition, messages, root optimum, and traceback or dual refutation of cheaper values | recurrence and cost arithmetic | minimum cost or proof cost exceeds \(B\) |
| `SENSOR-REPAIR` | conflict cores and selected sensors | every core is hit; optimality certificate for the hitting-set master when claimed | sensor sufficiency or optimality |
| `FE-ROW` | residual norm, coercivity lower bound, response functional, interval decision | certified row is safe, unsafe, or unresolved | sound row classification for the discrete algebraic model |
| `SPARSIFICATION` | retained scopes \(J_i\), omitted-term bounds, inner/outer row tables | interval arithmetic and inclusion checks | monotone inner/outer sparsification ladder |

A solver log is never a certificate. The verifier should ignore search history except where the certificate type explicitly requires recurrence tables or optimization witnesses.

### Status tags

Every theorem, algorithm, and experiment should return exactly one of the following tags:

- `CERTIFIED-SAT`: a policy certificate verifies;
- `CERTIFIED-UNSAT`: a refutation certificate verifies;
- `CERTIFIED-OPT`: an optimum and its proof verify;
- `INCONCLUSIVE`: timeout, unresolved numerical rows, inner/outer gap, failed decomposition search, or failed certificate verification.

This four-tag convention is the computational form of the topological-order rule: once certificate verification fails, no higher-level claim is licensed.

## Stage 3 theorem: one-shot fibres

**Theorem A2, completed form.** For a one-shot observation map \(o:W	o O\), finite action set \(A\), and scenario-admissible sets \(S_w\subseteq A\), an observation-uniform selector exists iff

\[
A_z:=\bigcap_{w:o(w)=z}S_w
e\varnothing
\]

for every realised observation value \(z\). With bit-vector action sets the test takes \(O(|W||A|/\omega)\) word operations. If a fibre fails, there is a conflict certificate using at most \(|A|\) scenarios from that fibre, and this bound is tight.

**Proof.** A selector chooses one action \(a_z\) for each observation value. It is admissible exactly when \(a_z\in S_w\) for every scenario with observation \(z\), which is exactly \(a_z\in A_z\). Thus the fibre intersections are necessary and sufficient. Bit-vector intersection gives the stated running time. If \(A_z=\varnothing\), then for each action \(a\in A\) choose one scenario \(w_a\) in the fibre with \(a
otin S_{w_a}\). The set of distinct selected scenarios has size at most \(|A|\) and excludes every action. Tightness is witnessed by \(A=\{1,\ldots,k\}\), scenarios \(w_1,\ldots,w_k\), and \(S_{w_j}=A\setminus\{j\}\): all \(k\) scenarios are needed to exclude all actions.

## Stage 4 theorem: reachability-correct causal compilation

**Theorem A3, completed form.** Consider a finite explicit history tree whose predictor nodes are partitioned into information cells. A pure observation-uniform policy assigns one action to each information cell. For each unsafe leaf, read the list of information cells and edge actions along the root-to-leaf path. If one information cell occurs on that path with two different required actions, discard the path. Otherwise add one forbidden tuple on the distinct information-cell variables appearing on that path. The resulting forbidden-tuple presentation has global assignments exactly the policies that avoid every unsafe leaf.

**Proof.** Fix a policy. If an unsafe path contains one information cell with two different edge labels, no uniform policy can realise that path, so discarding it removes no feasible unsafe execution. For every remaining unsafe path, the path is realised by the policy exactly when the policy agrees with all action labels on the path, equivalently when its restriction to the path variables equals the forbidden tuple. Therefore forbidding all such tuples is exactly the condition that no unsafe leaf is reached. The construction is linear in the total length of explicitly listed unsafe paths, and in an explicit tree is \(O(NH)\), where \(N\) is the number of nodes and \(H\) the height.

## Stage 5 theorem: explicit-table complexity frontier

The following cases are ready to state once the input schema above is adopted.

- Verification of a proposed assignment is polynomial by scanning all relation rows or hash tables.
- Unary constraints are polynomial by intersecting allowed values variablewise.
- Boolean binary clauses are polynomial via the standard 2-SAT implication graph.
- Boolean ternary explicit-table CSP is NP-complete by the standard 3-SAT encoding, with nonempty local relations.
- Binary disequality over a three-element domain is NP-complete by graph 3-colouring.
- Nonexistence is coNP-complete as the complement of explicit-table CSP satisfiability.
- Counting global assignments is \(\#\mathrm P\)-complete by the parsimonious reduction from \(\#\)SAT.

These results belong to the companion monograph, not to the foundational monograph. The foundational text may cite them only as finite-source examples after the explicit-table representation has been declared.

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
A_o=\bigcap_{w:o(w)=o}S_w\ne\varnothing
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

## Stage 6 artifact: prototype solver and verifier

A first correctness artifact now exists at:

```text
/home/user/finite_ecd_prototype/
```

It is intentionally small and dependency-free. Its purpose is not performance but certificate discipline. The current prototype implements:

- explicit-table finite instance loading;
- well-formedness checks;
- policy verification;
- brute-force solving for tiny instances;
- one-shot fibre conflict generation;
- one-shot fibre conflict verification;
- exact two-spring examples with same-observation infeasibility and split-observation feasibility.

The demonstrator commands are:

```bash
python3 finite_ecd.py solve examples/two_spring_same_observation.json
python3 finite_ecd.py solve examples/two_spring_split_observation.json
python3 finite_ecd.py fibre-conflict examples/two_spring_fibres.json same
python3 finite_ecd.py verify-fibre examples/two_spring_fibres.json examples/two_spring_fibre_conflict_certificate.json
```

The observed statuses are the intended first validation gate:

| Example | Expected status | Meaning |
|---|---|---|
| same-observation two-spring instance | `CERTIFIED-UNSAT` by exhaustive search, with separate fibre conflict certificate | no observation-uniform command exists |
| split-observation two-spring instance | `CERTIFIED-SAT` | threshold sensor repairs the obstruction |
| fibre conflict certificate | `VERIFIED` | every action is excluded by a named scenario in the common observation fibre |

The prototype is not yet a width-DP solver, FE relation generator, or performance artifact. It satisfies only the first executable checkpoint: finite instances and elementary certificates are machine-checkable independently of prose.

## Stage 7 theorem: diagnostic semiring dynamic programming

For a tree decomposition 
\((T,(B_t)_{t\in T})\) of the primal graph, orient the tree at a root. Assign each factor to one bag containing its scope. For a bag assignment \(\alpha\\in\\prod_{x\\in B_t}D_x\), let the message value \(M_t(\\alpha)\\in\\{0,1\\}\times(\\mathbb N\\cup\\{\\infty\\})\) summarize the subtree below \(t\) conditional on \(B_t=\\alpha\). The recurrence is the usual introduce/join/projection recurrence, with local factor compatibility multiplied by \(\otimes\) and alternative extensions combined by \(\oplus\):

\[
(s,c)\\oplus(s',c')=(s\\lor s',\\min(c,c')),
\\qquad
(s,c)\\otimes(s',c')=(s\\land s',c+c').
\]

Here \((0,\\infty)\) is infeasible, \((1,\\infty)\) is set-feasible but not catalogue-realised, and \((1,c)\) with \(c<\\infty\) is catalogue-realised at cost \(c\). The root message therefore distinguishes:

- no set-theoretic section;
- set-only success;
- finite-cost effective success;
- budgeted success when \(c\\le B\).

**Soundness claim.** If all message tables are recomputed by the verifier and the root value is \((0,\\infty)\), then no global section exists. If the root value is \((1,c)\), traceback yields a global section of cost \(c\), and no lower-cost section exists when the recurrence used min-combination over all extensions.

This should be proved as an induction over the rooted decomposition: each message equals the semiring aggregate of all assignments on the variables in the processed subtree that agree with the boundary assignment. The proof object is the collection of message tables plus the decomposition certificate.

## Stage 8 theorem: weighted-width bound

For heterogeneous domains, the correct table-size parameter is not just bag cardinality. Define

\[
\lambda(T)=
\max_{t\in T}
\sum_{x\in B_t}\lceil\\log_2 |D_x|\rceil.
\]

Then every bag table has at most \(2^{\\lambda(T)}\) assignments. For explicit relations and fixed arithmetic word size, the verifier and solver recurrences run in

\[
\\operatorname{poly}(|I|,|T|)\,2^{\\lambda(T)}
\]

up to factor-indexing overhead. The certificate should report both ordinary width and weighted width, because a decomposition with small bags can still be infeasible when one variable has a very large domain.

The proof is immediate from the product bound

\[
\\prod_{x\in B_t}|D_x|
\\le
\\prod_{x\in B_t}2^{\\lceil\\log_2|D_x|\\rceil}
=2^{\\sum_{x\in B_t}\\lceil\\log_2|D_x|\\rceil}.
\]

## Stage 9 theorem: join-tree certificate extraction

For permitted-table presentations whose hypergraph is \(\alpha\)-acyclic and supplied with a join tree, semijoin reduction gives a polynomial certificate of satisfiability or emptiness in the total explicit relation size.

A certificate should include:

1. the join tree;
2. for each edge, the separator variables;
3. semijoin deletion traces or final reduced relations;
4. either a surviving root tuple with backtracking choices, or an empty reduced relation witnessing unsatisfiability.

The verifier checks that every deletion is justified by absence of a matching separator tuple in the neighbouring relation, and that every retained backtracking choice agrees on separators. This is a standard database/CSP specialization; the companion should cite it rather than present it as a new acyclicity theorem.

## Stage 10 theorem: one-shot sensor repair by hitting set

Let each candidate sensor \(s\in\\mathcal S\) be a map from scenarios to sensor values. In a one-shot fibre model, a conflict core \(C\subseteq W\) is repaired by a selected sensor set \(T\subseteq\\mathcal S\) exactly when some selected sensor separates the core:

\[
T\\cap E_C\\ne\\varnothing,
\\qquad
E_C=\\{s\\in\\mathcal S:s\\text{ is nonconstant on }C\\}.
\]

Thus a sensor family repairs all currently known cores iff it is a hitting set for \((E_C)_C\). If all possible minimal fibre conflicts are included, the condition is exact for one-shot repair.

**Proof.** If no selected sensor separates \(C\), then all scenarios in \(C\) remain in one observation fibre, so the same conflict certificate still excludes every action. Conversely, if a selected sensor separates each conflict core, then no certified failing core remains inside a single observation fibre. For the exact one-shot theorem, take the family of all minimal failing fibres under the original scenario set; after refinement, a fibre fails iff it contains one of these cores. Therefore hitting every \(E_C\) is necessary and sufficient.

The optimization version is minimum hitting set. The lazy-cut algorithm is sound because each failed synthesis call returns a genuine missing hitting constraint. If each master hitting-set problem is solved exactly, the first selected sensor set for which synthesis succeeds is globally optimal for the generated exact core family.

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

## Stage 11 theorem target: catalogue and budget promise hardness

The catalogue layer should be treated as a finite artifact class, not as ordinary computability. A clean reduction pattern is as follows.

- Start from an explicit finite presentation with at least one set-theoretic section.
- Add implementation variables \(\ell_j\in\mathcal L_j\cup\{\bot\}\), where \(\bot\) has infinite cost and is compatible with every behaviour.
- Encode a finite combinatorial choice problem in the requirement that non-wildcard implementations jointly realise the policy variables.

The safe theorem target is:

1. catalogue-effective realisability is NP-hard even under the promise \(\Gamma_{\mathrm{set}}\ne\varnothing\);
2. budgeted realisability is NP-hard even under the promise \(\Gamma_{\mathrm{eff}}\ne\varnothing\).

The reductions should be written so that the wildcard proves the promise: a set-level policy always exists, while finite-cost catalogue choices encode the hard problem. Until the reductions are fully specified, the companion should claim only that the catalogue and budget layers contain standard finite selection and knapsack/set-cover phenomena.

## Stage 12 theorem: FE inner/outer soundness for the discrete model

For the mechanics front end, the certified object is the discrete algebraic model. Suppose each true finite relation row satisfies

\[
R_i^-\subseteq R_i^{\mathrm{true}}\subseteq R_i^+ .
\]

Let \(P^-\), \(P^{\mathrm{true}}\), and \(P^+\) be the corresponding finite presentations. Then

\[
\Gamma(P^-)\subseteq\Gamma(P^{\mathrm{true}})\subseteq\Gamma(P^+).
\]

**Proof.** If a global assignment satisfies every inner relation \(R_i^-\), then it satisfies every true relation because each row allowed by \(R_i^-\) is truly safe. Hence it is in \(\Gamma(P^{\mathrm{true}})\). If an assignment is truly safe, then every local row lies in \(R_i^{\mathrm{true}}\), hence in \(R_i^+\), so it lies in \(\Gamma(P^+)\). This is factorwise monotonicity.

For a symmetric positive-definite solve \(Ku=f\), with residual \(r=f-K\widehat u\) and certified lower spectral bound \(\underline\lambda\le\lambda_{\min}(K)\),

\[
\|u-\widehat u\|_2\le \frac{\|r\|_2}{\underline\lambda},
\qquad
|c^T(u-\widehat u)|\le \|c\|_2\frac{\|r\|_2}{\underline\lambda}.
\]

A row is placed in \(R^-\) only when the whole certified interval satisfies the safety inequality, and excluded from \(R^+\) only when the whole interval violates it. Threshold-crossing rows remain unresolved.

## Stage 13 artifact: exact spring demonstrator generation

The prototype now includes an exact generator:

```text
/home/user/finite_ecd_prototype/two_spring_generator.py
```

It generates the model

\[
u(f,a_1,a_2)=\frac{f-a_1-a_2}{2},
\qquad f\in\{1,2\},\quad a_1,a_2\in\{0,1\},
\]

with safety \(|u|\le 0.25\). The generated relations are

\[
R_1=\{(0,1),(1,0)\},
\qquad
R_2=\{(1,1)\}.
\]

The checked outputs are:

- same-observation generated instance: `CERTIFIED-UNSAT`;
- split-observation generated instance: `CERTIFIED-SAT`;
- one threshold sensor: `CERTIFIED-OPT` repair certificate verified by brute-force enumeration of smaller sensor subsets.

This remains a correctness demonstrator, not a performance benchmark.

## Stage 14 theorem: width-adaptive certified sparsification

For affine rows

\[
y_i(a)=d_i+\sum_{x\in S_i}g_{ix}a_x,
\]

retain \(J_i\subseteq S_i\) and bound the omitted terms by

\[
\underline\eta_i(J)=
\sum_{x\in S_i\setminus J_i}\min_{v\in D_x}g_{ix}v,
\qquad
\overline\eta_i(J)=
\sum_{x\in S_i\setminus J_i}\max_{v\in D_x}g_{ix}v.
\]

The inner sparse relation admits a retained assignment only if every completion of omitted variables is safe; the outer sparse relation admits it if some completion is not certified unsafe. If \(J_i\subseteq J_i'\), then the omitted interval shrinks, and therefore

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

This theorem is a mechanics-specific certificate theorem. It does not claim that sparsification will reduce runtime on real models; it claims that refinement is monotone and sound.

## Stage 15 artifact target: FE-to-ECD relation generation

The next implementation step is not a large FE code. The feasible target is a minimal relation generator with a stable interface:

```text
scenario data + actuator domains + response functional + safety threshold
    -> inner rows, outer rows, unresolved rows, row certificates
```

For affine examples the generator should use baseline plus actuator influence solves. For each row it should emit an `FE-ROW` certificate containing:

- scenario identifier;
- action tuple;
- approximate response;
- residual norm or exact arithmetic flag;
- coercivity lower bound or exact formula flag;
- certified response interval;
- classification: safe, unsafe, unresolved.

Only after this interface is stable should the project add larger truss/frame examples. This follows the rule: row certificates precede mechanical scaling claims.

## Stage 16 adjudication: \\(\mathsf D^{\mathsf P}\\) gap detection

The proposed gap-detection theorem should not yet be promoted to a main result. The safe current status is: **candidate theorem, not claimed**.

A typical gap predicate has the form

\[
\Gamma_A\ne\varnothing
\quad\text{and}\quad
\Gamma_B=\varnothing,
\]

where \(\Gamma_B\subseteq\Gamma_A\) are two declared layers, for example set-feasible versus catalogue-feasible or centralized-feasible versus distributed-feasible. For explicit finite encodings, membership in such a language is naturally in \(\mathsf D^{\mathsf P}\), because it is the conjunction of an NP statement and a coNP statement. Hardness, however, depends on the exact pair of layers and on a reduction that preserves the promise that the two spaces are nested.

Therefore the companion should use the following wording until a complete reduction is written:

> Gap detection belongs naturally to a difference-of-NP pattern once two nested finite layers are explicitly encoded. We do not use this observation as a complexity theorem unless membership and hardness are proved for the particular layers under discussion.

If retained, the appendix proof must specify:

1. the two finite presentations or layers \(A,B\);
2. the input representation;
3. the nesting proof \(\Gamma_B\subseteq\Gamma_A\);
4. membership in \(\mathsf D^{\mathsf P}\);
5. many-one or parsimonious hardness reduction;
6. preservation of nonempty-local-relation promises if those promises are used elsewhere.

## Stage 17 exact-hypothesis complexity statements

The broad dichotomy and parameterized-hardness claims should be included only with exact hypotheses.

### Fixed-template dichotomy

Safe statement:

> For fixed finite-domain constraint languages, CSP complexity is governed by the standard fixed-template dichotomy theory. This is background for interpreting special catalogue or relation languages. It is not a dichotomy for the variable explicit-table instances used by the general solver.

The companion should cite the appropriate Schaefer/Bulatov/Zhuk line depending on the domain and language actually used. Do not state a universal tractability classification for all finite ECD instances.

### ETH and parameterized lower bounds

Safe statement:

> Since finite ECD explicit-table synthesis contains standard CSP, hitting-set, and set-cover subproblems, the corresponding lower bounds transfer only under the same parameterizations and encodings as the source problems.

Before claiming W[1], W[2], or ETH lower bounds, the text must fix:

- parameter: treewidth, action budget, sensor budget, domain size, catalogue size, or horizon;
- encoding: explicit tables, forbidden tuples, circuits, or generated FE relations;
- reduction source;
- whether the reduction preserves bounded domain, bounded arity, or nonempty local relations.

### Nested-dissection mechanics claims

Safe statement:

> If certified sparsification produces retained scopes whose primal graph follows the separator structure of the mechanical substructure graph, then the DP inherits the corresponding separator width.

This remains conditional until a graph lemma links mechanical locality, retained influence scopes, and the policy primal graph.

## Stage 18 current reproducibility gate

The current executable artifact has a reproducibility gate at:

```text
/home/user/finite_ecd_prototype/run_repro_checks.py
/home/user/finite_ecd_prototype/repro_report.json
```

The gate performs:

- exact two-spring generation;
- same-observation infeasibility check;
- split-observation feasibility check;
- fibre-conflict certificate generation and verification;
- corrupted fibre-certificate rejection;
- optimal threshold-sensor repair generation and verification;
- corrupted sensor-repair rejection.

The current report has the expected statuses:

| Check | Expected status | Current status |
|---|---|---|
| same-observation generated instance | `CERTIFIED-UNSAT` | `CERTIFIED-UNSAT` |
| split-observation generated instance | `CERTIFIED-SAT` | `CERTIFIED-SAT` |
| fibre conflict certificate | `VERIFIED` | `VERIFIED` |
| corrupted fibre certificate | `REJECTED` | `REJECTED` |
| threshold sensor repair | `CERTIFIED-OPT` | `CERTIFIED-OPT` |
| sensor repair certificate | `VERIFIED` | `VERIFIED` |
| corrupted sensor repair | `REJECTED` | `REJECTED` |

This is not yet a mechanics benchmark suite. It is a correctness gate for the certificate grammar and the exact demonstrator.

## Stage 19 baseline-comparison boundary

No scaling superiority over SAT, CP-SAT, MILP, or join-tree baselines should be claimed yet. The only justified statement is:

> The current artifact verifies the smallest certificate layer and exact demonstrator. Comparative performance remains untested.

A fair baseline section requires, at minimum:

1. identical finite instances after relation generation;
2. documented encodings for SAT/CP-SAT/MILP;
3. join-tree baseline for acyclic permitted-table cases;
4. hardware, versions, random seeds, and time/memory limits;
5. separate accounting for FE preprocessing, relation generation, decomposition, solving, certificate generation, and verification;
6. timeouts reported as `INCONCLUSIVE`, not as failures of the baseline or successes of ECD.

Until those conditions are met, the companion may claim certificate structure and fixed-parameter width bounds, but not empirical advantage.

## Computational study required before applied-mechanics submission

A theorem-only manuscript is unlikely to fit an applied and computational mechanics venue. The computational study should be treated as a certification study, not merely as a speed test. The minimum deliverable is an end-to-end artifact that can produce a policy or a refutation certificate and then have that certificate checked by an independent verifier.

### Feasibility-ordered experimental roadmap

| Phase | Goal | Required outputs | Publication role |
|---:|---|---|---|
| 0 | Exact correctness harness | exhaustive enumeration for the two-spring model and other tiny hand-checkable CSPs; positive and negative certificates; corrupted-certificate rejection tests | Establishes that the certificate grammar and verifier are meaningful. |
| 1 | Finite relation-table solver | tree-decomposition DP on explicit tables; weighted-width reporting; SAT/CP-SAT/MILP encodings for the same finite instances; independent certificate verification | Supports the finite-algorithmic claims without relying on mechanics numerics. |
| 2 | Causal compilation tests | finite history-tree examples; forbidden-tuple compilation; reachability and inconsistent-path checks; comparison with brute-force policy enumeration | Validates the sensor-limited control compilation layer. |
| 3 | Certified FE relation generation | small linear spring/truss systems; residual and coercivity certificates; inner/outer row labels; unresolved-row accounting | Demonstrates that mechanics data can be converted into certified finite ECD instances. |
| 4 | Mechanics benchmark suite | 10-bar truss with quantized sensors; modular frame or mass-spring chain; cross-braced frame or two-dimensional lattice; dense-influence stress tests | Tests whether width, locality, and sensor structure appear in representative finite models. |
| 5 | Width-adaptive sparsification study | retained-scope ladders \(J\subseteq J'\); monotone inner/outer inclusions; width versus inconclusiveness tradeoff; ablations with no sparsification | Evaluates the main mechanics-specific contribution. |
| 6 | Comparative scaling study | tuned baselines; fixed hardware; fixed seeds; memory limits; all timeouts and unresolved cases reported explicitly | Only this phase can support claims about practical advantage over generic solvers. |

Phases 0--3 are the minimum credible computational package for a focused methods paper. Phases 4--6 are needed for a strong applied-mechanics submission and for any comparative performance claim.

### Implementation components

The artifact should contain:

- an implemented finite ECD solver;
- an independent verifier written against the certificate specification rather than the solver internals;
- exact small cases checked by exhaustive enumeration;
- finite-element relation-generation code;
- decomposition certificates;
- policy and refutation certificates;
- certificate corruption tests, including altered decomposition bags, altered separator messages, altered FE row bounds, and altered policy actions;
- reproducible scripts for every table and figure;
- explicit instance files preserving observations, domains, relations, implementation catalogues, costs, and sensor choices.

### Benchmark families

| Benchmark | Purpose | Earliest phase |
|---|---|---:|
| Exact spring and small truss systems | exhaustive correctness and certificate debugging | 0 |
| Synthetic finite CSP/ECD instances with controlled width | isolate width dependence from mechanics preprocessing | 1 |
| Finite inspection-actuation examples | causal compilation validation | 2 |
| 10-bar truss with quantized sensors | FE-to-ECD pipeline | 3 |
| Modular frame or mass-spring chain | fixed-width or slowly growing-width scaling | 4 |
| Cross-braced frame or 2D lattice | width-growth boundary | 4 |
| Dense influence instances | honest assessment of sparsification limits | 5 |
| Catalogue and budget instances | set/effective/bounded-tier diagnostics | 5 |

### Baselines

- exhaustive enumeration on small instances;
- SAT / CP-SAT encoding;
- MILP formulation;
- join-tree semijoin solver where applicable;
- tree-decomposition dynamic programming;
- width-adaptive certified solver.

The baseline comparison should be on identical finite instances after relation generation. FE preprocessing should also be reported separately so that a fast solver is not credited for omitted model-generation cost.

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
- table sizes by bag;
- unresolved numerical entries;
- inner/outer/inconclusive status;
- policy cost;
- core size;
- sensor-repair size;
- number of lazy sensor cuts;
- sparsification retained-scope size;
- baseline encoding size;
- timeout and memory-limit status.

### Certificate acceptance criteria

A reported theorem-backed computational result should be accepted only if the verifier confirms the corresponding object:

| Claimed outcome | Required certificate | Invalid substitutes |
|---|---|---|
| Safe policy for the finite model | policy assignment, observation-uniformity proof, relation-row certificates, and inner-model satisfaction | solver success log without checked row certificates |
| No policy for the finite model | outer-model UNSAT certificate, decomposition/message proof or exhaustive refutation, and certified exclusion of unsafe rows | inner UNSAT alone; solver timeout |
| No catalogue implementation | set-feasible witness plus checked impossibility or optimization certificate for finite-cost catalogue variables | failure of a heuristic catalogue search |
| Budget exceeds \(B\) | checked minimum-cost certificate or refutation of all cost-\(\le B\) assignments | inability to find a low-cost policy |
| Sensor repair optimality | hitting-set optimality certificate plus conflict cores generated under the selected sensors | a locally minimal sensor set |
| Sparsified result | inclusion certificate showing \(\Gamma^-_J\subseteq\Gamma^-_{J'}\subseteq\Gamma^{\mathrm{true}}\subseteq\Gamma^+_{J'}\subseteq\Gamma^+_J\) for the tested ladder | empirical agreement of sparse and dense solutions on sampled actions |

Timeouts, failed numerical certification, and unresolved inner/outer gaps should be reported as inconclusive, not merged with proven infeasibility.

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


## Remaining implementation-plan and source-audit adjudication

A further pass over `humanization-implementation-plan.md`, `humanized-baseline-verification.md`, `qwen halting upgrades.txt`, `halting additions audit.txt`, and `grok, gemini halting audit2.txt` leaves the following actionable status.

### Foundational monograph items

| Source point | Adjudication | Action taken / current status |
|---|---|---|
| Avoid informal humanized phrases such as “In plain terms.” | Worth implementing where it appears in formal theorem prose. | Replaced the remaining occurrence in the foundational monograph with “Operationally.” |
| Signpost the variance of nested-prefix diagrams versus later patch categories. | Worth implementing; readers can otherwise mistake “no initial object” for a variance switch. | Added a variance-convention remark after the nested-prefix definition in `monograph-revised-v40.tex`. |
| External results are cited rather than reproved. | Worth making explicit; not a flaw if framed correctly. | Added relation-to-frameworks caveat in `monograph-revised-v40.tex` listing standard imported results. |
| Terminal compression should be emphasized as a distinctive contribution. | Already implemented in the abstract, notation table, introduction, compression spectrum, structural spine, and conclusion. | No further edit needed now. |
| Global information recall/action-recall boundary with Kuhn. | Already implemented in v34 with strategic-mixed preservation and behavioural-strategy caution. | No companion action. |
| Bell repair subsection needs physical-model caveats. | Already implemented and further caveated. | No further edit unless adding experimental Bell data, which is outside this project. |
| Protocol complexes, measurable kernels, quantum process extensions, infinite arenas. | Correctly remain source-doctrine modules. | Kept in dependency ledger; do not promote without definitions. |

### Companion algorithms/mechanics items

| Source point | Adjudication | Action taken / current status |
|---|---|---|
| The companion should be proof-producing finite algorithmics, not a broad ECD summary. | Central and already adopted. | v10 retains this as editorial identity. |
| Finite input schema and certificate grammar must precede algorithms. | Implemented. | Stages 1--2 drafted in v6. |
| Exact small demonstrator and corrupted-certificate rejection should come before benchmarks. | Implemented. | Prototype and `run_repro_checks.py` execute this gate. |
| Width DP, weighted width, join-tree certificates, sensor repair. | Implemented as theorem/certificate drafts. | Stages 7--10 drafted in v7. |
| FE inner/outer and sparsification soundness before mechanics claims. | Implemented as theorem/interface drafts. | Stages 12--15 drafted in v8. |
| DP gap detection, ETH, W-hardness, Schaefer/Zhuk. | Should remain cautious until exact reductions/hypotheses are written. | v9 marks these as candidate or fixed-hypothesis statements only. |
| Scaling superiority over CP-SAT/MILP. | Not claimable. | v9 states baseline boundary and required evidence. |

### Remaining worthwhile next implementations

The first three implementation-level items have now been completed in `/home/user/finite_ecd_prototype/`:

1. a small tree-decomposition DP verifier;
2. emitted and verified `TREE-DECOMP`, `DP-REFUTATION`, and `DP-OPTIMUM` certificates on tiny instances;
3. a minimal exact affine row generator producing and verifying `FE-ROW` certificates for the two-spring affine model.

The current reproducibility gate is `run_repro_checks.py`, with results in `repro_report.json`. It verifies positive certificates and rejects corrupted fibre, sensor, DP, and FE-row certificates.

These next implementation items have now also been completed in the prototype:

1. an exact affine sparsification certificate checker for omitted-term intervals;
2. nontrivial supplied path-decomposition examples with `DP-OPTIMUM` and `DP-REFUTATION` certificates;
3. dependency-free baseline encoders for Boolean explicit-table instances: DIMACS SAT, LP-format MILP, and a minimal CP-SAT forbidden-tuple JSON representation.

The baseline encoders do not run external solvers and do not support performance claims. They only ensure that future comparisons use identical finite instances.

These next implementation items have now also been completed in the prototype:

1. a small generated benchmark library for Boolean path and binary-tree families with known treewidth 1;
2. verifier-side sparsification ladder checks for retained scopes `J\subseteq J'`;
3. an optional external-solver adapter that reports missing executables, timeouts, and unrecognised output as `INCONCLUSIVE`;
4. a larger exact four-actuator affine frame-style finite algebraic example with verified `FE-ROW` and DP certificates.

These next implementation items have now also been completed in the prototype:

1. external solver results can be cross-checked against native ECD policy or `DP-REFUTATION` certificates, without trusting solver logs;
2. additional controlled-width benchmark families are available: banded chains and grids with supplied decompositions;
3. a report generator summarizes instance size, factor rows, width, weighted width, certificate size, verification status, and verification time;
4. fair external baseline experiments remain explicitly gated until fixed hardware and solver configurations are available.

These next implementation items have now also been completed in the prototype:

1. optional adapters detect and run `minisat`, `kissat`, or `z3` only when available, otherwise reporting `INCONCLUSIVE`;
2. dependency-free SVG plots are generated for certificate size versus weighted width and verification time versus certificate size;
3. scripted controlled-width sweeps generate path, banded-chain, and grid benchmark batches with native certificate verification;
4. an artifact manifest records scripts, reproduction commands, status discipline, and repository-deposit checklist.

These next implementation items have now also been completed or safely gated in the prototype:

1. repository-ready reproduction entry points exist: `make reproduce` and `./reproduce.sh`;
2. `ARTIFACT_APPENDIX.md` summarizes instance formats and certificate schemas;
3. `run_external_baselines.py` records solver availability and reports `INCONCLUSIVE` when supported solvers are unavailable;
4. `RELEASE_MANIFEST_TEMPLATE.md` is ready to freeze once the final repository or DOI link is supplied.


## Artifact appendix and release-link status

A polished LaTeX artifact appendix has been prepared at:

```text
/home/user/companion-artifact-appendix-v1.tex
```

It summarizes the finite instance format, native certificate schemas, FE-row and sparsification certificates, baseline encodings, external-solver discipline, reproduction commands, and claim boundary. This appendix can be inserted into the eventual companion article with minor formatting adjustments.

Repository and DOI fields remain intentionally unfilled. The release manifest cannot be frozen until the artifact is deposited and a repository URL, archival DOI, release tag or commit hash, and freeze date are available. The current template remains:

```text
/home/user/finite_ecd_prototype/RELEASE_MANIFEST_TEMPLATE.md
```

The external-baseline runner was executed again. In the current environment no supported external solver is installed, so the report remains `INCONCLUSIVE` rather than a performance result:

```text
/home/user/finite_ecd_prototype/reports/external_baselines.json
```

When a repository or DOI link is available, insert it in this plan, the release manifest, and the companion article. Until then, the paper should use placeholder wording such as: “An artifact containing the finite ECD prototype and reproduction scripts will be deposited in a public repository before publication.”

The next genuinely worthwhile items are now editorial/release tasks rather than new mathematics or implementation:

1. copy the artifact appendix into the companion article appendix in polished form;
2. freeze a release manifest after repository deposit;
3. insert the repository/DOI link into the companion plan and eventual paper;
4. if external solvers are later available on fixed hardware, run baseline experiments and attach the resulting report without changing the native certificate claims.

Items not worth implementing now: broad game-theory mixed/behavioural semantics, noninvertible empirical functoriality, protocol-complex impossibility theorems, measurable-kernel descent, and continuum mechanics claims. Each lacks the required source doctrine for a safe theorem in the current manuscripts.

## Remaining development tasks in topological-feasibility order

The following order is the working order for the companion monograph. A later item should not be promoted to a main claim until the blocking earlier items have been completed.

| Stage | Task | Depends on | Feasibility status | Output needed |
|---:|---|---|---|---|
| 1 | Formalize the finite input model, including variables, domains, relations, observations, implementation catalogues, costs, and budgets. | none | drafted in v6 | canonical instance schema and examples |
| 2 | Define the certificate grammar for policies, refutations, decompositions, costs, FE rows, sensor repairs, and sparsification inclusions. | 1 | drafted in v6 | verifier-facing certificate specification |
| 3 | Prove the fibre selector algorithm and the at-most-\(|A|\) conflict-certificate bound. | 1--2 | theorem draft complete | theorem plus small demonstrator certificates |
| 4 | Prove reachability-correct causal compilation from finite history trees to forbidden-tuple presentations. | 1--2 | theorem draft complete | theorem plus brute-force cross-check on tiny arenas |
| 5 | Prove the explicit-table NP/\(\#\)P/coNP frontier. | 1 | standard cases drafted | reductions with nonempty-local-relation promises |
| 6 | Implement a prototype finite-table solver and independent verifier. | 1--4 | first prototype complete | `/home/user/finite_ecd_prototype/` implements explicit-table checks and fibre certificates |
| 7 | Develop the diagnostic semiring DP with proof objects. | 2, 6 | theorem/proof-object draft in v7 | recurrence, certificates, verifier checks |
| 8 | Prove weighted-width complexity bounds and report actual table sizes. | 7 | theorem draft in v7 | theorem plus instrumentation |
| 9 | Prove acyclic/join-tree certificate extraction for permitted tables. | 1--2 | certificate draft in v7 | cited theorem specialization plus certificate trace |
| 10 | Prove one-shot sensor-repair hitting-set theorem and lazy cut correctness. | 3, 6 | theorem draft in v7 | optimality certificate for selected sensors |
| 11 | Develop promise-hardness reductions for catalogue effectiveness and budget boundedness. | 1, 5 | reduction pattern drafted in v8 | checked reductions using finite catalogues and wildcard implementations |
| 12 | Prove FE inner/outer relation soundness for the discrete algebraic model. | 1--2 | theorem draft in v8 | residual/coercivity row certificates |
| 13 | Generate exact small spring/truss benchmarks. | 6, 12 | two-spring generator complete | exhaustive comparisons and certificate rejection tests |
| 14 | Prove width-adaptive certified sparsification. | 12 | theorem draft in v8 | monotone inclusion theorem and retained-scope certificates |
| 15 | Build certified FE-to-ECD relation-generation code. | 12--14 | interface specified in v8 | reproducible preprocessing pipeline |
| 16 | Adjudicate the proposed \(\mathsf D^{\mathsf P}\) gap-detection result. | 5, 11 | adjudicated as candidate only in v9 | either a complete proof or removal to conjectural remarks |
| 17 | State Schaefer/Zhuk, ETH, W[1], and W[2] claims only with exact fixed-template or parameterized hypotheses. | 5, 10--11 | safe wording drafted in v9 | cited theorem statements, not broad informal claims |
| 18 | Design and execute reproducible mechanical experiments. | 6--15 | correctness gate executed in v9; mechanics suite still open | benchmark tables with all inconclusive cases separated |
| 19 | Compare against SAT/CP-SAT/MILP and join-tree baselines. | 18 | boundary conditions specified in v9; no comparison claim yet | fair encodings, hardware details, seeds, limits, and certificate checks |

This ordering deliberately places the finite model, certificate language, and verifier before FE experiments or solver comparisons. It also postpones \(\mathsf D^{\mathsf P}\), ETH, and W-hardness claims until the simpler explicit-table reductions and sensor-repair reductions are settled.

## Cross-monograph placement of open items

| Item | Foundational monograph placement | Algorithms/mechanics placement | Rule-imposed action |
|---|---|---|---|
| Presentation-relative diagnostics | central theorem layer | background motivation | keep foundational; use in companion only to explain diagnostics |
| Morphisms, compression, and certificate transport | central theorem layer | optional background for certificates | avoid re-proving broad categorical claims in the companion |
| Global information recall and action-recall redundancy | scoped arena lemma | not central | keep in foundational monograph; game-theory expansion requires separate expected-utility semantics |
| Bell/contextuality repair profiles | foundational application module | not in mechanics article | keep separate unless used as an analogy |
| Weihrauch/reverse mathematics | foundational computability module | not in finite article | exclude from focused mechanics paper |
| Finite CSP complexity | supporting background only | central theorem package | develop in companion after finite encoding is fixed |
| Width and weighted-width DP | not central | central algorithmic contribution | develop after certificate grammar |
| Independent verifier | artifact note only | central correctness mechanism | implement before performance claims |
| FE inner/outer soundness | outside foundational scope except as source doctrine | central mechanics theorem | prove for discrete algebraic model before continuum claims |
| Certified sparsification | source-domain-specific module | central mechanics theorem | prove monotone inclusions before experiments |
| CP-SAT/MILP comparisons | not foundational | empirical section only | claim only after reproducible benchmarks |

## v18: external baseline runs executed, release manifest frozen

The gated external-baseline items have now been implemented and executed; the
repository links have been inserted.

### External solvers installed and recorded

minisat (2.2 series, arminbiere mirror commit 16982a5, gcc 14.2, with the
standard gcc compatibility patch on `core/SolverTypes.h`), kissat 4.0.4
(commit 8af8e56), z3 5.1.0, OR-Tools CP-SAT 9.15.6755, and HiGHS 1.15.1 are
installed for the recorded experiment. Versions, invocation flags, and build details are
recorded in `finite_ecd_prototype/RELEASE_MANIFEST.md`.

### Fixed-hardware baseline experiment executed

`finite_ecd_prototype/external_baseline_sweep.py` (with `cpsat_runner.py`
and `highs_runner.py`) runs the comparison under a fixed protocol: 60 s wall-clock timeout, 3 GiB
address-space cap, three repetitions per solver and instance with median
timing, single-threaded deterministic configurations, and identical Boolean
explicit-table instances from the controlled-width families plus an
unsatisfiable odd-ring family, encoded by `baseline_encode.py` to DIMACS CNF,
the minimal CP-SAT forbidden-tuple encoding, and the LP-format MILP encoding.

Recorded outcome (`reports/external_baseline_sweep.json`):

- 24 instances, 120 external runs across five solvers;
- all 24 native DP certificates independently re-verified;
- all 19 satisfiable-instance policies reconstructed from certificates and
  verified;
- all 95 external SAT models parsed and verified natively as policies;
- all 25 external UNSAT answers cross-checked against verified
  `DP-REFUTATION` certificates;
- 120/120 status agreement with the native certificates; zero inconclusive or
  rejected runs;
- peak external resident set size at most about 101 MiB against the 3 GiB cap.

At the recorded certificate-study sizes the compiled SAT solvers finish in
milliseconds, the CP-SAT process takes roughly 0.35--0.62 s, the HiGHS
process roughly 0.11--0.27 s including interpreter startup, and the Python DP
reference completes in 0.001--0.69 s.
The experiment supports reproducibility and cross-checking claims only. No
external-solver performance superiority claim is made, consistent with the
Stage 19 boundary: the comparative scaling study (phase 6) remains future
work and requires tuned baselines, larger and harder instance families, and
separate accounting for FE preprocessing.

### Reproduction gate and smoke gate updated

`make reproduce` and `./reproduce.sh` now include the gated
`external-baselines` step; without installed solvers the emitted report is
`INCONCLUSIVE`. `run_external_baselines.py` runs z3 directly on the DIMACS
smoke instance; the smoke report is `COMPLETE_WITH_AVAILABLE_SOLVERS` in the
recorded environment. `README.md` documents the sweep, its environment
variables (`EXTERNAL_ECD_MINISAT`, `EXTERNAL_ECD_KISSAT`, `EXTERNAL_ECD_Z3`,
`EXTERNAL_ECD_CPSAT_PYTHON`, `EXTERNAL_ECD_HIGHS_PYTHON`), and its output
file.

### Release manifest frozen

`finite_ecd_prototype/RELEASE_MANIFEST.md` records the repository URL
(https://github.com/MIKEAA2020/halting-physics), release tag
`halting_physics_workspace_v3`, the recorded environment, solver versions and
build provenance, reproduction commands, expected outputs, the fixed baseline
protocol, the claim boundary, and the files to archive. The DOI field stays
open until an archival identifier is assigned at publication time.

### Companion manuscript and appendix versioned

The companion article reports the experiment in a dedicated
external-baseline subsection with the fixed protocol, a results table, and
the claim boundary, and references the public repository and release tag. The
artifact appendix documents the fixed configuration and the sweep command.
New files: `companion monograph/monograph-2-algorithms-and-certificates-v4.tex`
and `companion monograph/companion-artifact-appendix-v3.tex`; earlier
versions are unchanged.

### Remaining items

1. assign and insert the archival DOI at publication time;
2. mechanics benchmark suite phases 4--6 of the experimental roadmap (10-bar
   truss and frame families, sparsification study, tuned comparative scaling
   study) before any applied-mechanics submission;
3. freeze a release manifest refresh at each future artifact release.

## v19: mechanics benchmark phases 4--6 executed

Session status: the remaining pre-submission item of the v18 plan (item 2,
mechanics benchmark suite phases 4--6) has been executed and recorded. The
remaining-items list is now:

1. assign and insert the archival DOI at publication time;
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. freeze a release manifest refresh at each future artifact release
   (done for this release: tag `halting_physics_workspace_v4`).

### Phase 4: mechanics benchmark suite

Implemented in the prototype:

- `mechanics_fe.py`: exact rational structural front end for declared
  pin-jointed trusses (rational 3-4-5 member directions) and grounded
  mass-spring chains; node-force and self-equilibrated member-pair
  actuators; member-force and displacement monitors; certificates
  `MECH-SOLVE` (verified by exact residual substitution against an
  independently assembled stiffness matrix), `MECH-ROW-BATCH` (verified by
  regeneration through independently written assembly and solve code, with a
  recorded relation-enumeration cap and explicit `RELATION-TABLE-LIMIT`
  markers), `MECH-SPARSIFY-BATCH`, and exact row-level policy verification.
- `mechanics_gen.py`: the four families (ten-bar cantilever with quantized
  load scenarios; pre-tensioned chain with exactly local influence; dense
  chain; cross-braced lattice with width growth), same/split observation
  variants, deterministic minimum-fill decompositions, ten-bar affine
  cross-validation model, and sensor-repair data.
- `mechanics_benchmarks.py`: the recorded gate (20 cases, all row batches
  verified, 9 verified refutations and 9 verified optimum policies, lattice
  relation-table limits at C=3,4, corrupted-certificate rejections, sensor
  repair certified optimal with one threshold sensor).
- A semantics-preserving performance fix in `finite_ecd.py`
  (separator-indexed child summaries instead of per-assignment child
  re-enumeration; cached factor relations) was required for the width-15
  bags; the recorded external-baseline sweep reproduces identically after
  the fix.

### Phase 5: width-adaptive sparsification study

`sparsification_study.py` records retained-scope ladders by member-graph
proximity with verified monotonicity (20 sparsification certificates, 14
ladder steps), inner/outer brackets for both observation variants, and the
unresolved-fraction tradeoff. Recorded finding: unresolved fractions
decrease monotonically with radius, brackets certify only at or near the
full radius, and intermediate radii need not reduce the decomposition width;
the ladder theorem is certified, no practical width-reduction benefit is
claimed. The chain-pretension family is the no-sparsification ablation
(singleton scopes, width 0).

### Phase 6: comparative scaling study on mechanics instances

`mechanics_baseline_sweep.py` with `native_dp_runner.py` applies the fixed
external-baseline protocol to fourteen mechanics-derived Boolean instances
with the native pipeline as a bounded isolated process and FE preprocessing
accounted separately. Recorded: 70 external runs, 67 agreements with native
certificates, 3 explicit timeouts (minisat on the dense family at n=16,
HiGHS on the unsatisfiable dense instance), 34 SAT models verified natively,
33 UNSAT answers cross-checked against verified refutations. Per-instance
observations only; no superiority claim. A latent HiGHS version-probe call
bug in `external_baseline_sweep.py` was fixed (missing list brackets).

### Artifact and manuscript versions

- New: `finite_ecd_prototype/mechanics_fe.py`, `mechanics_gen.py`,
  `mechanics_benchmarks.py`, `sparsification_study.py`,
  `mechanics_baseline_sweep.py`, `native_dp_runner.py`;
  `reports/mechanics_benchmarks.json`,
  `reports/sparsification_study.json`,
  `reports/mechanics_external_baseline_sweep.json`;
  `finite-ecd-prototype-implementation-report-v8.md`; refreshed
  `finite_ecd_prototype/RELEASE_MANIFEST.md`.
- Manuscript: `companion monograph/monograph-2-algorithms-and-certificates-v5.tex`
  and `companion monograph/companion-artifact-appendix-v4.tex`; earlier
  versions unchanged.
- Release: `halting_physics_workspace_v4` with the full workspace; earlier
  releases unchanged.
- Gate: `make reproduce` includes `mechanics-benchmarks`,
  `sparsification-study`, and `mechanics-baselines`; the smoke gate adds
  ten-bar and chain-16 checks.
- Archive note: the dense-chain n=16 baseline encodings and the
  byte-identical duplicate native DP certificates are regenerable and are
  excluded from the archive; the study report references the phase 4
  certificates.

## v20: root-fix pass on the companion manuscript

Session status: a line-level audit of
`companion monograph/monograph-2-algorithms-and-certificates-v5.tex` was
resolved into a root-fix revision
`companion monograph/monograph-2-algorithms-and-certificates-v6.tex`
together with `companion monograph/companion-artifact-appendix-v5.tex`;
earlier versions are unchanged. The ground truth for the recorded-data
reconciliation was the implementation report
`finite-ecd-prototype-implementation-report-v8.md` (release tag
`halting_physics_workspace_v4`). The GitHub access token for the repository
is persisted in the working environment (git credential store plus
`~/.github_token`). The v6 manuscript compiles cleanly under tectonic with
no new typographical warnings relative to v5.

### Mathematical fixes (v6)

1. The one-shot sensor-repair theorem is restated over inclusion-minimal
   conflict cores, with cores now required to lie within a single
   observation fibre, and is proved in both directions; a remark records why
   minimal failing fibres are the wrong objects (a fibre may fail through a
   small core while the selected sensors separate only scenarios outside
   it). The v5 wording over "minimal failing fibres" was not exact: whole
   failing fibres are never minimal as cores unless they coincide with them.
   The two-spring demonstrator now instantiates the corrected theorem (its
   fibre is its own unique minimal core).
2. The inner--outer finite soundness proposition now carries a proof and an
   explicit shared-presentation hypothesis.
3. The width-DP section now defines separator-indexed message tables
   semantically, proves the private-variables/factor-separation lemma and a
   recurrence-correctness lemma, and restates the DP certificate soundness
   proposition with a complete proof rooted at the running-intersection
   property. This also documents, at the theory level, the
   separator-indexed child summaries used by the implementation's
   performance fix of phase 4.
4. The sparsification ladder proof is completed: the five inclusions are
   proved assignment by assignment (fine completions fix newly retained
   variables to the assignment's own values; coarse outer completions extend
   the fine witness by those values), with the interval nesting stated
   explicitly; the sparse policy spaces are defined before the theorem.
5. A remark separates value costs (per-assignment costs used by
   DP-OPTIMUM) from catalogue costs (per-implementation costs), repairing the
   undefined cost notion behind v5's DP-OPTIMUM claim; the observation fibre
   is defined before the fibre criterion; Table 1 is now referenced in the
   text.

### Recorded-data reconciliation (v6)

6. Mechanics baseline accounting: the recorded summary counters (34 SAT, 33
   UNSAT, 3 inconclusive, 67 agreements) are arithmetically inconsistent
   with the per-instance records, which show four non-answers on the
   dense-chain n=16 instances (minisat TMO on both variants, HiGHS TMO on
   the unsatisfiable variant, CP-SAT UNKNOWN within its limit on the
   unsatisfiable variant) while 34+33+3=70 forces the CP-SAT UNKNOWN run to
   be counted among the cross-checked unsatisfiable answers. The only
   consistent reconciliation is 34 SAT, 32 UNSAT, 3 TMO plus 1 UNKNOWN
   inconclusive, and 66 status-bearing agreements; the summary counter
   evidently buckets an UNKNOWN status with the UNSAT answers (an
   `ext_status in ("UNSAT","UNKNOWN")`-style branch). The manuscript reports
   the corrected accounting with a footnote documenting the discrepancy and
   the harness re-audit; Table 5 marks the CP-SAT cell as UNK, and the
   observations paragraph now agrees with the table and the accounting.
7. Table 2 statuses use the four-status vocabulary with a caption
   definition (UNSAT/OPT abbreviating CERTIFIED-UNSAT/CERTIFIED-OPT as
   verified DP-REFUTATION/DP-OPTIMUM certificates); the marker is unified
   to RELATION-TABLE-LIMIT everywhere (v5 used TABLE-LIMIT in the body and
   RELATION-TABLE-LIMIT in the appendix); the universal claims are scoped
   to the eighteen constructed instances (twenty recorded cases minus the
   two scope-only lattice cases at C=3,4), matching the recorded gate
   counts (row batches 20, decompositions 18, DP certificates 18,
   refutations 9, optima 9, relation-table limits 2).
8. The sparsification table caption now states the complete rung inventory,
   which is uniquely determined by the recorded counts (rungs 20, ladder
   steps 14, brackets 9 certified + 11 inconclusive per variant, families
   6, and the per-family radius series of the report): ten-bar and
   dense-chain ladders of five radii each, the single-rung chain ablation,
   and lattice ladders of four, three, and two radii at column counts one,
   two, and three. The compressed radius ranges are explained (consecutive
   certified rungs; displayed values are the finest rung's, whose inner
   widths match the full-instance widths of the benchmark table).
9. The abstract's duplicated cross-check sentence is merged; the appendix
   FE-ROW schema is aligned with the grammar's three row statuses (exact
   rows are SAFE/UNSAFE; UNRESOLVED arises only for interval rows); the
   appendix cross-checking discipline now lists solver statuses without a
   certified claim (CP-SAT UNKNOWN) among the inconclusive outputs; a
   bookkeeping-marker paragraph in the status-discipline remark
   distinguishes gate markers from the four answer statuses.
10. A new Appendix B records the standard reductions behind the complexity
    table (2-SAT for Boolean binary, 3-SAT for ternary, 3-colourability for
    three-domain disequality, coNP and #P complements, and set cover for
    minimum-cardinality fibre obstruction), all under the
    nonempty-local-relation promise, and a seventeen-entry bibliography
    replaces the previously uncited frontier (Schaefer/Zhuk dichotomy, ETH,
    W[1]/W[2], treewidth sources, certifying algorithms).

### Remaining items

1. re-audit the mechanics baseline summary counter (item 6) in the harness
   and regenerate `reports/mechanics_external_baseline_sweep.json` at the
   next release, so the recorded summary agrees with the per-instance
   records;
2. assign and insert the archival DOI at publication time (unchanged);
3. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
4. freeze a release manifest refresh at the next artifact release.

## v21: phase-6 replication, dense-family extension, and the accounting audit

Session status: the full phase-6 comparative scaling study was replicated
under version-exact solver provenance, the dense-influence family was
extended to n=17 and n=18 with generation and comparative sweep, the
carried harness-accounting flaw was resolved at the root by a forensic
audit plus an evidence-gated harness counter, and the manuscript passages
that the audit proves wrong were corrected. New documents:
`companion monograph/monograph-2-algorithms-and-certificates-v7.tex`
(compiles under tectonic with no new typographical warnings relative to
v6; two pre-existing overfull boxes in untouched sections remain),
`companion monograph/companion-artifact-appendix-v6.tex`,
`finite-ecd-prototype-implementation-report-v9.md`, this plan, and the
repository worklog `repository-worklog.md`. Earlier versions are
unchanged.

### Phase-6 sweep replication (version-exact)

All five solvers were rebuilt or pinned to the recorded versions (minisat
rebuilt from the arminbiere mirror at commit 16982a5 with gcc 14.2 at
-O3 and the mkLit compatibility patch; kissat 4.0.4 at commit 8af8e56;
z3 5.1.0; OR-Tools CP-SAT 9.15.6755; HiGHS 1.15.1) and the complete
fourteen-instance sweep was re-executed under the fixed protocol, in case
chunks equivalent to a single invocation. The replicated report
`finite_ecd_prototype/reports/mechanics_external_baseline_sweep_v2.json`
reproduces the recorded summary exactly (14 native certificates, 7
policies, 34/33/3/0/67 external accounting) and every structural field;
the only differences are certificate file names, and the re-emitted native
certificates are byte-identical (SHA-256 equality verified on dense,
ten-bar, and lattice spot checks). The chunked invocation, checkpointed
per unit, is documented in the report.

### Dense-family extension n=17/18 (phases 4 and 6)

Two deposited drivers extend the recorded studies beyond the dense-family
boundary n=16 with the recorded drivers and protocol unchanged:
`dense_extension_generate.py` (phase-4 driver, per-case checkpointing)
and `dense_extension_sweep.py` (phase-6 protocol, per-(case, solver)
checkpointing). Generation certifies all four FE row batches and
decompositions (widths 16, 16, 17, 17) and three DP certificates
(REFUTATION at 17 same, 120.2 MB; OPTIMUM with verified policy at
17 split, 243.2 MB; REFUTATION at 18 same, 252.5 MB); the 18 split case
is recorded as DP-MEMORY-LIMIT (in-process certificate emission killed by
the OOM killer at about 3.75 GiB resident, exit 137; model, certified row
batch, instance, and validated decomposition archived). The sweep records
20 external runs: seven verified satisfiable models, three verified
unsatisfiable answers (all cross-checked), ten inconclusive, none
rejected, seven agreements; the bounded native run of 18 split raises
MemoryError at the 3 GiB address-space cap. Observations: minisat
exceeds the limit on all four instances; CP-SAT returns unknown within
its limit on the three heaviest variants; kissat is the only solver
answering the unsatisfiable 18 same variant within the limit (52.2 s);
on the satisfiable 18 split variant kissat, z3, and HiGHS return models
that verify natively while the certificate-emitting native DP cannot
complete within the same cap.

### Harness accounting audit and root fix (resolves the v20 item 6 defect report)

The forensic audit of this round establishes that the recorded summary
counters were never inconsistent with the per-instance records: the
CP-SAT run on dense-chain n=16 same answered UNSAT (49.5 s median) with a
verified cross-check, not UNKNOWN; exactly three non-answers exist
(minisat on both dense-16 variants, HiGHS on the unsatisfiable one);
34+33+3 = 70; the counters agree with the per-instance records in the
recorded external-baseline sweep (95/25/0/120), the recorded mechanics
sweep, and the v2 replication. Code inspection shows a CP-SAT UNKNOWN can
never be bucketed with unsatisfiable answers (cpsat_runner.py maps
UNKNOWN to INCONCLUSIVE and a None classification), and the recorded
artifact is byte-identical across the release-v4 archive, the
recorded-reports extraction, the live prototype, and the repository
(SHA-256 acd666e3...). The v20 item 6 "only consistent reconciliation"
(32/4/66) and the v6 footnote asserting it are therefore themselves
documentation errors and are withdrawn in the v7 manuscript.

The root-cause remediation lives in the harness code: the
status_agreement_with_native counter in external_baseline_sweep.py,
mechanics_baseline_sweep.py, and dense_extension_sweep.py is now gated on
verified cross-check evidence, so a rejected or evidence-free answer can
never be counted as an agreement (the latent over-counting hole behind
the v20 hypothesis). verify_accounting_fix.py proves the change
semantics-preserving on every recorded sweep (recorded = old = fixed:
120/120, 67/67, 67/67). The recorded
reports/mechanics_external_baseline_sweep.json is deliberately NOT
regenerated: it is already consistent, and regeneration would overwrite
the user's original artifact, contrary to the version discipline. The v20
remaining item 1 is thereby resolved without regeneration.

### Manuscript corrections (v7) and appendix (v6)

1. The comparative-scaling table's CP-SAT cell for dense n=16 same
   changes from UNK to the recorded 49.5 s; the observations paragraph
   states that CP-SAT certifies the unsatisfiable dense instance in about
   50 seconds; the cross-check accounting paragraph reports the
   audit-verified recorded accounting (33/3/67); the v6 footnote is
   replaced by the audit statement; the withdrawn "corrected accounting"
   is documented as withdrawn.
2. Table 3 displays the recorded values exactly (0.67, 3.56, 5.56, 6.67
   replacing the one-decimal roundings) and its caption states the true
   rung inventory (ten-bar four radii, two-rung chain-pretension
   ablation, dense-chain five, lattices four/three/two; 20 rungs, 14
   ladder steps). crosscheck_table3.py verifies every displayed value
   against reports/sparsification_study.json, which is deposited in the
   repository.
3. A new subsubsection documents the version-exact replication and the
   dense-family extension with its table, the 3 GiB memory wall at
   n=18 split, and the honest boundary statement; the artifact paragraph
   records the checksum-manifest policy for artifacts above the
   repository's 100 MB per-file limit.
4. The appendix adds the extension drivers and commands, the
   checkpointing discipline, the replication report, the large-artifact
   manifest policy, and the evidence-gated agreement counter to the
   cross-checking discipline; the claim boundary records the certificate
   growth and memory boundary as artifact properties, not performance
   claims.

### Repository deposit

New files only (nothing overwritten): the v2 replication report and eight
extension reports under finite_ecd_prototype/reports/; the extension
drivers, the manifest builder, and the audit tools
(audit_sweep_summary.py, crosscheck_table3.py, diff_reports.py,
verify_accounting_fix.py) under finite_ecd_prototype/; the evidence-gated
counter fix in external_baseline_sweep.py and
mechanics_baseline_sweep.py as a dedicated bug-fix commit; thirty-seven
small dense-17/18 example artifacts with examples/SHA256SUMS extended;
the large-artifact checksum manifest
reports/dense_extension_large_artifacts.json; the companion monograph
v7 and artifact appendix v6; implementation report v9; this plan; and
repository-worklog.md.

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. freeze a release manifest refresh at the next artifact release,
   incorporating the v2 replication and dense-extension outputs.

## v22: audit of v7 against the deposited artifact, and the v8 correction pass

Session status: a full line-level audit of the v7 manuscript and appendix v6
was performed against the now-deposited artifact ground truth (the recorded
JSON reports and harness source in `finite_ecd_prototype/`), every recorded
number in the manuscript was re-derived from the reports, and the residual
flaws found were corrected at their root in companion monograph v8 and
artifact appendix v7. New documents:
`companion monograph/monograph-2-algorithms-and-certificates-v8.tex` (compiles
under tectonic with zero overfull boxes, improving on v5-v7 which carried two),
`companion monograph/companion-artifact-appendix-v7.tex`, implementation
report v10, this plan, and the repository worklog round 4. Earlier versions
are unchanged.

### What the audit confirmed

- The v7 withdrawal of the v6 "corrected accounting" (32/4/66) is correct and
  complete: the recorded summary is 34/33/3/0/67 and the per-instance records
  agree; the CP-SAT dense-16 same run answered UNSAT at 49.5 s with a
  verified cross-check; `cpsat_runner.py` maps UNKNOWN to INCONCLUSIVE by
  construction; the recorded artifact's SHA-256 is
  `acd666e340da4fb08b58f727b2259a6eba5749b76fd9d2eb6440f3cfec6c4226`.
- Every value of Tables 2, 3, 5, and 6 was re-derived from
  `reports/mechanics_benchmarks.json`, `reports/sparsification_study.json`,
  `reports/mechanics_external_baseline_sweep.json`, and
  `reports/mechanics_dense_extension_sweep.json` and matches: the 20-case
  gate (18 constructed + 2 scope-only, 20 row batches, 18 decompositions, 18
  DP certificates, 9 refutations + 9 optima), the rung inventory (ten-bar 4,
  chain 2, dense 5, lattice 4/3/2 = 20 rungs, 14 ladder steps) with the v7
  corrected lattice values (0.67, 3.56, 5.56, 6.67), all fourteen recorded
  sweep rows including the 49.5 s CP-SAT cell, the extension table and its
  accounting (7 SAT, 3 UNSAT, 10 inconclusive, 0 rejected, 7 agreements),
  the extension widths (16, 16, 17, 17) and certificate sizes (120.2, 243.2,
  252.5 MB), the FE preprocessing times (about 2.7 s + 2.7 s), the
  large-artifact manifest (18 entries, CP-SAT encodings 137.68-388.11 MB),
  and the replication's identical summary and 1135/29 field comparison.

### Residual flaws found in v7 and fixed at the root in v8

1. **Wrong appendix input (critical).** v7 line 1291 still read
   `\input{companion-artifact-appendix-v5.tex}`: the v6 appendix (audit-tool
   paragraph, replication paragraph, dense-extension section, updated claim
   boundary) was never included in the compiled v7 document, although the v7
   body references exactly that material. v8 inputs appendix v7.
2. **Table 4 did not match the recorded artifact.** The five controlled-width
   baseline rows (0.395/0.678/0.005/0.003/0.006/0.621/0.129 etc.) match no
   deposited report: they came from an unrecorded session, while the
   manuscript claims "the artifact report contains the full per-instance
   data". v8's Table 4 now carries the medians recorded in
   `reports/external_baseline_sweep.json` (0.388/0.682/0.006/0.004/0.007/
   0.611/0.130 etc.), and the caption names the report. The peak-memory
   sentence changes from "about 101 MiB" to the recorded maximum 100.2 MiB.
3. **UNK/TMO marker semantics in the extension table.** The v7 caption
   defined UNK as "CP-SAT runs that returned UNKNOWN within their limit",
   but the recorded n=18 same run was killed by the ninety-second hard
   process cap (returncode -9, no output) and the n=18 split run returned
   UNKNOWN only after overshooting its soft sixty-second solver limit
   (73.1 s of solve time, 90.05 s wall). v8 relabels the n=18 same cell as
   TMO, redefines both markers truthfully, and discloses the two-tier limit
   (sixty-second hard kill for subprocess solvers; sixty-second solver limit
   plus ninety-second hard cap, with a thirty-second startup-and-construction
   grace, for the in-process CP-SAT/HiGHS runners and the bounded native
   runner) in the protocol paragraph of Subsection 13.1, in the Table 6
   caption, in the observations paragraph (replacing the unsupported claim
   that model construction consumes a substantial share of the budget), and
   in the appendix protocol paragraph.
4. **Replication comparison overstated as "every structural field
   identical".** `diff_reports.py` finds 29 mismatches: the 14 certificate
   file names, the 14 per-case provenance notes carried only by the recorded
   report, and the hardware block's memory figure (3.9 against 4.1 GiB). v8
   states all three classes and lists the fuller SHA-256 spot-check set
   (dense-8/16 same, ten-bar same, lattice C2 split, and the three completed
   dense-17/18 certificates).
5. **OOM unit slip.** "killed ... at about 3.75 GiB resident" mis-converts
   the kernel figure `anon-rss:3750608kB` (KiB): the anonymous resident set
   is 3.58 GiB = 3.84 GB. v8 quotes the kernel line and converts correctly
   (about 3.6 GiB).
6. **Unsourced distribution claim.** "Debian GNU/Linux 13" appears in no
   recorded artifact (the recorded protocol block lists glibc 2.41, kernel
   5.10.134, Python 3.12.14; the kernel string is an al8 build). v8 drops
   the distribution and reports exactly the recorded fields.
7. **Scope-only lattice width provenance.** Table 2 tabulated 17 and 23
   (treewidths, 6C-1) for the RELATION-TABLE-LIMIT rows, but the artifact's
   recorded width field for these cases is the influence-scope size (18 and
   24: every certified row's scope is the full actuator set, so the primal
   graph is complete). v8 keeps the treewidths and adds the caption
   clarification stating exactly what is recorded and what is implied.
8. **Two display-convention slips.** The chain-pretension row of Table 3 was
   labelled "0 (= full)" although both of its rungs certify and the caption's
   compression convention requires the range 0--full (now displayed so, with
   the rung coincidence explained); the chain n=8 row of Table 2 displayed a
   single 0.000 DP/verify pair although the recorded split values are 0.001
   (now shown as 0.000 / 0.001).
9. **The two pre-existing overfull hboxes** (the SPARSIFICATION-BATCH table
   cell and the Theorem 4.2 proof paragraph, carried since v5) are resolved
   by an explicit \allowbreak in the typewriter token, an \emergencystretch
   of 1em, and source formatting of the two-spring display; v8 compiles with
   zero overfull boxes and no new warnings, with all \ref/\cite keys resolved.

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. freeze a release manifest refresh at the next artifact release,
   incorporating the v2 replication and dense-extension outputs;
4. the implementation report v7's "about 101 MiB" peak-memory phrasing and
   the v9 extension table's "UNK 90.0 s" presentation remain as deposited
   historical documents; the v8 manuscript states the recorded values and
   the precise marker semantics, and report v10 records the divergence.


## v23: environment-provenance restoration and the Lean-availability statement

Context: the repository owner confirmed that claims of the form "verified, but
the sources did not persist" are factual and must not be deleted for lack of a
deposit; the loss of the sources is to be stated in an availability statement
instead. Two corrections follow, one per monograph.

### Changes to the companion manuscript (v9)

1. **Debian GNU/Linux 13 restored.** v8 had dropped the v7 platform claim
   ("Debian GNU/Linux 13 with kernel 5.10.134 and glibc 2.41") because the
   artifact's machine-recorded protocol block carries only the glibc version
   (field `os`), the kernel string, RAM, cores, CPU, and harness Python -- no
   distribution name. That drop was a mis-correction: the platform is an
   operator-side environment fact, true but not machine-captured. v9 restores
   the full platform sentence and adds an explicit provenance split: the
   protocol block machine-records the processor, core count, memory, kernel
   version, glibc version, and harness Python; the distribution name, Debian
   GNU/Linux 13, is stated from the operator's environment record rather than
   machine-captured, and is consistent with the recorded glibc 2.41 userland.
   The v8 parenthetical "(the recorded protocol block of the artifact reports
   exactly these fields)" is withdrawn in favour of this split.
2. Nothing else changes relative to v8. v9 compiles with exactly v8's warning
   profile (zero overfull boxes; the fifteen underfull warnings are unchanged,
   pre-existing at lines 223/227/229); appendix v7 is unchanged and still
   input at the same place in the document.

### Changes to the main monograph (v42)

Owner directive: the Lean formalisation was executed and its checks passed;
its sources did not persist. The claims stay; the loss is disclosed.

1. **Artifact availability paragraph** added to the Formal verification
   section: the twenty-four core Lean files, `theorem_D_tri.lean`, the
   `research/mathlib/k_game.lean` project, the twelve deterministic Python
   experiments, and the recorded Lean 4.33.0 / Python 3.13 environment did not
   persist and are not part of the repository deposit; the gate was executed
   and its checks passed, so the listed formal statements are machine-checked,
   but the verifying sources are not available for independent re-execution or
   audit; the reproduction entry point available in the present repository is
   the companion artifact's `make reproduce` gate (the finite-ECD prototype,
   harness Python 3.12.14), a separate artifact that does not re-run the Lean
   checks; the proofs in the text are self-contained. All v41 Lean claims are
   retained verbatim; in particular "Python 3.13" (the formal-gate
   environment) is no longer treated as conflicting with the companion's
   recorded 3.12.14 -- they are different artifacts in different environments,
   and the availability paragraph says so explicitly.
2. **Citation policy completed.** The introduction promises "cites, rather
   than reproves" for Hoeffding concentration, Konig's lemma, and standard
   finite CSP complexity classifications; v41 invoked all of these uncited.
   v42 adds: Hoeffding's inequality cites Hoeffding 1963; Konig's lemma cites
   Konig 1927 (and Simpson 2009 at the Weak-Konig/RCA_0 reverse-mathematics
   usage); the 3SAT hardness reduction cites Karp 1972; the
   distinct-variables 3SAT variant cites Tovey 1984; the parsimonious #3SAT
   reduction cites Valiant 1979. Six bibitems added (28 total); every bibitem
   is cited and every cite key resolves.
3. **All eleven floats are now referenced in the text.** v41 had seven
   unreferenced floats: tab:notation, tab:compression-signature,
   fig:diagnostic-flow, tab:bell-repair, tab:weihrauch-classification,
   fig:cut-poset-linearisation, tab:source-domain-status. Each gained a
   natural anchor sentence in the remark, definition, or paragraph it
   illustrates (e.g. the degree-theoretic-contribution remark now says
   "Table~ref{tab:weihrauch-classification} separates ..." instead of "The
   table separates ...").
4. **Companion naming unified and pinned.** "companion finite monograph" and
   "companion programme" are replaced by "companion algorithmic monograph" /
   "companion algorithmic programme"; the first document mention now pins
   "version 8, with its artifact appendix, version 7".
5. **prop:nonembedded (External-policy special case) restated** so that the
   identification of the bounded realised policy class with the external class
   is explicitly definitional (the defining-image equality) rather than a
   derived conditional; the proof now argues only the substantive reduction.
6. v42 compiles with tectonic (exit 0) with exactly v41's warning profile
   (27 overfull and 172 underfull warnings, all pre-existing) and zero
   undefined references or citations.

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. if the Lean and Mathlib sources are ever recovered, deposit them with
   checksums and gate records and shorten the availability paragraph
   accordingly;
4. the main monograph's companion version pin (v8 / appendix v7) must be
   re-checked whenever the companion is bumped again.

## v24: pedagogical, game-theoretic, and visual enhancements

Context: the owner asked whether the two monographs merit additional
non-decorative pedagogical or expository enhancements (including physical
and game-theoretic insight), additional non-decorative tables or figures,
or supplements and delegation. The assessment round concluded that most
candidate additions would violate the books' own anti-decorative
discipline, and identified six genuine gaps, implemented here in the
agreed order: (A) a hand-verifiable dynamic-program example, (D) a
structural figure for the benchmark families, (B) a
certificates-as-verifier-games remark, (C) a physical reading of the
two-spring demonstrator, (F) a ladder-outcome table, and (E) commutative
diagrams for the functorial chapter. No material was delegated out of
either monograph: the two-book split is already the delegation device,
the companion's Appendix A is already a de-facto reproducibility
supplement, and the main monograph earns its self-containedness.

### Changes to the companion manuscript (v10)

1. **Example 6.4 (A): a hand-verifiable dynamic program.** Section 6
   previously contained no numeric instance: the private-variables lemma,
   the recurrence-correctness lemma, and DP certificate soundness were all
   purely abstract, and the two-spring demonstrator exercises the
   pipeline but not the dynamic program. New Example `ex:dp-micro` works a
   four-variable, three-factor path instance end to end: bags
   B1={x1,x2}, B2={x2,x3}, B3={x3,x4} rooted at B3, factor-to-bag
   assignment, the charging rule (x2 charged at B2, the bag closest to the
   root), both message tables entry by entry (nu_1 = (1,0), nu_2 = (1,1)),
   the root value 2, witness backtracking to the optimal sections
   (1,0,0,1) and (0,1,1,0), a brute-force cross-check over all sixteen
   assignments, the TREE-DECOMP + DP-OPTIMUM certificate reading, a
   refutation variant (R1', R2', R3') whose message tables
   (nu_1' = (0,infinity), nu_2' = (infinity,0), infeasible root)
   constitute a DP-REFUTATION certificate, and the weighted-width count
   lambda(T) = 2. All arithmetic was machine-verified by brute force
   before insertion, and the example is explicitly scoped as a
   pedagogical check, not a recorded artifact run.
2. **Figure 1 (D): structural schematic of the demonstrator and the four
   benchmark families.** The family table described all four structures
   verbally. New five-panel TikZ figure `fig:mechanics-families`, drawn
   after the artifact's model generators (mechanics_gen.py), shows
   (a) the two-spring demonstrator with the displaced position dashed,
   (b) the six-node ten-bar cantilever with 3x4 bays, 3-4-5 diagonals,
   four vertical node-force actuators, and the quantized tip load,
   (c) the pretension chain with self-equilibrated pairs, (d) the dense
   chain with alternating stiffnesses 1 and 2 and the monitored
   mid-chain displacement, and (e) the cross-braced lattice with two
   bay-rows, C columns, and free-edge corner loads. The caption
   disambiguates the family table's "3x4 bays" (bay dimensions 3 by 4,
   two bays) and "two-row" (two bay-rows, three node-rows, consistent
   with the 6C-1 width formula). The figure is referenced from both
   Section 10 (physical reading) and Section 11 (family paragraph).
3. **Physical reading of the two-spring demonstrator (C).** New paragraph
   in Section 10 mirroring the foundational monograph's Bell reading: the
   obstruction has an operational face as a repair (sensor acquisition);
   a controller commanded without load sensing must be admissible for
   every indistinguishable load; the refutation certifies insufficiency
   of the information structure, not structural unsafety; the repairing
   sensor is an instrumentation decision with a certified justification,
   exhibited at structural scale by the ten-bar repair certificate.
4. **Table `tab:ladder-outcomes` (F): certificate-bearing outcomes of the
   sparsification ladder.** New table in Section 9 recording the three
   terminal configurations at a fixed retained profile (inner
   satisfiable / outer unsatisfiable / inconclusive bracket) with their
   supporting certificates and transported claims, the refinement
   stability of the two certification rows (only an inconclusive pair
   can move under refinement), and, as a new theorem-level corollary, the
   certified cost bracket
   min_{Gamma^+_J} kappa <= min_{Gamma^true} kappa <= min_{Gamma^-_J}
   kappa with min(empty) = infinity, each side certified by a
   DP-OPTIMUM run on the corresponding sparse instance. The recorded
   study classifies brackets and does not tabulate cost bounds; the
   table's caption also records the study's direct re-verification of
   inner policies against full certified rows.
5. Preamble: tikz with the coil, patterns, arrows.meta, and positioning
   libraries (loaded before hyperref) and a definition-style example
   environment sharing the theorem counter; the example is the last
   numbered item of Section 6, so no existing theorem number moves.
   Appendix v7 is unchanged and still input at the same place. v10
   compiles with zero errors, zero overfull boxes, and v9's underfull
   sites unchanged plus one new site of the same pre-existing class as
   the grammar table's (the lone-token line break of
   SPARSIFICATION-BATCH in a p-column). All references resolve; the
   example, table, and figure pages were visually verified.

### Changes to the main monograph (v43)

1. **Remark 12.59 (B): certificates as verifier-game strategies.** New
   remark in the finite-algorithmic handoff welding Theorem 12.40
   (finite verifier-game representation) to Proposition 12.58 (finite
   certificate conservativity): a verified policy certificate is exactly
   a winning pure strategy in the tabular verifier game (verification is
   play acceptance; the checked factorwise tests are the verifier's
   accepting worlds); a verified refutation records that no pure
   strategy wins; "inconclusive" is the absence of a game-outcome
   certificate, not a third outcome; and an unfinished play decides
   nothing, which is why a bare solver timeout supplies no ECD
   classification. This is the only game-theoretic enhancement that
   respects the monograph's own fencing of further game theory to a
   separate source doctrine (the Kuhn/imperfect-recall boundary remark
   and the dependency ledger).
2. **Commutative diagrams (E).** The functorial chapter previously had
   no commutative diagrams at all (the monograph's four figures are
   array-based schematics). Two additions: the naturality square of
   alpha : A^P => A^Q o F unpacked after the base-isomorphism
   definition (Section 12.2), and the retraction square plus idempotence
   triangle for Gamma o Term = Id and ExtComp^2 = ExtComp after the
   terminal-retraction theorem (Section 12.4), with the triangle's
   bottom edge glossed as the identity on the compressed image per the
   theorem's typed identity. tikzcd is added to the preamble before
   hyperref.
3. **Companion version pin re-checked** (remaining item 4 of the v23
   section): the pin now reads "version 10, with its artifact appendix,
   version 7".
4. v43 compiles with exactly v42's warning profile: the same nine
   overfull lines at their shifted positions (offsets +2, +13, +35, +53
   exactly match the inserted line counts), zero errors, zero undefined
   references or citations; the two diagram pages and the remark page
   were visually verified.

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. if the Lean and Mathlib sources are ever recovered, deposit them with
   checksums and gate records and shorten the availability paragraph
   accordingly;
4. the main monograph's companion version pin (now v10 / appendix v7)
   must be re-checked whenever the companion is bumped again;
5. if a zero-underfull profile is ever required for the companion, the
   ladder table's middle column can be reworded to avoid the lone-token
   SPARSIFICATION-BATCH line break; the same cosmetic warning class
   already exists in the Section 3 grammar table.

## Round 7 section (plan v25) — four-part owner audit (remnants/redundancy, clarity/flow, structure/causal coherence, intent) and its implementation (companion v11 / appendix v8 / main v44)

### Audit basis

Five parallel line-level scans (main remnants; companion+appendix remnants;
main clarity/flow; companion clarity/flow; cross-book alignment), all
spot-verified. Verdicts: main v43 remnant-clean with three moderate items;
companion v10 remnant-clean with one major-severity item (the §13↔Appendix A
duplication cluster); notation character-identical across the pair; every
main claim about the companion verified; ladder and cost bracket consistent.
The withdrawn-accounting footnote of §13.2 was separately re-reviewed against
the v4-tag artifact source (cpsat_runner.py maps UNKNOWN→INCONCLUSIVE by
construction; mechanics_baseline_sweep.py gates status_agreement_with_native
on classification): all four forensic claims check out; the withdrawal itself
is proper; two micro-edits applied (labelled the 32/4/66 triple; dropped the
temporal "now" from the agreement-counter sentence).

### Changes to the companion monograph (v11)

1. **§13↔Appendix A consolidation (the round's one major-severity fix).**
   §13.1 is now the single documentation site for the environment, solver
   versions (kissat's gcc detail absorbed there), and protocol. The §13.2
   replication paragraph's version list collapses to a back-pointer; the
   dense-extension archive policy in §13 keeps the availability guarantees
   (checksums, regenerability) and delegates the mechanics to Appendix A;
   Appendix A.2–A.4 now uses \ref-based back-pointers (value-cost remark,
   status-discipline remark, mechanics front end, benchmark convention,
   external-baseline configuration) instead of restating content; the
   intra-appendix cross-check restatement and the version-exact provenance
   list were removed for the same reason; "new subsection" → "the subsection
   below"; the phase-4 vocabulary is glossed at first use in each file.
2. **§1 inventory fixes.** The contributions list gains the sensor-repair
   theorem (hitting-set characterization on inclusion-minimal cores) as the
   new Fifth item with renumbering; the roadmap sentence gains the one-shot
   fibre and sensor-repair layer; the foundational monograph is version-pinned
   (version 44).
3. **§9 clarity.** Purpose-first opening (interval uncertainty traded for
   width; monotone and certifiable refinement); Γ^true is bound in the Write
   sentence as Γ(P^true) of the true, unsparsified instance; the
   numeric-domains qualifier moved next to the η display.
4. **Notation micro-pass.** Definition 2.2 names the scenario set W and the
   map obs:W→O; Definition 2.3 introduces O_j at the evaluation map; §4 opens
   with the FIBRE-CONFLICT occasion and the o=obs alias; Example 6.4's ad-hoc
   κ_1 symbol is dropped; the §13.2.1 post-table opener no longer repeats
   the no-superiority sentence verbatim; Figure 1(a) is named the two-spring
   arrangement.
5. **Signposting.** §10's opening bridges the §9→§10 seam (the demonstrator
   assembles the earlier layers; the ladder is exercised by the study);
   §10's corrupted-rejection claim points at the §13 gate records; §11's
   second ten-bar mention is an explicit back-reference; §12's classification
   cites Table 1 and glosses the zero-extension convention; the verification
   gate table is captioned (Table 5) with the Remark 3.1 status pointer;
   Table 8 is now referenced from the extension prose; §13's opening points
   to Appendix A; the repository URL
   (https://github.com/MIKEAA2020/halting-physics) is inserted in the
   archival paragraph.
6. The withdrawn-accounting footnote's 32/4/66 triple is spelled out
   (32 cross-checked unsatisfiable answers, 4 inconclusive runs, 66
   agreements) and "is now gated" loses the temporal "now".

### Changes to the artifact appendix (v8)

Consolidation back-pointers as above; nothing else. The appendix's
operational content (schemas, runner scripts, env vars, reproduction
commands, dense-extension drivers, claim boundary) is unchanged.

### Changes to the main monograph (v44)

1. **Bracketing (the round's headline structural fix).** The introduction's
   roadmap gains a fourth stage (the morphism tier: morphism levels, terminal
   compression as idempotent functor, groupoid equivalence, composition laws,
   verifier games, the topological-order development principle, and the
   delegation to the companion) and a clause completing the static-local
   tier's announcement; "The paper proceeds in three stages" becomes "The
   monograph proceeds in four stages"; the Monograph-scope paragraph
   discloses the companion delegation up front; the Conclusion gains a final
   paragraph recording the morphism tier, the verifier-game reading, the
   topological-order development principle, and the handoff with the version
   pin.
2. **The orphan patch-category paragraph** (the only unparseable passage in
   the Γ-definitional heart) is relocated verbatim from before Definition 5.5
   to after the full patch-site collapse corollary, where "this presentation"
   resolves.
3. **§11 subdivision.** The 620-line monolithic subsection is divided into
   seven (Imperfect-information arenas and behavioural coordinates;
   Information refinement and recall; One-shot team arenas and blind-order
   normal forms; World schedules; Distributed compilation of finite arenas;
   One-shot Bell realisation; Explicit-table complexity boundary), and the
   three \paragraph units of the operational-feedback subsection are
   promoted to subsections (World-only decoupling; Observation-preserving
   compilation; Trace-relative past factorisation). §11 now has fourteen TOC
   entries; no theorem numbers move (the counter is per-section); the
   subsec:oneshot label travels with the one-shot content.
4. **§12.13 orientation sentence** stating the certificate↔game bridge role
   at the theorem's point of statement.
5. **Cross-book alignment.** The abstract's "companion morphism theory"
   becomes "accompanying morphism theory" (removing the polysemy with the
   companion book); the inner–outer handoff proposition records that the
   companion proves its mechanics front-end instance; the companion pin is
   bumped to version 11 / appendix 8; the availability paragraph inserts the
   repository URL.
6. **Precision micro-pass.** DNR/PA expanded at first use in abstract and
   introduction; CHSH expanded at first use; the PR box is expanded and
   anchored by a new Popescu–Rohrlich bibitem; def:realise states the
   represented-realisation scope clause; def:morphism-levels cites the §6
   definitions it specializes; the global-family functor proof cites
   Proposition 6.x instead of re-running the naturality computation; the
   CHSH paragraph's recollections are compressed to a pointer after
   cor:team-decision; the def:epsEC trailing commentary moves into the
   success-set remark; a display punctuation error is fixed; the variance
   recollection in the nested-prefix remark is trimmed; forward references
   are marked "below"; rem:ladder gains the tab:presentations anchor and §6
   a closing word; "paper/article" lexicon unified to "monograph" (five
   sites); -ize/-ise and French-spacing strays normalized; blank-line runs
   collapsed.

### Verification

Both books compile with tectonic: main v44 with exactly v43's warning profile
(the same nine overfull lines at shifted positions and the same 172 underfull
lines; zero errors, zero undefined references or citations, including the new
popescu bibitem) and companion v11 with v10's underfull set (the grammar-table
class) and zero overfull boxes after URL allow-breaking; the gate table
renders as Table 5 with its Remark 3.1 pointer; the TOC shows §11's fourteen
subsections; all new cross-references resolve in both PDFs.

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. if the Lean and Mathlib sources are ever recovered, deposit them with
   checksums and gate records and shorten the availability paragraph
   accordingly;
4. the version pins are now mutual (main v44 pins companion v11/appendix v8;
   companion v11 pins main v44) and must be re-checked together whenever
   either book is bumped;
5. the zero-underfull profile remains declined (v25 records the same
   cosmetic warning class as v24: the grammar-table and ladder-table
   lone-token line breaks);
6. round-8 incorporation candidates not yet executed (finite effective
   collapse proposition; relation-to-prior-work passage with
   decentralized-control/sensor-selection citations; observation
   identification width warning; sensor-design hardness and FPT framings,
   gated on writing complete reductions; claim-boundary anchor bibitems) —
   these remain owner decisions, separate from the present structural pass.

## Round 8 section (plan v26) — Round-8 candidate adjudication, plan-v25 remainders, withdrawn-footnote re-verification, and the register scan (companion v12 / appendix v9 / main v45)

### Basis

Owner directives: (1) include Round-8 incorporation candidates only if
highly merited; (2) address remaining points from plan v25 at root cause;
(3) address the withdrawn footnote if there is still defect; (4) scan for
meta-commentary, informal chat jargon, self-referential or editorial
comments, over-hedging, and internal jargon. Two register scans were run
(main v44; companion v11 + appendix v8) by independent agents; every
reported defect and defensible borderline was verified in context before
editing. Krause–Guestrin (AAAI 2007) and Witsenhausen (SIAM J. Control 9(2),
1971) bibliographic details were verified by web search before insertion.

### Round-8 candidate adjudication (six ranked candidates from the round-8 source-draft mining)

1. **Finite effective collapse proposition — INCLUDED (companion §2).** The
   draft's Proposition 1 (Γ_set = Γ_eff for finite explicitly encoded
   presentations under unrestricted lookup-table catalogues) was absent from
   both books and closes a conceptual gap at the exact sentence that states
   the finite tier hierarchy: under unrestricted catalogues the
   set-theoretic and effective questions are one question, and only the
   declared-catalogue and budget separations remain. Inserted as
   Proposition (Finite effective collapse) with a two-line proof and a
   remark (What the collapse separates) tying it to the status discipline
   (a timeout or table-size limit is inconclusive, not evidence of
   non-existence) and to the bounded-class convention.
2. **Relation-to-prior-work passage — INCLUDED (companion §1, new
   subsection "Relation to prior work"; main §1, one new paragraph in
   "Relation to established frameworks").** The companion had no prior-work
   prose at all despite the submission assessment listing the literature
   comparison as one of three essentials. The companion passage assembles
   the six lines the article actually builds on (Yannakakis join processing;
   Freuder/Dechter/Bodlaender–Koster width and consistency; certifying
   algorithms; parameterised complexity and ETH; the
   Witsenhausen/Papadimitriou–Tsitsiklis/Bernstein et al. decentralised-
   control information-structure tradition; Krause–Guestrin sensor selection
   and George/Lipton–Tarjan nested dissection) and states the honest
   novelty boundary: none of these lines supplies the assembly (typed
   certificates, hitting-set repair, exact-arithmetic rows, verified
   brackets, the status discipline); the engines are classical. Seven new
   companion bibitems (bernstein02, freuder82, george73, krauseguestrin07,
   liptontarjan79, papadimitrioutsitsiklis86, witsenhausen71), all cited;
   the bibliography label widens to {24}. The main gains the missing
   decentralised-control lineage in its relation subsection (three new
   bibitems, all cited), pointing at the distributed-selector tier and the
   one-shot team arenas as the presentation-relative treatment of the same
   source problems.
3. **Observation-identification width warning — INCLUDED (companion §5,
   after the complexity-boundary section).** The draft's Proposition 5
   (matching → arbitrary quotient) was only instantiated empirically
   (dense-chain same width n−1; lattice complete primal graph). Inserted as
   Proposition (Identification can destroy low width) with the primal-graph
   definition at first use (previously used undefined at §6), a two-line
   construction proof, and a remark (Width is measured after identification)
   that gives the general form of the same/split convention, the
   graph-colouring instantiation of the hardness clause (citing
   gareyjohnson79), and the discipline sentence (neither low mesh width nor
   low width of separate scenario copies is sufficient). §11's same/split
   definition gains the cross-reference; the minimum-fill heuristic sentence
   gains the George/Lipton–Tarjan citation (previously an uncited lineage).
4. **Sensor-design hardness proposition — DECLINED.** Requires writing a
   complete reduction (new research, not inclusion); the books' claim
   discipline forbids stating gated claims without complete proofs.
5. **FPT / parameterised framing — DECLINED.** Same gating: the W[1]/ETH
   statements need complete reductions with exact source hypotheses; the
   companion's §5 already cites the parameterised sources with their exact
   hypotheses and declines to restate them as universal classifications.
6. **Claim-boundary anchor bibitems — DECLINED.** The Ainsworth–Oden /
   Moore / Tabuada anchors would decorate declined-scope statements rather
   than anchor load-bearing claims; the George/Lipton–Tarjan and Freuder
   anchors were absorbed into candidate 2/3 where they are load-bearing.

### Plan-v25 remaining items, addressed at root cause

- Items 1–3 (archival DOI at publication time; continuum-mechanics
  validation outside scope; conditional Lean-source recovery): external or
  conditional, correctly not actionable now; unchanged.
- Item 4 (mutual version pins re-checked together on every bump): honored —
  companion v12 pins main v45; main v45 pins companion v12 and appendix v9;
  companion v12 \inputs appendix v9; all three bumped consistently.
- Item 5 (zero-underfull profile): remains declined; v12 has exactly v11's
  five-warning underfull class at shifted positions and v45 exactly v44's
  nine-overfull profile at shifted positions; no new warnings of either
  class were introduced.
- Item 6: the incorporation candidates — resolved as above.

### Withdrawn-footnote re-verification (owner directive 3)

The §13.2 withdrawn-accounting footnote was re-read in v11 line-level: the
counters remain internally consistent (34 + 33 + 3 = 70 runs; 67
status-bearing; the withdrawn v6 triple 32/4/66 is itself internally
consistent); the CP-SAT 49.5 s UNSAT datum matches Table 6; both micro-edits
of the round-10 review are in place (the 32/4/66 triple is labeled; the
temporal "now" is absent from the gating sentence); the replication
cross-reference resolves; and "An earlier version of this article" matches
the companion's uniform self-reference lexicon ("this article", five body
sites + six appendix sites; the foundational monograph uses "monograph").
Verdict: **no remaining defect**; the passage stands as proper scholarly
documentation of the withdrawal.

### Register scan (owner directive 4) — findings and disposition

Main v45 fixes (from the v44 scan): two -ize strays introduced by the v44
insertion pass itself (realization/realizes → realisation/realises); the
"companion algorithmic programme" polysemy in the §12 closing remark →
"accompanying" (completing the fix the same pass made in the abstract); WKL
expanded at first use in both abstract and §1; CSP parenthesised at first
use; MILP expanded at its sole use; "normalized" → "normalised"; the sole
temporal "now" dropped from the §4 opening; "The common lesson" → "The
common content of these results" in the Conclusion.

Companion v12 fixes: the unglossed "Phase-6" gate row gains its gloss at the
preamble (phase 6 = the recorded mechanics comparative-scaling study,
verified against the artifact README and mechanics_baseline_sweep.py);
"ETH lower bounds" expanded at first use; "FE preprocessing" expanded;
"system OOM killer" → "kernel out-of-memory (OOM) killer"; "this release" →
"the artifact release"; the two pre-introduction uses of "the artifact
report" (§11 gate caption, §12 ladder caption) → "the artifact's recorded
reports"; the DP-OPTIMUM forward use now cites both the grammar section and
the width-DP section; seven -ize strays normalised (specialise, organised,
parameterised ×2, synthesising, realise, optimisation) and five "quantized"
→ "quantised"; the sole unspaced em-dash pair spaced.

Appendix v9 fixes: the positional self-reference "the subsection below" is
replaced by a labelled cross-reference (the dense-family subsection gains
\label{subsec:dense-extension}); the appendix is otherwise unchanged.

Scan false positive, verified and retained: the appendix's
\texttt{VERIFIED-SAT}/\texttt{VERIFIED-UNSAT} tokens are genuine recorded
artifact field values (repro_report.json records both), not invented
status tokens; they are correctly documented in the artifact-format
appendix and de-tokenising them would misdescribe the artifact.

### Verification

Both books compile with tectonic: main v45 with exactly v44's nine-overfull
profile at positions shifted by the insertion (identical badness values;
zero errors, zero undefined references or citations, including the three new
bibitems); companion v12 with exactly v11's five-warning underfull class at
shifted positions (zero overfull, zero errors, zero undefined references,
including the seven new bibitems and the appendix-v9 label). pdftotext
confirms all insertions render: the Relation-to-prior-work subsection, both
new propositions and remarks, the same/split cross-reference, the phase-6
gloss, the FE/OOM expansions, both caption rewrites, both version pins
(version 12 / version 9), the distributed-side paragraph, the WKL/CSP/MILP
expansions, and every new bibitem. Mechanical checks: 47 labels / 24
bibitems (companion + appendix, all cited, no duplicates); 302 labels / 32
bibitems (main, all cited, no duplicates).

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. if the Lean and Mathlib sources are ever recovered, deposit them with
   checksums and gate records and shorten the availability paragraph
   accordingly;
4. the version pins are mutual (main v45 pins companion v12/appendix v9;
   companion v12 pins main v45) and must be re-checked together whenever
   either book is bumped;
5. the zero-underfull profile remains declined (the grammar-table and
   ladder-table lone-token line-break class);
6. the sensor-design hardness and FPT/parameterised framings remain gated on
   writing complete reductions; the claim-boundary anchor bibitems remain
   declined as decoration.

## Round 9 section (plan v27) — sensor-design hardness and FPT framing: research, placement decision, and implementation (companion v13 / main v46)

### Basis

Owner directive: do new research for sensor-design hardness and the
FPT (fixed-parameter tractability) framing if merited, and decide whether
the material belongs in a separate monograph, a supplementary document, or
the same book. This was the item plan v26 left gated ("the sensor-design
hardness and FPT/parameterised framings remain gated on writing complete
reductions"), and the gate is the round's subject: the reductions now
exist and are complete.

### Research performed

Literature. Three search passes confirmed the external anchors: set cover
is W[2]-complete under the standard parameterisation by the number of
chosen sets (the parameter-preserving reduction from dominating set; the
parameterised-complexity source is already bibliography item
downey-fellows99); constraint satisfaction over bounded-treewidth primal
graphs is the classical fixed-parameter tractability lineage the companion
already cites (freuder82, arnborg-proskurowski89, bodlaender-koster08,
dechter03); and the sensor-placement hardness literature (constrained
placement for LTI observability, filtering-based selection, MOMDP sensor
budgeting) lives in formalisms disjoint from the companion's finite
one-shot model, so no imported result states the companion's own problem.
The companion's own problem therefore needs its own reduction, which is
what the round supplies. No new bibliography items are required: the two
sources the proofs use (karp72, downey-fellows99) are already cited.

Mathematical work. The complete reduction: given a set-cover instance
(universe U, covering sets X_1,...,X_n, budget k), take W = {w_0} ∪
{w_j : j ∈ U} with a single observation value, A = {0,1}, S_{w_0} = {0},
S_{w_j} = {1}, and one candidate sensor per covering set, s_i(w_0) = 0,
s_i(w_j) = 1 for j ∈ X_i and 0 otherwise. The inclusion-minimal conflict
cores are exactly the pairs {w_0, w_j} (every conflict contains w_0 and
some w_j; both singletons are conflict-free), and s_i separates w_0 from
w_j exactly for j ∈ X_i, so by the one-shot repair theorem the repairing
subfamilies of size at most k are exactly the covers of size at most k.
The budget parameter is preserved, so W[2]-hardness transfers. Membership
in NP holds via the witness (chosen subfamily, refined selector table),
checked by a linear scan. Scoping was checked both directions: the
hardness is stated for a listed candidate family, because unrestricted
sensor synthesis allows a single all-separating sensor on this
construction (one sensor repairs every pair core at once), so hardness
does not transfer to the unrestricted formulation; that formulation is
recorded as an explicit unclassified boundary.

### Merit adjudication

Sensor-design hardness: merited. Theorem 7.1 already characterises repair
as a hitting-set condition and the section already closes with "the second
task contains hitting-set structure even when the first task is easy"; the
proposition converts that structural observation into a precise complexity
boundary with a complete, verifier-format reduction, exactly the
discipline the complexity section demands (direct reduction, exact source
hypotheses, no classification transfer).

FPT framing: merited, as a remark rather than a theorem. The book already
proves the bound poly(|I|,|T|)·2^{λ(T)}; the remark names its
parameterised reading (fixed-parameter tractability in the weighted width
for the input consisting of the instance with its declared decomposition)
and pairs it with the new design-side W[2]-hardness, yielding the
evaluation/design asymmetry: certification is fixed-parameter tractable in
width, design is W[2]-hard in its own budget already at width zero. This
is the complexity-theoretic content of the guiding rule and it closes the
gap between the introduction's promise ("parameterised complexity
calibrates what width-bounded computation cannot achieve") and the book's
actual statements.

### Placement decision

Same book: the companion. Reasons: (1) the established content is small
(one proposition with proof, one remark, one table row, one appendix
reduction, and four local prose integrations — 84 added lines across eight
sites) and completes statements the companion already makes; (2) it
requires no apparatus beyond Theorem 7.1 and two already-cited sources;
(3) a separate monograph or a supplementary document would be justified
only by a research programme — bicriteria width-and-repair design,
approximation guarantees, ETH-tight bounds for repair, parameterised
design beyond the solution budget — none of which is established; these
are recorded as open boundaries in the limitations section, consistent
with the existing claim discipline. The foundational monograph is
untouched except for the mutual version pin (it states no companion-side
complexity, so nothing in it becomes stale); main v46 is a one-line pin
bump to companion v13, with appendix v9 unchanged and still pinned.

### Implementation (companion v13, 1,933 lines; main v46, 7,700 lines)

Companion v13, eight sites: (1) §1 contribution Fifth gains the hardness
clause; (2) the §5 complexity table gains the row "Minimum-cardinality
sensor repair (listed candidates) — NP-complete"; (3) §5 prose after the
source-hypotheses sentence states the design-side result as established
directly rather than transferred, with the Proposition 7.3 / Appendix B
pointers; (4) §6 gains Remark 6.4 (A fixed-parameter reading) after the
DP-soundness proposition, cross-linked both directions with §7; (5) §7
gains Proposition 7.3 (Sensor-design hardness) with proof after the
two-task paragraph; the proof carries the width-zero clause (single
observation value, unary factors, edgeless primal graph) and the pointer
to Remark 6.4; (6) §13's frontier sentence gains the parenthetical
acknowledgement that the W[2]-hardness of sensor repair is the one
design-side reduction the article records, a single problem rather than a
layer; (7) Appendix B "Hard rows" gains the full set-cover construction
with the pair-core analysis, the W[2] transfer under the standard
parameterisation, the NP membership witness, and the unrestricted-formulation
boundary clause; (8) the foundational pin is bumped to version 46.

Main v46: the companion pin in the closing delegation passage is bumped
from version 12 to version 13 (appendix pin unchanged at version 9). No
other edit; the foundational monograph contains no statement affected by
the companion's new boundary.

### Verification

Tectonic: companion v13 compiles with exactly v12's six-warning underfull
class at positions shifted by the two-line contribution edit (identical
badness values: 3815, 3601, 2762, 10000, 10000, 10000), zero overfull,
zero errors, zero undefined references or citations. Main v46 compiles
with exactly v45's warning profile: the same nine unique overfull warnings
and the same fifty-five unique underfull warnings at identical positions
and badness values (the pin edit sits below every warned paragraph),
zero errors, zero undefined references. pdftotext confirms every
insertion renders: the contribution clause, the table row, the §5 prose
with its Proposition 7.3 and Appendix B references, the full Remark 6.4
text, the full Proposition 7.3 statement and proof (pair-core analysis,
budget preservation, width-zero clause, Remark 6.4 pointer), the §13
parenthetical, the complete Appendix B reduction paragraph including the
unrestricted-synthesis boundary, and both version pins (companion pinning
main v46; main pinning companion v13). Mechanical checks: 49 labels
(47 prior + the two new), zero duplicates, all references resolve, 24
bibliography items all cited, no citation without a bibliography item,
and no new bibliography items.

### Remaining items

1. assign and insert the archival DOI at publication time (unchanged);
2. continuum-mechanics validation and discretisation-error certification
   remain outside the artifact scope (unchanged claim boundary);
3. if the Lean and Mathlib sources are ever recovered, deposit them with
   checksums and gate records and shorten the availability paragraph
   accordingly;
4. the version pins are mutual (main v46 pins companion v13/appendix v9;
   companion v13 pins main v46) and must be re-checked together whenever
   either book is bumped;
5. the zero-underfull profile remains declined (the same cosmetic
   lone-token warning class as v25/v26);
6. unrestricted sensor synthesis (sensors not drawn from a declared
   candidate list) remains unclassified, as does any ETH-tight or
   approximation-classification statement for repair, and the bicriteria
   width-and-repair design problem remains unposed beyond the asymmetry
   remark; these are the natural next research targets if a future round
   reopens the design-side programme;
7. the claim-boundary anchor bibitems remain declined as decoration.
