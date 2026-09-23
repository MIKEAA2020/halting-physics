# Second monograph plan: Algorithms and Certificates for Finite Effective Causal Descent

## Working title

Algorithms and Certificates for Finite Effective Causal Descent: Width, Counting, Compression, and Source Integration

## Motivation

The first monograph develops the section-theoretic, diagnostic, functorial, computability, Bell, and causal foundations of effective causal descent. A second monograph can pursue the algorithmic programme needed for a JACM-style contribution: tractability boundaries, width parameters, counting, certificate extraction, and applications to finite source integration and database-style repair.

The goal is not to repackage known CSP and database algorithms. The goal is to show how the ECD presentation data determine which algorithms and certificates are preserved under translations, compression, hiding, and composition.

## Central thesis

Finite ECD presentations admit an algorithmic theory whose complexity depends on the interaction between:

1. local relation representation;
2. incidence width;
3. algebraic or convex structure;
4. certificate language;
5. implementation and resource filters;
6. presentation-changing operations such as terminal compression, hiding, and coarse-graining.

The main output should be a structural algorithmic classification of finite presentations and their certificates.

## Core theorem package

### 1. Finite ECD algorithmic meta-theorem

Develop a theorem collecting the following regimes for explicit finite presentations:

- general finite distributed capability is NP-complete;
- exact counting of compatible families is \(\#\mathrm P\)-complete;
- acyclic/join-tree presentations are solvable in polynomial time;
- bounded-treewidth or bounded-hypertree-width presentations are fixed-parameter tractable;
- affine finite-field presentations are decidable in polynomial time by Gaussian elimination;
- rational convex/distributional presentations are decidable by linear programming;
- bijective-network presentations are decidable by holonomy fixed-point computation.

### 2. Width-sensitive algorithms

Define width measures for ECD incidence diagrams:

- primal graph treewidth;
- incidence graph treewidth;
- hypertree width;
- fractional hypertree width;
- join-tree acyclicity.

Prove dynamic-programming algorithms for bounded-width presentations and identify which diagnostic levels can be decided in time polynomial for fixed width.

### 3. Certificate extraction

For each tractable class, give an explicit certificate extraction theorem:

- finite local emptiness certificates;
- join-tree witnesses or semijoin reductions;
- affine inconsistency vectors;
- holonomy loops with empty common fixed-point set;
- Farkas dual certificates for rational convex presentations;
- bounded-width unsatisfiable cores.

### 4. Counting and enumeration

Develop the counting side:

- \(\#\mathrm P\)-completeness in general;
- polynomial-time counting on acyclic joins under suitable representation assumptions;
- FPT counting under bounded width;
- delay bounds for enumerating compatible families;
- approximate counting or sampling for selected convex/distributional subclasses.

### 5. Compression and certificate loss

Study the algorithmic effect of terminal compression and other repackagings:

- terminal compression preserves existence but can destroy local certificate structure;
- compression can reduce the apparent diagnostic from \(\mathsf D\) to \(\mathsf L\);
- minimal certificate size is not preserved under compression;
- reconstructing local incidence from compressed global spaces is underdetermined.

Possible flagship result:

> For every \(n\), there are finite \(\mathsf D\)-presentations whose smallest compatibility certificate has size \(n\), but whose terminal compression has a one-object \(\mathsf L\)-certificate. Conversely, decompressions of one compressed object can realise arbitrarily large minimal certificate depth.

### 6. Hiding, projection, and witness complexity

Analyze existential projection of internal variables:

- set-level nonemptiness is preserved by projection;
- computable or bounded witness recovery can fail;
- certificate extraction may become harder after hiding;
- exact variable elimination can blow up local relation size.

This connects ECD to database projection, CSP existential quantification, and synthesis with hidden implementation details.

### 7. Source integration and database repair

Make source integration the central application.

Topics:

- consistency of local source tables;
- minimal inconsistent subfamilies;
- join-tree positive cases;
- cyclic parity obstructions;
- source repair operations and edit costs;
- protected facts and nontrivial repair feasibility;
- query-preserving integration;
- certificate transport under schema mappings.

Potential theorem package:

- NP-completeness and \(\#\mathrm P\)-completeness for general integration;
- polynomial-time solvability for join-tree acyclic source schemas with separator consistency;
- FPT algorithms by hypertree width;
- finite dual certificates for linear/probabilistic source constraints;
- compression theorem showing terminal integration hides whether inconsistency was local or gluing-based.

### 8. Bell and probabilistic data fusion as LP case studies

Extend the finite Bell repair profile into a general LP-based marginal-coupling chapter:

- marginal compatibility as linear feasibility;
- Farkas certificates as separating inequalities;
- finite-sample testing under sampling models;
- detector/postselection repairs as LPs;
- contextual fraction and noncontextual fraction as LPs.

This is algorithmically useful but likely belongs to a specialized chapter rather than the main JACM-style core.

### 9. Implementation and resource algorithms

For finite presentations, separate:

- evaluating a fixed policy;
- synthesizing a policy from an instance description;
- compiling a policy through a morphism;
- verifying a resource certificate.

Develop resource-aware complexity statements for:

- bounded time;
- memory-limited policies;
- communication-limited distributed selectors;
- circuit-size bounded realizations;
- finite-state controllers.

### 10. Benchmark problems and reductions

Provide canonical reductions and examples:

- 3SAT to finite distributed selectors;
- \(\#3\mathrm{SAT}\) to source-integration counting;
- parity cycles as minimal \(\mathsf D\)-certificates;
- affine systems as polynomial-time but certificate-rich examples;
- Bell local-polytope membership as LP feasibility;
- hidden-witness examples showing projection can erase \(\mathsf K\)-data.

## Suggested chapter structure

1. Finite ECD presentations and explicit encodings.
2. Decision complexity: NP-completeness and tractable subclasses.
3. Width measures and dynamic programming.
4. Counting compatible families.
5. Certificate extraction and verification.
6. Compression, decompression, and certificate depth.
7. Hiding, projection, and witness recovery.
8. Source integration and database repair.
9. Probabilistic coupling and Bell/data-fusion LPs.
10. Resource-bounded synthesis and implementation complexity.
11. Case studies and benchmark reductions.
12. Open algorithmic problems.

## Focused article extraction

A strong JACM-style article should likely be narrower than the full monograph. Candidate extraction:

**Algorithms and Certificates for Finite Local-to-Global Selection**

Core results:

1. finite ECD explicit-input formalism;
2. NP-completeness and \(\#\mathrm P\)-completeness;
3. bounded-width FPT algorithms;
4. tractable affine and convex subclasses;
5. certificate extraction and compression/certificate-loss theorem;
6. source-integration application.

## Required references to add later

- Yannakakis on acyclic database schemes and join algorithms.
- Beeri--Fagin--Maier--Yannakakis on acyclic database schemes.
- Grohe/Marx or Gottlob et al. on hypertree width and CSP tractability.
- Valiant on \(\#\mathrm P\).
- Schrijver or standard LP references for Farkas/LP certificates.
- Database repair literature such as Arenas--Bertossi--Chomicki.

## Development status

This file is a second-monograph plan. It is not part of the current monograph's proved theorem set. The current monograph supplies the foundations and several finite examples; this second monograph would supply the algorithmic classification and certificate-extraction theory.
