# Remaining implementation-plan and source-audit adjudication

## Executive answer

Yes, there were a few remaining points worth implementing immediately, but most remaining audit suggestions should stay as guarded future work. The safe immediate edits were:

1. remove the last informal phrase from the formal monograph;
2. signpost the nested-prefix variance convention;
3. state explicitly that several external results are cited standard inputs;
4. record the remaining source-audit status in the companion plan.

These have been implemented in:

- `/home/user/monograph-revised-v40.tex`
- `/home/user/monograph-2-algorithms-and-certificates-plan-v10.md`

## Implementation plan points

The `humanization-implementation-plan.md` is mostly already reflected in the monograph: the decision-maker opening, four failure modes, presentation relativity, relation-to-frameworks prose, and formal-but-readable tone are present. One remaining style rule was still actionable: avoid informal phrases like “In plain terms.” The only remaining occurrence was changed to “Operationally.”

Other implementation-plan items are either already implemented or not worth adding now because they would lengthen the monograph without adding theorem content. In particular, the proposed component-role table for prediction games remains optional and is not necessary.

## Source audit points adjudicated

### Implemented now

- Nested-prefix variance signpost: added after the nested-prefix definition.
- External standard-result caveat: added to the relation-to-frameworks discussion.
- Formal tone cleanup: removed the remaining “In plain terms” phrase.

### Already implemented before this pass

- Shared-randomness communication repair.
- Reverse-math nested-prefix off-by-one and prefix-tree hypothesis.
- Farkas vector notation avoiding Bell-functional collision.
- Bell visibility tangent-cone proof note.
- Holonomy empty-intersection and cycle wrap-around conventions.
- Terminal/final-predictor loss clarification.
- AH positive-report parenthetical.
- Action-recall/Kuhn boundary.
- FE inner/outer finite-model handoff.
- Artifact status separation.

### Not implemented now

- New game-theory semantics for behavioural strategies: requires a separate game-theory source doctrine.
- Noninvertible empirical functoriality: remains conjectural until morphisms are fixed.
- Protocol-complex impossibility placements: require process-model legality and carrier maps.
- Measurable-kernel descent: requires measurable spaces and selection hypotheses.
- Continuum-mechanics validity: cannot follow from finite residual certificates alone.
- CP-SAT/MILP scaling claims: require experiments and baselines.

## Next genuinely worthwhile implementation step

The next high-value implementation is not another prose pass. It is to extend `/home/user/finite_ecd_prototype/` with a tiny tree-decomposition dynamic-programming verifier that emits and checks:

- `TREE-DECOMP` certificates;
- `DP-REFUTATION` certificates;
- `DP-OPTIMUM` certificates.

After that, the next feasible mechanics step is a minimal exact affine row generator and `FE-ROW` verifier for spring/truss examples.
