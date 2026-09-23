.PHONY: reproduce smoke sweep plots external-baselines mechanics-benchmarks sparsification-study mechanics-baselines clean

PY ?= python3

reproduce: smoke sweep plots external-baselines mechanics-benchmarks sparsification-study mechanics-baselines
	@echo "Reproduction complete. See repro_report.json and reports/."

smoke:
	$(PY) run_repro_checks.py

sweep:
	mkdir -p reports
	$(PY) benchmark_sweep.py --out reports/benchmark_sweep.json

plots:
	mkdir -p reports
	$(PY) plot_reports.py reports/benchmark_sweep.json --outdir reports

# Gated external baseline sweep: runs every solver found on PATH or named by
# EXTERNAL_ECD_MINISAT / EXTERNAL_ECD_KISSAT / EXTERNAL_ECD_Z3 /
# EXTERNAL_ECD_CPSAT_PYTHON / EXTERNAL_ECD_HIGHS_PYTHON. With no solver
# available the report is INCONCLUSIVE.
external-baselines:
	mkdir -p reports
	$(PY) external_baseline_sweep.py --out reports/external_baseline_sweep.json

# Phase 4 mechanics benchmark suite: exact rational structural models,
# certified rows and relations, instances, decompositions, DP certificates,
# sensor-repair demonstrator, and the ten-bar affine cross-validation.
mechanics-benchmarks:
	mkdir -p reports
	$(PY) mechanics_benchmarks.py --out reports/mechanics_benchmarks.json

# Phase 5 width-adaptive sparsification study: retained-scope ladders,
# monotonicity verification, inner/outer brackets, unresolved fractions.
sparsification-study:
	mkdir -p reports
	$(PY) sparsification_study.py --out reports/sparsification_study.json

# Phase 6 comparative scaling study on mechanics-derived instances under the
# fixed external-baseline protocol (same solvers, limits, and cross-checks;
# native DP as a bounded subprocess). With no solver available the report is
# INCONCLUSIVE.
mechanics-baselines:
	mkdir -p reports
	$(PY) mechanics_baseline_sweep.py --out reports/mechanics_external_baseline_sweep.json

clean:
	rm -f repro_stdout.txt reports/benchmark_sweep_stdout.json reports/plot_stdout.json
	rm -rf reports/_run_tmp
