from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
PRIVATE_PATH_BYTES_RE = re.compile(rb"(/Users/[^\s'\"`,;:]+|C:\\Users\\[^\s'\"`,;:]+)")
PRIVATE_PATH_REDACTION = b"<REDACTED_ABSOLUTE_PATH>"

IST_FILES = [
    "README.md",
    "docs/cli_reference.md",
    "docs/ist_author_external_completion_packet.md",
    "docs/ist_stronger_plan_source_record.md",
    "examples/claimbench_eda/claimbench_claims.csv",
    "examples/claimbench_eda/claimbench_gold.csv",
    "examples/negative_claim_cases/claims_full.csv",
    "examples/evidence_level_gold_standard/evidence_gold.csv",
    "examples/corrupted_artifact_cases_extended/README.md",
    "examples/corrupted_artifact_cases_extended/case_index.csv",
    "examples/corrupted_artifact_cases_extended/taxonomy.csv",
    "examples/external_cases/README.md",
    "examples/external_cases/source_manifest.csv",
    "reports/e0_repository_installation_quality.md",
    "reports/rq1_multi_adapter_ingestion.md",
    "reports/rq1_multi_adapter_ingestion.csv",
    "reports/rq2_replay_reproducibility.md",
    "reports/rq2_replay_repeats.md",
    "reports/rq2_replay_repeat_summary.csv",
    "reports/rq2_docker_ci_status.csv",
    "reports/rq2_replay_summary.csv",
    "reports/rq3_negative_claim_injection.md",
    "reports/rq3_claimbench_summary.md",
    "reports/rq3_confusion_by_claim_type.csv",
    "reports/rq3_negative_claim_detection_summary.csv",
    "reports/rq3_confusion_matrix.csv",
    "reports/rq3_safe_rewrite_suggestions.md",
    "reports/rq4_corrupted_artifact_detection.md",
    "reports/rq4_corrupted_artifact_detection_summary.csv",
    "reports/rq4_error_classification_matrix.csv",
    "reports/rq4_defect_taxonomy.md",
    "reports/rq4_corruption_extended_results.csv",
    "reports/rq4_defect_confusion_matrix.csv",
    "reports/rq4_clean_specificity_cases.csv",
    "reports/rq4_severity_weighted_detection.md",
    "reports/rq5_evidence_level_classification.md",
    "reports/rq5_evidence_level_classification_summary.csv",
    "reports/rq5_evidence_level_confusion_matrix.csv",
    "reports/rq5_evidence_level_predictions.csv",
    "reports/rq5_evidence_level_holdout_summary.csv",
    "reports/rq6_external_case_generalization.md",
    "reports/rq6_external_case_generalization.csv",
    "reports/rq6_external_case_generalization_summary.csv",
    "reports/rq6_scalability.md",
    "reports/rq6_scalability_runtime.csv",
    "reports/rq6_scalability_memory.csv",
    "reports/rq6_scalability_summary.csv",
    "reports/rq7_scalability_summary_extended.md",
    "reports/rq7_scalability_extended_runtime.csv",
    "reports/rq7_scalability_extended_memory.csv",
    "reports/rq7_scalability_model_fit.csv",
    "reports/rq7_scalability_extended_summary.csv",
    "reports/rq7_baseline_comparison.md",
    "reports/rq7_baseline_comparison.csv",
    "reports/rq7_baseline_task_execution.md",
    "reports/rq7_baseline_task_results.csv",
    "reports/rq8_ablation.md",
    "reports/rq8_ablation_results.csv",
    "reports/rq8_ablation_effect_sizes.csv",
    "reports/rq8_ablation_observations.csv",
    "reports/rq9_local_backend_audit.md",
    "reports/rq9_optional_backend_status.csv",
    "reports/rq10_reviewer_walkthrough.md",
    "reports/rq10_reviewer_walkthrough_summary.csv",
    "reports/rq10_reviewer_walkthrough_observations.csv",
    "reports/rq10_reviewer_walkthrough_command_log.csv",
    "reports/ist_empirical_evaluation_summary.md",
    "reports/IST_GAP_AUDIT.md",
    "reports/IST_EXPERIMENT_CONTRACT.md",
    "reports/IST_FROZEN_CLAIM_BOUNDARY.md",
    "reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md",
    "reports/IST_VERIFICATION_RECEIPTS.json",
    "reports/IST_WORKFLOW_REFLECTION_LOG.md",
    "reports/IST_WORKFLOW_GOVERNOR_GATE_LEDGER.md",
    "reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md",
    "reports/IST_FINAL_ACCEPTANCE_AUDIT.md",
    ".codex_workflow/WORKFLOW_STATE.md",
    ".codex_workflow/STAGE_CONTROL_PACKET.md",
    "paper/manuscript_ist.md",
    "paper/manuscript_ist.tex",
    "paper/figures/scalability_fit.png",
]


def sanitize_payload(payload: bytes) -> tuple[bytes, bool]:
    cleaned = PRIVATE_PATH_BYTES_RE.sub(PRIVATE_PATH_REDACTION, payload)
    return cleaned, cleaned != payload


def zip_private_path_hits(path: Path) -> list[str]:
    hits: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            if PRIVATE_PATH_BYTES_RE.search(zf.read(name)):
                hits.append(name)
    return hits


def main() -> int:
    external_case_files = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "examples" / "external_cases").rglob("*"))
        if path.is_file() and not path.name.startswith("._")
    ]
    baseline_output_files = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "outputs" / "rq7_baseline").rglob("*"))
        if path.is_file() and not path.name.startswith("._")
    ]
    ablation_output_files = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "outputs" / "rq8_ablation").rglob("*"))
        if path.is_file() and not path.name.startswith("._")
    ]
    walkthrough_output_files = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "outputs" / "rq10_reviewer_walkthrough").rglob("*"))
        if path.is_file() and not path.name.startswith("._")
    ]
    package_files = sorted(
        dict.fromkeys(
            IST_FILES
            + external_case_files
            + baseline_output_files
            + ablation_output_files
            + walkthrough_output_files
        )
    )
    missing = [rel for rel in IST_FILES if not (ROOT / rel).exists()]
    if missing:
        for rel in missing:
            print(f"missing IST artifact: {rel}")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "package": OUT.name,
        "scope": "IST evaluation artifacts for software-only EDA experiment artifact engineering",
        "external_release_mutated": False,
        "files": package_files,
        "sanitized_private_path_payloads": [
            rel
            for rel in package_files
            if PRIVATE_PATH_BYTES_RE.search((ROOT / rel).read_bytes())
        ],
    }
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("ist_artifact_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        for rel in package_files:
            payload, _ = sanitize_payload((ROOT / rel).read_bytes())
            zf.writestr(rel, payload)
    private_path_hits = zip_private_path_hits(OUT)
    if private_path_hits:
        for rel in private_path_hits:
            print(f"private path payload in IST zip: {rel}")
        return 1
    print(OUT.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
