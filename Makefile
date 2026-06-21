PYTHON ?= python3
VENV ?= .venv
PYTHON_RUN ?= $(shell if [ -x "$(VENV)/bin/python" ]; then printf "%s" "$(VENV)/bin/python"; else printf "%s" "$(PYTHON)"; fi)
ARTIFACTGATE ?= $(shell if [ -x "$(VENV)/bin/artifactgate" ]; then printf "%s" "$(VENV)/bin/artifactgate"; else printf "%s" "artifactgate"; fi)
PYTEST ?= $(shell if [ -x "$(VENV)/bin/pytest" ]; then printf "%s" "$(VENV)/bin/pytest"; else printf "%s" "pytest"; fi)
RUFF ?= $(shell if [ -x "$(VENV)/bin/ruff" ]; then printf "%s" "$(VENV)/bin/ruff"; else printf "%s" "ruff"; fi)
RUFF_FLAGS ?= --no-cache

.PHONY: install test lint smoke ingest-all reproduce-core negative-claims corrupted-tests scalability baseline summaries figures manuscript-package reproduce-all package-release supplementary-package dist-package release-preflight prepare-release-metadata-dry-run external-release-check preflight clean

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
