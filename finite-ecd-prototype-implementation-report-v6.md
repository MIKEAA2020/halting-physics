# Finite ECD prototype implementation report v6

## New in v6

This implements the repository-readiness and release-preparation items.

## 1. Repository-ready reproduction entry point

Added:

```text
/home/user/finite_ecd_prototype/Makefile
/home/user/finite_ecd_prototype/reproduce.sh
```

Primary command:

```bash
make reproduce
```

Equivalent shell entry point:

```bash
./reproduce.sh
```

The command runs:

1. `run_repro_checks.py`;
2. `benchmark_sweep.py --out reports/benchmark_sweep.json`;
3. `plot_reports.py reports/benchmark_sweep.json --outdir reports`.

The command completed successfully in the current workspace.

## 2. Compact artifact appendix

Added:

```text
/home/user/finite_ecd_prototype/ARTIFACT_APPENDIX.md
```

It summarizes:

- finite instance format;
- native certificate schemas;
- baseline encodings;
- external solver discipline;
- reproduction commands.

This is suitable to adapt into a paper appendix or repository documentation.

## 3. Gated external baseline runner

Added:

```text
/home/user/finite_ecd_prototype/run_external_baselines.py
```

It detects supported solvers and only runs optional external baselines when solvers are installed. In the current environment:

```json
{"minisat": false, "kissat": false, "z3": false}
```

Therefore the baseline report is:

```text
INCONCLUSIVE
```

with reason:

```text
no supported external solver installed
```

Output file:

```text
/home/user/finite_ecd_prototype/reports/external_baselines.json
```

No external baseline performance claim is made.

## 4. Release manifest template

Added:

```text
/home/user/finite_ecd_prototype/RELEASE_MANIFEST_TEMPLATE.md
```

It contains placeholders for:

- repository URL;
- DOI or archival identifier;
- release tag or commit hash;
- freeze date;
- OS/Python/hardware/solver versions;
- expected reproduction outputs;
- claim boundary;
- files to archive.

The actual release manifest should be frozen only after the repository or DOI link is available.

## Current repository-readiness status

The artifact now has a one-command reproduction path, documentation for file formats and certificate schemas, conservative external-baseline gating, and a release-manifest template. It is ready for repository packaging once the user supplies the final repository/DOI destination.
