# Examples deposit exclusions

Two files of the recorded release v4 workspace archive are not deposited in
the repository tree:

- `examples/mech_dense16_split_dp_certificate.json` (115,626,447 bytes)
  exceeds the repository host's 100 MB per-file limit. It is the recorded
  phase 4 `DP-OPTIMUM` certificate of the dense-chain n=16 split-observation
  instance and is archived verbatim in the release asset
  `workspace-halting-v4.zip` (tag `halting_physics_workspace_v4`).
  SHA-256:
  `8a1c617605b7607b9da807de4e178c892f5f65e02f4ca10c301ccabb3f2c5b73`
- `finite_ecd.py.tmp` (build residue of an intermediate edit; not an
  archived source file per the release manifest's file list).

The dense-chain n=16 baseline encodings (`mech_dense16_*.cnf`, `.lp`,
`_cpsat.json`) and the duplicate native DP certificates were already
excluded from the release archive itself as regenerable, per the release
manifest; they are regenerated deterministically by the sweep scripts from
the deposited instances.

A post-deposit correction: `examples/mech_dense16_same_cpsat.json`, the
CP-SAT encoding of the dense-chain n=16 same instance regenerated during
the v9 replication re-audit, was inadvertently included in the initial
examples deposit commit and is removed in the following commit to keep the
tree aligned with the release manifest's regenerable-encoding exclusion
policy. It is regenerated deterministically by `baseline_encode.py` from the
deposited instance (and by `mechanics_baseline_sweep.py` on every run). The
blob remains retrievable from the deposit commit in the repository history.
