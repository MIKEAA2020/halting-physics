# Release manifest template

## Repository / DOI

- Repository URL: TODO
- DOI / archival identifier: TODO
- Release tag or commit hash: TODO
- Date frozen: TODO

## Environment

- OS: TODO
- Python: TODO
- External solvers, if any: TODO
- Hardware for baseline experiments, if any: TODO

## Required reproduction commands

```bash
make reproduce
```

Expected primary outputs:

- `repro_report.json`
- `reports/benchmark_sweep.json`
- `reports/certificate_size_vs_width.svg`
- `reports/verify_time_vs_certificate_size.svg`

## Claim boundary

This release certifies finite explicit-table examples and exact finite affine algebraic models. It does not claim continuum-mechanics validation or external-solver performance superiority unless an additional baseline report with fixed hardware and solver versions is attached.

## Files to archive

- source scripts: `*.py`, `Makefile`, `reproduce.sh`
- examples: `examples/*.json`, generated baseline encodings when relevant
- reports: `repro_report.json`, `reports/*.json`, `reports/*.svg`
- documentation: `README.md`, `ARTIFACT_MANIFEST.md`, `ARTIFACT_APPENDIX.md`, this release manifest
