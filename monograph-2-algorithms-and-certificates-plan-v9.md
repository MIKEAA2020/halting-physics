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
