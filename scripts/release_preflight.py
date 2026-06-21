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

ALLOWED_FORBIDDEN_CONTEXTS = (
    "repo/src/artifactgate_eda/policies/",
    "examples/negative_claim_cases/",
    "examples/corrupted_artifact_cases/",
    "examples/ngspice_circuitfaultbench_sample/unsupported_ledger.md",
    "examples/hdl_icarus_yosys_minimal/unsupported_ledger.md",
    "supplementary/cfb_full_artifact_tables/unsupported_ledger.md",
    "supplementary/spec2dfx_full_artifact_tables/unsupported_ledger.md",
    "README.md",
    "paper/softwarex_manuscript.md",
    "paper/softwarex_manuscript.tex",
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

DIST_FILES = [
    "dist/artifactgate_eda-0.1.1.tar.gz",
    "dist/artifactgate_eda-0.1.1-py3-none-any.whl",
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
        if any(pattern in text for pattern in lower_patterns) and not rel.startswith(ALLOWED_FORBIDDEN_CONTEXTS):
            errors.append(f"forbidden wording outside allowed context: {rel}")


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
