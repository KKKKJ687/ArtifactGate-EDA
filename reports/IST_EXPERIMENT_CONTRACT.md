# IST Experiment Contract

Plan source: `docs/ist_stronger_plan_source_record.md`

## Goal

Evaluate ArtifactGate-EDA as a software engineering method and tool for
claim-safe, replay-checkable, and reviewer-auditable software-only EDA
experiment artifacts.

## Allowed Paths

- `repo/src/artifactgate_eda/`
- `examples/`
- `tests/`
- `scripts/`
- `reports/`
- `docs/`
- `.codex_workflow/`
- `paper/manuscript_ist.md`
- `paper/manuscript_ist.tex`

## Protected Paths

- Existing release archives under `release/`
- Existing Python distribution archives under `dist/`
- Existing SoftwareX manuscript files unless a targeted update is required
- Git tags and archived external release records

## Baseline Command

```bash
make preflight
make external-release-check
```

## Experiment Command

```bash
make ist-all
```

## Evaluation Commands

```bash
make rq1-ingest-all
make rq2-replay-core
make rq3-negative-claims
make rq4-corrupted-artifacts
make rq5-evidence-classification
make rq6-external-cases
make rq6-scalability
make rq7-baseline
make rq8-ablation
make rq9-local-backends
make rq10-reviewer-walkthrough
make ist-reports
```

## Primary Metric

All RQ reports must be generated with PASS status in
`reports/ist_empirical_evaluation_summary.md`.

## Improvement Rule

Keep an implementation change only if it makes at least one IST gate more true
without weakening the completed SoftwareX release baseline or expanding the
claim boundary beyond software-only artifact evidence.

## Rollback Policy

Use file-level restore from the current branch if a change breaks `make
preflight`, `make external-release-check`, or `make ist-all`. Do not move
release tags or mutate archived external records as part of rollback.

## Approval Gates

- Creating a new external archive version requires user confirmation.
- Filling author-side submission metadata requires author confirmation.
- Introducing a core dependency on local commercial tools is not allowed.

## Required Artifacts

- `examples/negative_claim_cases/claims_full.csv`
- `examples/evidence_level_gold_standard/evidence_gold.csv`
- `examples/external_cases/source_manifest.csv`
- `reports/rq1_multi_adapter_ingestion.md`
- `reports/rq2_replay_reproducibility.md`
- `reports/rq3_negative_claim_injection.md`
- `reports/rq4_corrupted_artifact_detection.md`
- `reports/rq5_evidence_level_classification.md`
- `reports/rq6_external_case_generalization.md`
- `reports/rq6_scalability.md`
- `reports/rq7_scalability_summary_extended.md`
- `reports/rq7_scalability_model_fit.csv`
- `reports/rq7_baseline_task_execution.md`
- `reports/rq7_baseline_task_results.csv`
- `reports/rq7_baseline_comparison.md`
- `reports/rq8_ablation.md`
- `reports/rq8_ablation_results.csv`
- `reports/rq8_ablation_effect_sizes.csv`
- `reports/rq8_ablation_observations.csv`
- `reports/rq9_local_backend_audit.md`
- `reports/rq10_reviewer_walkthrough.md`
- `reports/rq10_reviewer_walkthrough_summary.csv`
- `reports/rq10_reviewer_walkthrough_observations.csv`
- `reports/rq10_reviewer_walkthrough_command_log.csv`
- `reports/ist_empirical_evaluation_summary.md`
- `reports/IST_VERIFICATION_RECEIPTS.json`
- `reports/IST_WORKFLOW_REFLECTION_LOG.md`
- `paper/manuscript_ist.md`
- `release/artifactgate_eda_ist_evaluation_artifacts.zip`
