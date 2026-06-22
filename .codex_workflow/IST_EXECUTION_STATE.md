# IST Execution State

Date: 2026-06-22

Branch: `feature/ist-upgrade`

Plan source: `../177e7509-fd7b-408c-ba1a-7f266a7d92ab.md`

## Objective

Upgrade ArtifactGate-EDA from the completed SoftwareX release package into an
IST-oriented software engineering method/tool evaluation package while keeping
the evidence boundary at software-only EDA artifacts.

## Boundary

- Main positive evidence remains bounded to adapter ingestion, hashing,
  replay manifests, evidence-level classification, unsupported-claim checks,
  corrupted-package checks, scalability, baseline comparison, ablation, and
  optional-backend audit.
- Vendor implementation, device-image generation, and board-side measurements
  remain outside the current positive evidence layer.
- Optional local backends are audited as optional and must not become core
  reproducibility dependencies.

## Current Execution Packet

Completed in this packet:

- Added `artifactgate benchmark`.
- Added `artifactgate ablate`.
- Added deterministic IST datasets:
  - `examples/negative_claim_cases/claims_full.csv`
  - `examples/evidence_level_gold_standard/evidence_gold.csv`
  - `examples/ltspice_metadata_only/`
  - `examples/vivado_stub_boundary/`
- Added IST Make targets from `rq1-ingest-all` through `ist-all`.
- Generated RQ1-RQ9 reports and `reports/ist_empirical_evaluation_summary.md`.
- Drafted `paper/manuscript_ist.md` and `paper/manuscript_ist.tex`.
- Built local IST evaluation archive:
  `release/artifactgate_eda_ist_evaluation_artifacts.zip`.

Verification already run:

- `make external-release-check`
- `make preflight`
- `make ist-all`

## Remaining Work

- External IST archive versioning is intentionally not performed in this
  packet. Creating a new external archive should use a new version after user
  confirmation.
- Author-side submission metadata remains separate and must not be fabricated.
