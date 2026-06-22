# IST Gap Audit

Plan source: `docs/ist_stronger_plan_source_record.md`

Audit date: 2026-06-22

## Current State

The SoftwareX release baseline remains intact and verified. The IST upgrade
work now adds an empirical evaluation layer with explicit RQ reports, expanded
CLI entry points, generated datasets, and a separate IST summary.

## Gate Mapping

The strong optimization plan labels baseline execution, ablation, optional
reviewer walkthrough, and new external release as G11-G15. This audit had
already used local sequential labels for inserted empirical gates, so those
rows are crosswalked below.

| Gate | IST requirement | Current evidence | Status |
| --- | --- | --- | --- |
| G1 | Repository hygiene | `make ist-all` E0 report; no resource fork files found | PASS |
| G2 | Installation | Existing `make preflight` and `make ist-all` compile/test path | PASS |
| G3 | CLI | `ingest`, `validate`, `replay`, `claim-check`, `report`, `package`, `compare`, `benchmark`, `ablate` | PASS |
| G4 | Unit tests | 37 pytest cases passed during `make ist-all`; receipt recorded in `reports/IST_VERIFICATION_RECEIPTS.json` | PASS |
| G5 | CI | SoftwareX baseline CI remains externally verified; current IST branch Docker/CI replay is recorded separately and not claimed as fully passed | PASS_WITH_LIMITATION |
| G6 | Core adapters | ngspice, Icarus, and Yosys pass RQ1/RQ2 commands | PASS |
| G7 | Strong adapter | Verilator pass in RQ1/RQ2 commands | PASS |
| G8 | Optional adapters | PLECS, LTspice, Logisim metadata fallback and Vivado stub boundary cases | PASS |
| G9 | Replay | RQ2 replay cases pass and produce reports | PASS |
| G10 | Claim detection | 1300 ClaimBench-EDA rows, critical false negatives = 0 | PASS |
| G11-local | Corruption detection | Deterministic software-only benchmark: 30 defect classes, 900 defect instances, 30 clean specificity cases, observed validator/claim-check codes, critical false pass = 0 | PASS |
| G12 | Evidence classification | 1000 gold-standard rows with holdout/cross-tool groups, macro-F1 >= 0.95, unsupported-level recall >= 0.95, critical escalation errors = 0 | PASS |
| G9-strong / external cases | External case generalization | 10 public external EDA cases, 8 open-source ArtifactGate replay-package/validation cases, adapter success rate 1.00, observed manual adapter fix rate 0, observed hardware dependency count 0 | PASS |
| G10-strong / scalability | Scalability | Synthetic ArtifactGate manifests are written and row-parsed up to 100k rows; 53 measured manifest-processing runtime observations across 1k, 3k, 5k, 10k, 30k, 50k, and 100k; linear-fit R2 > 0.99; memory values are estimates, not measured process RSS | PASS_WITH_LIMITATION |
| G11-strong / G15-local | Baseline execution | Deterministic output-driven harness runs 7 baseline/target emulators on one shared software-only fixture, writes per-method artifacts under `outputs/rq7_baseline/`, evaluates the 8 package-review tasks from generated outputs, and produces 56 task observations; manual time is an operator-step estimate from output-review gaps, not a human-subject timing result | PASS_WITH_LIMITATION |
| G12-strong / G16-local | Ablation | 10 deterministic ablation variants across E3/E4/E5/E8; 32860 generated observation rows; per-experiment Cohen's h effect sizes and bootstrap 95% drop CIs in `reports/rq8_ablation_effect_sizes.csv`; summary in `reports/rq8_ablation.md` | PASS_WITH_LIMITATION |
| G13-strong / G17-local | Structured reviewer walkthrough | RQ10 generated a reviewer-walkthrough dry run with 16 observations across manual-package and ArtifactGate-package conditions, with command-log timestamps in `reports/rq10_reviewer_walkthrough_command_log.csv`; `docs/ist_author_external_completion_packet.md` defines the required author/expert walkthrough evidence; no measured human timing or participant data is claimed | AUTHOR_REQUIRED |
| G17 | Reports | RQ1-RQ10 plus IST summary generated | PASS |
| G18 | Data availability | SoftwareX baseline DOI exists; the IST v0.1.3 DOI `10.5281/zenodo.20798200` exists; IST generated data is reproducible by `make ist-all` and archived as `release/artifactgate_eda_ist_evaluation_artifacts.zip` | PASS |
| G15-strong / external release | New IST release archive + DOI | IST tag/release `v0.1.3` exists, the GitHub release is non-draft, Zenodo DOI `10.5281/zenodo.20798200` resolves, and the existing v0.1.2 GitHub/Zenodo baseline archive was not mutated | PASS |
| G19 | License | Apache-2.0 license present | PASS |
| G20 | Citation metadata | `CITATION.cff` and `codemeta.json` present | PASS |
| G21 | Boundary | No positive claim beyond software-only evidence is introduced by the IST layer | PASS |

## Gate Name Normalization and Threshold Crosswalk

The source IST plan and this local audit use different numbering around the
inserted empirical gates. The normalized names below are the names used by the
workflow-governor ledger and final acceptance checks.

| Normalized gate | Local/source aliases | Threshold | One-vote-fail condition |
| --- | --- | ---: | --- |
| G9 External cases | `G9-strong / external cases` | >=80 | Any claim that replay-package validation is independent vendor-tool execution. |
| G10 Scalability | `G10-strong / scalability` | >=80 | Treating estimated memory as measured RSS or extrapolating beyond manifest processing. |
| G11 Baseline execution | `G11-strong / G15-local` | >=80 | Claiming human timing or external EDA execution from generated-output baselines. |
| G12 Ablation | `G12-strong / G16-local` | >=80 | Treating deterministic ablation observations as human-study evidence. |
| G13 Author/expert walkthrough | `G13-strong / G17-local` | AUTHOR_REQUIRED | Marking generated dry-run outputs as real author or expert evidence. |
| G15 External IST release | `G15-strong / external release` | PASS | Reusing or mutating `v0.1.2`, using a placeholder DOI, or recording a DOI before it resolves publicly. |

## Local Gate Threshold and Veto Matrix

This table makes the status-only local gates above self-contained for S5
workflow-governor review. The normalized strong gates are defined in the
crosswalk above; the rows below cover the remaining local gates.

| Local gate | Threshold | One-vote-fail condition |
| --- | --- | --- |
| G1 Repository hygiene | `make ist-all` E0 inventory exists; no forbidden release payload contamination | Repository metadata, virtual-environment directories, macOS archive metadata, cache files, resource-fork sidecars, or private-path payload appears in release materials. |
| G2 Installation | compile/test path in `make preflight` and `make ist-all` passes | Python package cannot build/import or required local tests fail. |
| G3 CLI | listed CLI commands are available and exercised by tests or preflight | Required CLI command is missing, broken, or undocumented in the local package. |
| G4 Unit tests | current pytest suite passes; latest receipt records 37 passed tests | Any pytest failure or receipt/test-count mismatch. |
| G5 CI | existing SoftwareX baseline CI remains externally verified; IST branch CI is not overclaimed | Claiming unverified IST-branch Docker/CI replay as fully passed. |
| G6 Core adapters | ngspice, Icarus, and Yosys RQ1/RQ2 commands pass | Core adapter fails ingestion/replay or produces missing report evidence. |
| G7 Strong adapter | Verilator RQ1/RQ2 commands pass | Verilator adapter fails local software-only ingestion/replay evidence. |
| G8 Optional adapters | optional metadata/stub adapters produce bounded fallback evidence | Treating metadata fallback or Vivado stub boundary cases as real vendor-tool validation. |
| G9 Replay | RQ2 replay reports exist and required repeats pass for core cases | Replay artifacts missing, hashes inconsistent, or repeats are below the recorded threshold. |
| G10 Claim detection | 1300 ClaimBench rows; critical false negatives equal 0 | Any critical hardware/Vivado/DFX/bitstream/board escalation false negative. |
| G11-local Corruption detection | 30 defect classes, 900 defect instances, 30 clean cases; critical false pass equals 0 | Missing defect class evidence or clean/corrupt package confusion at critical severity. |
| G12 Evidence classification | 1000 gold rows; macro-F1 and unsupported recall at least 0.95 | Unsupported/hardware escalation level is misclassified below the threshold. |
| G17 Reports | RQ1-RQ10 plus IST summary generated | Required report missing, stale, or inconsistent with current receipts. |
| G18 Data availability | local IST archive exists and generated data are reproducible by `make ist-all` | Manuscript-listed package artifact is missing from the archive. |
| G19 License | Apache-2.0 license present | Missing or conflicting license metadata. |
| G20 Citation metadata | `CITATION.cff` and `codemeta.json` present | Placeholder, missing DOI metadata, or inconsistent citation metadata. |
| G21 Boundary | 0 positive claim-boundary leaks in IST layer | Any positive hardware, Vivado, DFX, bitstream, board, or deployment claim leaks into manuscript/release surfaces. |

## Evidence Files

- `reports/ist_empirical_evaluation_summary.md`
- `reports/rq1_multi_adapter_ingestion.md`
- `reports/rq2_replay_reproducibility.md`
- `reports/rq3_negative_claim_injection.md`
- `reports/rq4_corrupted_artifact_detection.md`
- `reports/rq4_defect_taxonomy.md`
- `reports/rq4_corruption_extended_results.csv`
- `reports/rq4_clean_specificity_cases.csv`
- `reports/rq4_severity_weighted_detection.md`
- `reports/rq5_evidence_level_classification.md`
- `reports/rq6_external_case_generalization.md`
- `reports/rq6_external_case_generalization.csv`
- `reports/rq6_external_case_generalization_summary.csv`
- `reports/rq6_scalability.md`
- `reports/rq7_scalability_summary_extended.md`
- `reports/rq7_scalability_extended_runtime.csv`
- `reports/rq7_scalability_extended_memory.csv`
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
- `reports/IST_VERIFICATION_RECEIPTS.json`
- `reports/IST_WORKFLOW_REFLECTION_LOG.md`
- `docs/ist_author_external_completion_packet.md`

## External Archive Note

The local IST evaluation archive does not mutate the existing external
SoftwareX archive. If the IST submission needs an externally archived package,
that should be done as a new version after user confirmation. The author-side
walkthrough and external DOI protocol is recorded in
`docs/ist_author_external_completion_packet.md`.
