from __future__ import annotations

import os
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_DIRS = [
    "README.md",
    "docs",
    "paper",
    "repo/src",
    "examples",
    "supplementary",
    "reports",
    ".codex_workflow",
]

PRIVATE_PATH_PATTERNS = [re.escape(str(Path.home()))]
if os.environ.get("USERPROFILE"):
    PRIVATE_PATH_PATTERNS.append(re.escape(os.environ["USERPROFILE"]))
PRIVATE_PATH_RE = re.compile("|".join(PRIVATE_PATH_PATTERNS))
PRIVATE_PATH_PAYLOAD_RE = re.compile(rb"(/Users/[^\s'\"`,;:]+|C:\\Users\\[^\s'\"`,;:]+)")

ALLOWED_FORBIDDEN_CONTEXTS = (
    "repo/src/artifactgate_eda/policies/",
    "repo/src/artifactgate_eda/core/artifact.py",
    "examples/negative_claim_cases/",
    "examples/corrupted_artifact_cases/",
    "examples/claimbench_eda/",
    "examples/corrupted_artifact_cases_extended/",
    "examples/ngspice_circuitfaultbench_sample/unsupported_ledger.md",
    "examples/hdl_icarus_yosys_minimal/unsupported_ledger.md",
    "supplementary/cfb_full_artifact_tables/unsupported_ledger.md",
    "supplementary/spec2dfx_full_artifact_tables/unsupported_ledger.md",
    "reports/claim_boundary_scan.csv",
    "reports/evidence_graph_nodes.csv",
    "reports/ist_manuscript_claim_gate.csv",
    "reports/rq3_claimbench_results.csv",
)

LINE_SCOPED_FORBIDDEN_CONTEXTS = {
    "README.md",
    "docs/ist_author_external_completion_packet.md",
    "docs/g13_author_expert_walkthrough_template.md",
    "paper/softwarex_manuscript.md",
    "paper/softwarex_manuscript.tex",
    "paper/manuscript_ist.md",
    "paper/manuscript_ist.tex",
    "reports/rq6_external_case_generalization.md",
    "reports/rq8_ablation.md",
    "reports/IST_FROZEN_CLAIM_BOUNDARY.md",
    "reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md",
    "reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md",
    "reports/IST_FINAL_ACCEPTANCE_AUDIT.md",
    ".codex_workflow/STAGE_CONTROL_PACKET.md",
}

BOUNDARY_CONTEXT_MARKERS = (
    "cannot",
    "does not",
    "do not",
    "must not",
    "no ",
    "not ",
    "not claimed",
    "not evidence",
    "not promoted",
    "not treated as",
    "unsupported",
    "boundary",
    "limitation",
    "stronger evidence",
)

FORBIDDEN_PATTERNS = [
    "hardware validation",
    "hardware-validated",
    "validated on FPGA",
    "FPGA validation",
    "board validation",
    "board-level validation",
    "DFX deployment",
    "DFX implementation completed",
    "partial reconfiguration validated",
    "Vivado timing closure",
    "Vivado implementation evidence",
    "full bitstream generated",
    "partial bitstream generated",
    "bitstream verified",
    "real FPGA speedup",
    "energy saving measured",
    "industrial deployment",
    "complete DFX automation",
    "ReconfigRT-I results show",
    "LA-DFX results show",
    "universal EDA framework",
    "general reproducibility framework for all EDA",
]

RELEASE_ZIPS = [
    "release/ngspice_minimal_artifactgate.zip",
    "release/hdl_icarus_artifactgate.zip",
    "release/yosys_artifactgate.zip",
    "release/artifactgate_eda_supplementary_artifacts.zip",
]
OPTIONAL_RELEASE_ZIPS = [
    "release/artifactgate_eda_ist_evaluation_artifacts.zip",
]
IST_ZIP_REQUIRED = {
    "Makefile",
    ".codex_workflow/WORKFLOW_STATE.md",
    ".codex_workflow/STAGE_CONTROL_PACKET.md",
    "docs/g13_author_expert_walkthrough_template.md",
    "docs/ist_author_external_completion_packet.md",
    "docs/ist_stronger_plan_source_record.md",
    "scripts/validate_g13_walkthrough.py",
    "reports/IST_VERIFICATION_RECEIPTS.json",
    "reports/IST_WORKFLOW_GOVERNOR_GATE_LEDGER.md",
    "reports/IST_FINAL_ACCEPTANCE_AUDIT.md",
    "reports/IST_WORKFLOW_REFLECTION_LOG.md",
    "reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md",
    "paper/MANUSCRIPT_REPRO_PACKAGE.md",
    "paper/manuscript_artifact_manifest.csv",
    "reports/evidence_graph_summary.md",
    "reports/ist_manuscript_claim_gate.md",
}
IST_ZIP_FORBIDDEN = {
    "docs/IST_ArtifactGate_EDA_Stronger_Optimization_Plan.md",
}
IST_ZIP_OPTIONAL_COMPLETE_SETS = [
    {
        "reports/g13_author_expert_walkthrough.md",
        "reports/g13_author_expert_walkthrough_observations.csv",
        "reports/g13_author_expert_walkthrough_command_log.csv",
    }
]
IST_MODE_MARKERS = {
    "docs/ist_author_external_completion_packet.md",
    "paper/manuscript_ist.md",
    "reports/IST_GAP_AUDIT.md",
}
ZIP_PRIVATE_PATH_ALLOWLIST = {
    ("release/artifactgate_eda_supplementary_artifacts.zip", "reports/file_inventory_private_paths.csv"),
}

DIST_FILES = [
    "dist/artifactgate_eda-0.1.3.tar.gz",
    "dist/artifactgate_eda-0.1.3-py3-none-any.whl",
]

CAPSULE_REQUIRED = {
    "artifact_index.json",
    "run_manifest.json",
    "claim_policy.yaml",
    "validation_report.md",
    "replay_acceptance_report.md",
    "unsupported_ledger.md",
    "README.md",
}

SUPPLEMENTARY_REQUIRED = {
    "README.md",
    "supplementary_manifest.json",
    "reports/GATE_REVIEW.md",
    "paper/MANUSCRIPT_REPRO_PACKAGE.md",
    "paper/manuscript_artifact_manifest.csv",
    "paper/figures/architecture.png",
    "paper/figures/workflow.png",
    "paper/figures/evidence_levels.png",
    "paper/figures/experiment_matrix.png",
}


def text_files() -> list[Path]:
    files: list[Path] = []
    for item in SOURCE_DIRS:
        path = ROOT / item
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    return sorted(files)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def check_private_paths(errors: list[str]) -> None:
    for path in text_files():
        rel = path.relative_to(ROOT).as_posix()
        if "__pycache__" in path.parts:
            continue
        if PRIVATE_PATH_RE.search(read_text(path)):
            errors.append(f"private path found in {rel}")


def check_resource_forks(errors: list[str]) -> None:
    forks = list(ROOT.rglob("._*"))
    if forks:
        errors.append(f"macOS resource fork files found: {len(forks)}")


def check_wording_context(errors: list[str]) -> None:
    lower_patterns = [pattern.lower() for pattern in FORBIDDEN_PATTERNS]
    for path in text_files():
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path).lower()
        if not text:
            continue
        if rel.startswith(ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        for pattern in lower_patterns:
            start = 0
            while True:
                index = text.find(pattern, start)
                if index == -1:
                    break
                if rel in LINE_SCOPED_FORBIDDEN_CONTEXTS and is_boundary_context(text, index):
                    start = index + len(pattern)
                    continue
                line_no = text.count("\n", 0, index) + 1
                errors.append(f"forbidden wording outside allowed context: {rel}:{line_no} ({pattern})")
                start = index + len(pattern)


def is_boundary_context(text: str, index: int) -> bool:
    window = text[max(0, index - 220) : min(len(text), index + 220)]
    return any(marker in window for marker in BOUNDARY_CONTEXT_MARKERS)


def check_zip(path: Path, required: set[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing release zip: {path.relative_to(ROOT).as_posix()}")
        return
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
    missing = sorted(required - names)
    if missing:
        errors.append(f"{path.relative_to(ROOT).as_posix()} missing {missing}")


def check_release_zips(errors: list[str]) -> None:
    for rel in RELEASE_ZIPS[:3]:
        check_zip(ROOT / rel, CAPSULE_REQUIRED, errors)
    check_zip(ROOT / RELEASE_ZIPS[3], SUPPLEMENTARY_REQUIRED, errors)
    for rel in RELEASE_ZIPS + OPTIONAL_RELEASE_ZIPS:
        path = ROOT / rel
        if path.exists():
            check_zip_private_paths(path, errors)
    check_ist_zip(errors)


def check_zip_private_paths(path: Path, errors: list[str]) -> None:
    rel_zip = path.relative_to(ROOT).as_posix()
    with zipfile.ZipFile(path) as zip_handle:
        for member in zip_handle.namelist():
            if member.endswith("/") or (rel_zip, member) in ZIP_PRIVATE_PATH_ALLOWLIST:
                continue
            if PRIVATE_PATH_PAYLOAD_RE.search(zip_handle.read(member)):
                errors.append(f"private path payload found in {rel_zip}:{member}")


def check_ist_zip(errors: list[str]) -> None:
    rel = "release/artifactgate_eda_ist_evaluation_artifacts.zip"
    path = ROOT / rel
    if not path.exists():
        if any((ROOT / marker).exists() for marker in IST_MODE_MARKERS):
            errors.append(f"missing IST evaluation zip: {rel}")
        return
    with zipfile.ZipFile(path) as zip_handle:
        bad_member = zip_handle.testzip()
        names = set(zip_handle.namelist())
    if bad_member:
        errors.append(f"{rel} corrupt member: {bad_member}")
    missing = sorted(IST_ZIP_REQUIRED - names)
    if missing:
        errors.append(f"{rel} missing IST workflow artifacts: {missing}")
    forbidden = sorted(IST_ZIP_FORBIDDEN & names)
    if forbidden:
        errors.append(f"{rel} contains full external plan snapshot: {forbidden}")
    for optional_set in IST_ZIP_OPTIONAL_COMPLETE_SETS:
        present = sorted(optional_set & names)
        missing_optional = sorted(optional_set - names)
        if present and missing_optional:
            errors.append(f"{rel} contains partial optional artifact set: present {present}; missing {missing_optional}")
    resource_forks = sorted(
        name for name in names if name.startswith("__MACOSX/") or name.startswith("._") or "/._" in name
    )
    if resource_forks:
        errors.append(f"{rel} contains macOS resource fork entries: {resource_forks[:5]}")


def check_dist_files(errors: list[str]) -> None:
    for rel in DIST_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing Python distribution artifact: {rel}")


def main() -> int:
    errors: list[str] = []
    check_resource_forks(errors)
    check_private_paths(errors)
    check_wording_context(errors)
    check_release_zips(errors)
    check_dist_files(errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("release preflight: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
