PYTHON ?= python3
VENV ?= .venv
PYTHON_RUN ?= $(shell if [ -x "$(VENV)/bin/python" ]; then printf "%s" "$(VENV)/bin/python"; else printf "%s" "$(PYTHON)"; fi)
ARTIFACTGATE ?= $(shell if [ -x "$(VENV)/bin/artifactgate" ]; then printf "%s" "$(VENV)/bin/artifactgate"; else printf "%s" "artifactgate"; fi)
PYTEST ?= $(shell if [ -x "$(VENV)/bin/pytest" ]; then printf "%s" "$(VENV)/bin/pytest"; else printf "%s" "pytest"; fi)
RUFF ?= $(shell if [ -x "$(VENV)/bin/ruff" ]; then printf "%s" "$(VENV)/bin/ruff"; else printf "%s" "ruff"; fi)
RUFF_FLAGS ?= --no-cache

.PHONY: install test lint smoke ingest-all reproduce-core negative-claims corrupted-tests scalability baseline summaries figures manuscript-package reproduce-all package-release supplementary-package dist-package release-preflight prepare-release-metadata-dry-run external-release-check preflight generate-ist-datasets file-audit ist-manuscript-gate ist-strong-l2 literature-map claimbench corruption-extended external-cases rq0-quality rq1-ingest-all rq2-replay-core rq2-replay-repeats rq3-negative-claims rq4-corrupted-artifacts rq5-evidence-classification rq6-external-cases rq6-scalability rq7-baseline rq8-ablation rq9-local-backends rq10-reviewer-walkthrough ist-reports ist-package ist-all clean

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -e ".[dev]"
	rm -rf artifactgate_eda.egg-info repo/src/*.egg-info

test:
	$(PYTEST)

lint:
	$(PYTHON_RUN) -m compileall repo/src tests
	$(RUFF) check $(RUFF_FLAGS) repo/src tests paper/figure_sources scripts

smoke:
	$(ARTIFACTGATE) ingest examples/ngspice_minimal --adapter ngspice --out outputs/smoke_ngspice
	$(ARTIFACTGATE) validate outputs/smoke_ngspice/artifact_index.json
	$(ARTIFACTGATE) claim-check --claims examples/negative_claim_cases/claims.md --artifact-index outputs/smoke_ngspice/artifact_index.json --out outputs/smoke_claims --expect-fail UNSUPPORTED_CLAIM

ingest-all:
	$(ARTIFACTGATE) ingest examples/ngspice_minimal --adapter ngspice --out outputs/e1_ngspice
	$(ARTIFACTGATE) ingest examples/hdl_icarus_yosys_minimal --adapter icarus --out outputs/e1_icarus
	$(ARTIFACTGATE) ingest examples/hdl_icarus_yosys_minimal --adapter yosys --out outputs/e1_yosys
	$(ARTIFACTGATE) ingest examples/hdl_verilator_minimal --adapter verilator --out outputs/e1_verilator
	$(ARTIFACTGATE) ingest examples/plecs_metadata_only --adapter plecs --out outputs/e1_plecs
	$(ARTIFACTGATE) ingest examples/logisim_metadata_only --adapter logisim --out outputs/e1_logisim

reproduce-core:
	$(ARTIFACTGATE) replay examples/ngspice_minimal --adapter ngspice --out outputs/replay_ngspice
	$(ARTIFACTGATE) replay examples/hdl_icarus_yosys_minimal --adapter icarus --out outputs/replay_icarus
	$(ARTIFACTGATE) replay examples/hdl_icarus_yosys_minimal --adapter yosys --out outputs/replay_yosys
	$(ARTIFACTGATE) replay examples/hdl_verilator_minimal --adapter verilator --out outputs/replay_verilator
	$(ARTIFACTGATE) report outputs/replay_ngspice --out reports/replay_ngspice.md
	$(ARTIFACTGATE) report outputs/replay_icarus --out reports/replay_icarus.md
	$(ARTIFACTGATE) report outputs/replay_yosys --out reports/replay_yosys.md
	$(ARTIFACTGATE) report outputs/replay_verilator --out reports/replay_verilator.md

negative-claims:
	$(ARTIFACTGATE) claim-check --claims examples/negative_claim_cases/claims.md --artifact-index outputs/e1_ngspice/artifact_index.json --policy repo/src/artifactgate_eda/policies/forbidden_claims.yaml --out outputs/e3_negative_claims --expect-fail UNSUPPORTED_CLAIM

corrupted-tests:
	$(ARTIFACTGATE) validate examples/corrupted_artifact_cases/missing_log --expect-fail MISSING_ARTIFACT
	$(ARTIFACTGATE) validate examples/corrupted_artifact_cases/hash_mismatch --expect-fail HASH_MISMATCH
	$(ARTIFACTGATE) validate examples/corrupted_artifact_cases/missing_tool_version --expect-fail MISSING_TOOL_VERSION
	$(ARTIFACTGATE) validate examples/corrupted_artifact_cases/broken_claim_reference --expect-fail BROKEN_CLAIM_REFERENCE
	$(ARTIFACTGATE) validate examples/corrupted_artifact_cases/absolute_path --expect-fail NON_PORTABLE_PATH
	$(ARTIFACTGATE) claim-check --claims examples/corrupted_artifact_cases/simulation_to_hardware_escalation/claims.md --artifact-index outputs/e1_ngspice/artifact_index.json --expect-fail UNSUPPORTED_CLAIM
	$(ARTIFACTGATE) claim-check --claims examples/corrupted_artifact_cases/yosys_to_vivado_escalation/claims.md --artifact-index outputs/e1_yosys/artifact_index.json --expect-fail EVIDENCE_LEVEL_ESCALATION

scalability:
	$(ARTIFACTGATE) benchmark-scale --base examples/scalability_cases/cfb_1k --scale 1000 --out outputs/scale_1k
	$(ARTIFACTGATE) benchmark-scale --base examples/scalability_cases/cfb_1k --scale 3000 --out outputs/scale_3k
	$(ARTIFACTGATE) benchmark-scale --base examples/scalability_cases/cfb_1k --scale 5000 --out outputs/scale_5k
	$(ARTIFACTGATE) benchmark-scale --base examples/scalability_cases/cfb_1k --scale 10000 --out outputs/scale_10k

baseline:
	$(ARTIFACTGATE) report-baseline --out reports/e6_baseline_comparison.md

generate-ist-datasets:
	$(PYTHON_RUN) scripts/generate_ist_datasets.py

file-audit:
	$(PYTHON_RUN) scripts/audit_file_inventory.py --root . --out reports/file_inventory_full.csv
	$(PYTHON_RUN) scripts/build_evidence_graph.py --inventory reports/file_inventory_full.csv --out reports/evidence_graph_edges.csv
	$(PYTHON_RUN) scripts/find_claim_boundary_terms.py --root . --policy repo/src/artifactgate_eda/policies/forbidden_claims.yaml --out reports/claim_boundary_scan.csv

ist-manuscript-gate:
	$(PYTHON_RUN) scripts/check_ist_manuscript_claims.py --policy repo/src/artifactgate_eda/policies/forbidden_claims.yaml --out reports/ist_manuscript_claim_gate.md paper/manuscript_ist.md paper/manuscript_ist.tex

ist-strong-l2: file-audit ist-manuscript-gate

literature-map:
	$(PYTHON_RUN) scripts/search_literature_matrix.py --out literature/literature_matrix.csv

claimbench: rq1-ingest-all
	$(PYTHON_RUN) scripts/generate_claimbench_eda.py --n 1200 --out examples/claimbench_eda
	$(ARTIFACTGATE) claim-check --claims examples/claimbench_eda/claimbench_claims.csv --artifact-index outputs/rq1_ngspice/artifact_index.json --policy repo/src/artifactgate_eda/policies/forbidden_claims.yaml --out outputs/rq3_claimbench --expect-fail UNSUPPORTED_CLAIM
	$(PYTHON_RUN) scripts/generate_claimbench_eda.py --summarize outputs/rq3_claimbench/claim_check_report.json --reports reports

rq0-quality:
	$(ARTIFACTGATE) benchmark --suite repository --repo . --out outputs/rq0_repository_quality --reports reports

rq1-ingest-all: generate-ist-datasets
	$(ARTIFACTGATE) ingest examples/ngspice_minimal --adapter ngspice --out outputs/rq1_ngspice
	$(ARTIFACTGATE) ingest examples/hdl_icarus_yosys_minimal --adapter icarus --out outputs/rq1_icarus
	$(ARTIFACTGATE) ingest examples/hdl_icarus_yosys_minimal --adapter yosys --out outputs/rq1_yosys
	$(ARTIFACTGATE) ingest examples/hdl_verilator_minimal --adapter verilator --out outputs/rq1_verilator
	$(ARTIFACTGATE) ingest examples/plecs_metadata_only --adapter plecs --out outputs/rq1_plecs
	$(ARTIFACTGATE) ingest examples/ltspice_metadata_only --adapter ltspice --out outputs/rq1_ltspice
	$(ARTIFACTGATE) ingest examples/logisim_metadata_only --adapter logisim --out outputs/rq1_logisim
	$(ARTIFACTGATE) ingest examples/vivado_stub_boundary --adapter vivado_stub --out outputs/rq1_vivado_stub

rq2-replay-core: generate-ist-datasets
	$(ARTIFACTGATE) replay examples/ngspice_minimal --adapter ngspice --out outputs/rq2_ngspice_minimal
	$(ARTIFACTGATE) replay examples/ngspice_circuitfaultbench_sample --adapter ngspice --out outputs/rq2_cfb_sample
	$(ARTIFACTGATE) replay examples/hdl_icarus_yosys_minimal --adapter icarus --out outputs/rq2_icarus
	$(ARTIFACTGATE) replay examples/hdl_verilator_minimal --adapter verilator --out outputs/rq2_verilator
	$(ARTIFACTGATE) replay examples/hdl_icarus_yosys_minimal --adapter yosys --out outputs/rq2_yosys
	$(ARTIFACTGATE) report outputs/rq2_ngspice_minimal --out reports/rq2_ngspice_minimal.md
	$(ARTIFACTGATE) report outputs/rq2_cfb_sample --out reports/rq2_cfb_sample.md
	$(ARTIFACTGATE) report outputs/rq2_icarus --out reports/rq2_icarus.md
	$(ARTIFACTGATE) report outputs/rq2_verilator --out reports/rq2_verilator.md
	$(ARTIFACTGATE) report outputs/rq2_yosys --out reports/rq2_yosys.md

rq2-replay-repeats: generate-ist-datasets
	$(PYTHON_RUN) scripts/run_replay_repeats.py --repeats 10 --out outputs/replay_repeats --reports reports

rq3-negative-claims: generate-ist-datasets rq1-ingest-all
	$(ARTIFACTGATE) claim-check --claims examples/negative_claim_cases/claims_full.csv --artifact-index outputs/rq1_ngspice/artifact_index.json --policy repo/src/artifactgate_eda/policies/forbidden_claims.yaml --out outputs/rq3_negative_claims --expect-fail UNSUPPORTED_CLAIM

corruption-extended:
	$(PYTHON_RUN) scripts/generate_corrupted_cases_extended.py --classes 30 --instances 30 --clean-cases 30 --out examples/corrupted_artifact_cases_extended
	$(ARTIFACTGATE) benchmark --suite corrupted --repo . --out outputs/rq4_corrupted_artifacts --reports reports

rq4-corrupted-artifacts: corruption-extended

rq5-evidence-classification: generate-ist-datasets
	$(ARTIFACTGATE) benchmark --suite evidence --repo . --out outputs/rq5_evidence_classification --reports reports

external-cases:
	$(PYTHON_RUN) scripts/prepare_external_eda_cases.py --out examples/external_cases
	$(ARTIFACTGATE) benchmark --suite external --repo . --out outputs/rq6_external_cases --reports reports

rq6-external-cases: external-cases

rq6-scalability:
	$(ARTIFACTGATE) benchmark --suite scalability --repo . --out outputs/rq6_scalability --reports reports --repeats 5

rq7-baseline:
	$(ARTIFACTGATE) benchmark --suite baseline --repo . --out outputs/rq7_baseline --reports reports

rq8-ablation:
	$(ARTIFACTGATE) ablate --out outputs/rq8_ablation --reports reports

rq9-local-backends:
	$(ARTIFACTGATE) benchmark --suite local-backends --repo . --out outputs/rq9_local_backends --reports reports

rq10-reviewer-walkthrough:
	$(ARTIFACTGATE) benchmark --suite reviewer-walkthrough --repo . --out outputs/rq10_reviewer_walkthrough --reports reports

ist-reports:
	$(ARTIFACTGATE) benchmark --suite reports --repo . --out outputs/ist_reports --reports reports

ist-package:
	$(PYTHON_RUN) scripts/package_ist_artifacts.py

ist-all: lint test smoke rq0-quality rq1-ingest-all rq2-replay-core rq2-replay-repeats rq3-negative-claims rq4-corrupted-artifacts rq5-evidence-classification rq6-external-cases rq6-scalability rq7-baseline rq8-ablation rq9-local-backends rq10-reviewer-walkthrough ist-reports ist-package

summaries:
	$(ARTIFACTGATE) summarize --repo . --out reports

figures:
	$(PYTHON_RUN) paper/figure_sources/generate_figures.py

manuscript-package: figures
	$(PYTHON_RUN) scripts/build_manuscript_package.py

reproduce-all: lint test smoke ingest-all reproduce-core negative-claims corrupted-tests scalability baseline summaries manuscript-package

package-release: summaries
	$(ARTIFACTGATE) package outputs/replay_ngspice --out release/ngspice_minimal_artifactgate.zip
	$(ARTIFACTGATE) package outputs/replay_icarus --out release/hdl_icarus_artifactgate.zip
	$(ARTIFACTGATE) package outputs/replay_yosys --out release/yosys_artifactgate.zip

supplementary-package: manuscript-package summaries
	$(PYTHON_RUN) scripts/package_supplementary.py

dist-package:
	rm -rf dist build artifactgate_eda.egg-info repo/src/*.egg-info
	$(PYTHON_RUN) -m build
	rm -rf build artifactgate_eda.egg-info repo/src/*.egg-info

release-preflight:
	$(PYTHON_RUN) scripts/release_preflight.py

prepare-release-metadata-dry-run:
	$(PYTHON_RUN) scripts/prepare_release_metadata.py --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA --doi 10.5281/zenodo.0000000 --release-date 2026-06-22

external-release-check:
	$(PYTHON_RUN) scripts/external_release_check.py

preflight: reproduce-all package-release supplementary-package dist-package release-preflight

clean:
	rm -rf outputs/* release/* dist build .pytest_cache .ruff_cache artifactgate_eda.egg-info repo/src/*.egg-info
