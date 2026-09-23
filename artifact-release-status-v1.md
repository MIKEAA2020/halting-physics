# Artifact release status v1

## Completed

1. A polished LaTeX artifact appendix has been prepared:

```text
/home/user/companion-artifact-appendix-v1.tex
```

It summarizes:

- finite explicit-table instance format;
- native certificate schemas;
- tree-decomposition DP certificates;
- FE-row and sparsification certificates;
- baseline encodings;
- external-solver discipline;
- reproduction commands;
- claim boundary.

2. The companion plan has been updated:

```text
/home/user/monograph-2-algorithms-and-certificates-plan-v17.md
```

3. The external baseline gate was run again:

```text
/home/user/finite_ecd_prototype/reports/external_baselines.json
```

Current status:

```json
{
  "availability": {
    "minisat": false,
    "kissat": false,
    "z3": false
  },
  "runs": [],
  "status": "INCONCLUSIVE",
  "reason": "no supported external solver installed"
}
```

No performance claim follows from this.

## Blocked pending repository deposit

The release manifest cannot be frozen yet because the repository URL, DOI or archival identifier, release tag/commit hash, and freeze date are not yet available.

Template remains:

```text
/home/user/finite_ecd_prototype/RELEASE_MANIFEST_TEMPLATE.md
```

## Placeholder wording for the companion article

Until the link is available, use:

> An artifact containing the finite ECD prototype and reproduction scripts will be deposited in a public repository before publication.

After deposit, replace this with the repository URL, DOI, release tag or commit hash, and freeze date.
