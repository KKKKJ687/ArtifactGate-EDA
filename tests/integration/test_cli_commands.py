import csv
from pathlib import Path

from artifactgate_eda.cli import main

ROOT = Path(__file__).resolve().parents[2]


def test_ingest_cli(tmp_path):
    out = tmp_path / "cli_ingest"
    assert main(["ingest", str(ROOT / "examples" / "ngspice_minimal"), "--adapter", "ngspice", "--out", str(out)]) == 0
    assert (out / "artifact_index.json").exists()


def test_claim_check_cli_expected_fail(tmp_path):
    ingest_out = tmp_path / "ingest"
    assert main(["ingest", str(ROOT / "examples" / "ngspice_minimal"), "--adapter", "ngspice", "--out", str(ingest_out)]) == 0
    assert (
        main(
            [
                "claim-check",
                "--claims",
                str(ROOT / "examples" / "negative_claim_cases" / "claims.md"),
                "--artifact-index",
                str(ingest_out / "artifact_index.json"),
                "--out",
                str(tmp_path / "claims"),
                "--expect-fail",
                "UNSUPPORTED_CLAIM",
            ]
        )
        == 0
    )


def test_ist_benchmark_and_ablate_cli(tmp_path):
    reports = tmp_path / "reports"
    assert (
        main(
            [
                "benchmark",
                "--suite",
                "corrupted",
                "--out",
                str(tmp_path / "corrupted"),
                "--reports",
                str(reports),
            ]
        )
        == 0
    )
    assert (reports / "rq4_corrupted_artifact_detection.md").exists()
    assert main(["ablate", "--out", str(tmp_path / "ablation"), "--reports", str(reports)]) == 0
    assert (reports / "rq8_ablation.md").exists()
    with (reports / "rq8_ablation_results.csv").open(newline="", encoding="utf-8") as handle:
        summary_reader = csv.DictReader(handle)
        assert {
            "variant",
            "removed_component",
            "claim_detection_recall",
            "defect_detection_recall",
            "error_classification_accuracy",
            "baseline_task_success_rate",
            "overall_success_drop",
            "overall_bootstrap_drop_ci",
            "overall_cohen_h_effect_size",
            "report_completeness",
            "manual_step_increase_estimate",
            "manual_correction_effort",
            "risk_score_error",
            "status",
        }.issubset(summary_reader.fieldnames or [])
        summary_rows = list(summary_reader)
    with (reports / "rq8_ablation_effect_sizes.csv").open(newline="", encoding="utf-8") as handle:
        effect_rows = list(csv.DictReader(handle))
    with (reports / "rq8_ablation_observations.csv").open(newline="", encoding="utf-8") as handle:
        observation_reader = csv.DictReader(handle)
        assert {
            "variant",
            "experiment",
            "observation_id",
            "expected_success",
            "observed_success",
            "metric",
        }.issubset(observation_reader.fieldnames or [])
        observation_rows = list(observation_reader)
    variants = {row["variant"] for row in summary_rows}
    experiments = {row["experiment"] for row in effect_rows}
    assert len(variants) >= 9
    assert experiments == {"E3_claimbench", "E4_corruption", "E5_evidence_classification", "E8_baseline_tasks"}
    assert len(effect_rows) >= len(variants) * len(experiments)
    assert len(observation_rows) >= len(variants) * 3000
    assert {
        "success_rate_drop",
        "cohen_h_effect_size",
        "bootstrap_drop_ci_low",
        "bootstrap_drop_ci_high",
    }.issubset(effect_rows[0])
    assert (
        main(
            [
                "benchmark",
                "--suite",
                "reviewer-walkthrough",
                "--repo",
                str(ROOT),
                "--out",
                str(tmp_path / "walkthrough"),
                "--reports",
                str(reports),
            ]
        )
        == 0
    )
    assert (reports / "rq10_reviewer_walkthrough.md").exists()
    with (reports / "rq10_reviewer_walkthrough_summary.csv").open(newline="", encoding="utf-8") as handle:
        walkthrough_summary = list(csv.DictReader(handle))
    with (reports / "rq10_reviewer_walkthrough_observations.csv").open(newline="", encoding="utf-8") as handle:
        walkthrough_reader = csv.DictReader(handle)
        assert {
            "walkthrough_id",
            "generated_at_utc",
            "reviewer_mode",
            "human_participants",
            "condition",
            "source_method",
            "task_id",
            "task_prompt",
            "evidence_file",
            "command_log",
            "command_timestamp_utc",
            "observed_success",
            "time_measurement_scope",
            "limitation",
        }.issubset(walkthrough_reader.fieldnames or [])
        walkthrough_observations = list(walkthrough_reader)
    with (reports / "rq10_reviewer_walkthrough_command_log.csv").open(newline="", encoding="utf-8") as handle:
        command_rows = list(csv.DictReader(handle))
    assert {row["condition"] for row in walkthrough_summary} == {"manual_package", "artifactgate_package"}
    assert {row["source_method"] for row in walkthrough_summary} == {"B1_manual_readme_zip", "B7_artifactgate_full"}
    assert len(walkthrough_observations) == 16
    assert {row["human_participants"] for row in walkthrough_observations} == {"0"}
    assert all("not measured human-subject timing" in row["time_measurement_scope"] for row in walkthrough_observations)
    assert {row["step"] for row in command_rows} == {"generate_baseline_source", "write_generated_dry_run"}


def test_external_benchmark_cli(tmp_path):
    reports = tmp_path / "reports"
    assert (
        main(
            [
                "benchmark",
                "--suite",
                "external",
                "--repo",
                str(ROOT),
                "--out",
                str(tmp_path / "external"),
                "--reports",
                str(reports),
            ]
        )
        == 0
    )
    assert (reports / "rq6_external_case_generalization.md").exists()
