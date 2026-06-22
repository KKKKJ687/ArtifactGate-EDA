# RQ7 Baseline Task Execution

This deterministic task harness runs seven baseline/target emulators on a shared software-only fixture package. Each emulator writes method-specific artifacts under `outputs/rq7_baseline/<method>/`, and the evaluator reads those generated outputs to score the same eight package-review tasks. Manual time is an operator-step estimate computed from generated-output review gaps, not a human-subject timing result.

- fixture package: `outputs/rq7_baseline/fixture_package`
- method output root: `outputs/rq7_baseline`
- task observations: 56
- external EDA execution: no
- hardware/Vivado/bitstream/board evidence claimed: no

| method | tasks_executed | task_success_rate | defect_detection_rate | claim_detection_rate | false_negative_rate | report_completeness_score | manual_time_minutes_estimate | status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| B1_manual_readme_zip | 8 | 0.25 | 0.333333 | 0 | 0.5 | 0.4 | 21.75 | BASELINE |
| B2_plain_checksum_manifest | 8 | 0.25 | 0.666667 | 0 | 0.375 | 0.2 | 17.25 | BASELINE |
| B3_ad_hoc_shell_replay | 8 | 0.5 | 0.666667 | 0 | 0.375 | 0.6 | 14.25 | BASELINE |
| B4_simple_json_manifest | 8 | 0.625 | 1 | 0 | 0.25 | 0.6 | 11.25 | BASELINE |
| B5_ro_crate_style_metadata | 8 | 0.75 | 1 | 0 | 0.25 | 1 | 9 | BASELINE |
| B6_artifactgate_without_claim_policy | 8 | 0.75 | 1 | 0 | 0.25 | 1 | 6.75 | ABLATED_BASELINE |
| B7_artifactgate_full | 8 | 1 | 1 | 1 | 0 | 1 | 2.25 | TARGET |

## Output-Evaluation Contract

| task | expected signal | generated evidence file |
| --- | --- | --- |
| T1 | MISSING_ARTIFACT | `detected_defects.csv` |
| T2 | HASH_MISMATCH | `detected_defects.csv` |
| T3 | NON_PORTABLE_PATH | `detected_defects.csv` |
| T4 | UNSUPPORTED_CLAIM | `claim_results.csv` |
| T5 | EVIDENCE_LEVEL_ESCALATION | `claim_results.csv` |
| T6 | NONEMPTY_COMMANDS | `replay_manifest.json` |
| T7 | NONEMPTY_ROWS | `claim_evidence_table.csv` |
| T8 | REVIEWER_READY_TEXT | `reviewer_report.md` |
