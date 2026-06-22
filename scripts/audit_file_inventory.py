#!/usr/bin/env python3
"""Build a reproducible repository file inventory for the IST audit layer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__MACOSX",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "__pycache__",
    "htmlcov",
    "build",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
GENERATED_AUDIT_OUTPUTS = {
    "reports/claim_boundary_scan.csv",
    "reports/evidence_graph_edges.csv",
    "reports/evidence_graph_nodes.csv",
    "reports/file_inventory_full.csv",
    "reports/file_inventory_private_paths.csv",
    "reports/ist_manuscript_claim_gate.csv",
}
TEXT_EXTENSIONS = {
    ".bib",
    ".cff",
    ".cir",
    ".csv",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rpt",
    ".tex",
    ".txt",
    ".v",
    ".yaml",
    ".yml",
    ".ys",
}
PRIVATE_PATH_RE = re.compile(r"(/Users/[^\s'\"`,;:]+|C:\\Users\\[^\s'\"`,;:]+)")
BOUNDARY_RE = re.compile(
    r"\b("
    r"hardware validation|validated on FPGA|board-level|board validation|Vivado timing|"
    r"Vivado implementation|DFX deployment|partial reconfiguration|bitstream|"
    r"FPGA speedup|energy saving measured|industrial deployment|universal EDA framework"
    r")\b",
    re.IGNORECASE,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def posix_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_admissible_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        dirnames[:] = [d for d in sorted(dirnames) if d not in EXCLUDED_DIRS]
        for filename in sorted(filenames):
            path = current_path / filename
            if path.suffix in EXCLUDED_SUFFIXES:
                continue
            files.append(path)
    return files


def git_tracked_files(root: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {item for item in result.stdout.decode("utf-8", "replace").split("\0") if item}


def release_entries(root: Path) -> set[str]:
    entries: set[str] = set()
    for archive in sorted((root / "release").glob("*.zip")):
        try:
            with zipfile.ZipFile(archive) as zip_handle:
                for name in zip_handle.namelist():
                    clean = name.strip("/")
                    if not clean or clean.endswith("/"):
                        continue
                    entries.add(clean)
                    parts = clean.split("/")
                    for index in range(len(parts)):
                        entries.add("/".join(parts[index:]))
        except zipfile.BadZipFile:
            entries.add(archive.relative_to(root).as_posix())
    return entries


def role_for(rel: str, suffix: str) -> str:
    name = Path(rel).name.lower()
    if rel.startswith(("release/", "dist/")) or suffix in {".zip", ".whl", ".gz"}:
        return "release_archive"
    if "policy" in rel or rel.startswith("repo/src/artifactgate_eda/policies/"):
        return "policy"
    if "schema" in rel or rel.startswith("repo/src/artifactgate_eda/schemas/"):
        return "schema"
    if "manifest" in name or "artifact_index" in name or rel.endswith(".cff") or rel == "codemeta.json":
        return "manifest"
    if suffix == ".log":
        return "raw_log"
    if rel.startswith("reports/"):
        return "report"
    if rel.startswith("paper/"):
        return "paper_asset"
    if rel.startswith(("outputs/", "dist/")):
        return "derived_result"
    if rel.startswith("examples/"):
        if suffix in {".csv", ".json", ".md"} and any(token in name for token in ("result", "report", "ledger")):
            return "derived_result"
        return "input_artifact"
    if rel.startswith(("repo/src/", "tests/", "scripts/", ".github/")) or suffix in {".py", ".v", ".ys"}:
        return "source"
    if rel.startswith("docs/") or suffix in {".md", ".tex"}:
        return "report"
    return "source"


def adapter_for(rel: str) -> str:
    lowered = rel.lower()
    for adapter in ("ngspice", "icarus", "yosys", "verilator", "plecs", "ltspice", "logisim", "vivado"):
        if adapter in lowered:
            return "vivado_stub" if adapter == "vivado" else adapter
    if "hdl" in lowered:
        return "hdl_generic"
    return ""


def evidence_level_for(rel: str, suffix: str, role: str) -> str:
    lowered = rel.lower()
    if "vivado" in lowered or "schema_boundary" in lowered:
        return "L0_METADATA"
    if "seed" in lowered or "testbench" in lowered or lowered.endswith(".seed.json"):
        return "L2_REFERENCE_OR_INTERFACE"
    if role in {"policy", "schema", "manifest", "report", "paper_asset", "release_archive"}:
        return "L0_METADATA"
    if suffix in {".v", ".ys", ".cir", ".asc", ".plecs", ".circ"}:
        return "L1_SOURCE_EXISTS"
    if suffix == ".log" or "simulation" in lowered or "vvp" in lowered:
        return "L3_SIMULATION"
    if "yosys" in lowered or "synthesis" in lowered or lowered.endswith(".rpt"):
        return "L4_SYNTHESIS"
    if suffix in {".csv", ".json"} and role in {"derived_result", "raw_log"}:
        return "L3_SIMULATION"
    return "L0_METADATA"


def claim_binding_for(rel: str) -> str:
    lowered = rel.lower()
    if any(token in lowered for token in ("claim", "unsupported", "evidence", "policy", "manuscript")):
        return "claim_related"
    return ""


def generated_by_for(rel: str, role: str) -> str:
    if rel.startswith("outputs/"):
        return "artifactgate_cli"
    if rel.startswith("reports/"):
        return "make_or_artifactgate_report"
    if rel.startswith("paper/figures/"):
        return "paper_figure_generation"
    if rel.startswith("release/"):
        return "release_packaging"
    if role == "release_archive":
        return "packaging_tool"
    return "source_tree"


def scan_text_flags(path: Path, rel: str) -> tuple[list[dict[str, str]], int]:
    if rel in GENERATED_AUDIT_OUTPUTS:
        return [], 0
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return [], 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        try:
            lines = path.read_text(encoding="latin-1").splitlines()
        except OSError:
            return [], 0
    except OSError:
        return [], 0
    private_rows: list[dict[str, str]] = []
    boundary_count = 0
    for line_no, line in enumerate(lines, start=1):
        boundary_count += len(BOUNDARY_RE.findall(line))
        for match in PRIVATE_PATH_RE.findall(line):
            allowed_context, status = private_path_context(rel, line)
            private_rows.append(
                {
                    "relative_path": rel,
                    "line_no": str(line_no),
                    "matched_path": match,
                    "context": line.strip()[:240],
                    "allowed_context": allowed_context,
                    "status": status,
                }
            )
    return private_rows, boundary_count


def private_path_context(rel: str, line: str) -> tuple[str, str]:
    lowered = rel.lower()
    if lowered.startswith("scripts/") and "private_path_re" in line.lower():
        return "tooling regex pattern", "ALLOWED"
    if "corrupted_artifact_cases/absolute_path" in lowered:
        return "negative portability fixture", "ALLOWED"
    if "corrupted_artifact_cases_extended/d24" in lowered:
        return "negative portability fixture", "ALLOWED"
    if "non_portable_path" in line.lower() or "absolute_path" in lowered:
        return "negative portability context", "ALLOWED"
    return "portable artifact leak", "LEAK"


def write_counter_csv(path: Path, header: tuple[str, str], counter: Counter[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for key, count in sorted(counter.items()):
            writer.writerow([key, count])


def write_summary(path: Path, rows: list[dict[str, str]], private_rows: list[dict[str, str]], boundary_hits: int) -> None:
    roles = Counter(row["role"] for row in rows)
    extensions = Counter(row["extension"] or "[none]" for row in rows)
    hash_coverage = sum(1 for row in rows if row["sha256"]) / max(len(rows), 1)
    role_coverage = sum(1 for row in rows if row["role"]) / max(len(rows), 1)
    evidence_coverage = sum(1 for row in rows if row["evidence_level"]) / max(len(rows), 1)
    tracked = sum(1 for row in rows if row["tracked_in_git"] == "yes")
    in_release = sum(1 for row in rows if row["inside_release_package"] == "yes")
    private_leaks = sum(1 for row in private_rows if row["status"] == "LEAK")
    lines = [
        "# File Inventory Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| admissible files | {len(rows)} |",
        f"| git tracked files | {tracked} |",
        f"| files present in release archives | {in_release} |",
        f"| hash coverage | {hash_coverage:.3f} |",
        f"| role coverage | {role_coverage:.3f} |",
        f"| evidence-level coverage | {evidence_coverage:.3f} |",
        f"| private absolute path hits | {len(private_rows)} |",
        f"| private absolute path leaks | {private_leaks} |",
        f"| claim-boundary term hits | {boundary_hits} |",
        "",
        "## Roles",
        "",
        "| Role | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {role} | {count} |" for role, count in sorted(roles.items()))
    lines.extend(["", "## Extensions", "", "| Extension | Count |", "|---|---:|"])
    lines.extend(f"| {extension} | {count} |" for extension, count in sorted(extensions.items()))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_inventory(root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], int]:
    tracked = git_tracked_files(root)
    release_index = release_entries(root)
    rows: list[dict[str, str]] = []
    private_rows: list[dict[str, str]] = []
    boundary_hits = 0
    for index, path in enumerate(iter_admissible_files(root), start=1):
        rel = posix_rel(path, root)
        suffix = path.suffix.lower()
        role = role_for(rel, suffix)
        adapter = adapter_for(rel)
        evidence = evidence_level_for(rel, suffix, role)
        path_private_rows, boundary_count = scan_text_flags(path, rel)
        private_rows.extend(path_private_rows)
        boundary_hits += boundary_count
        rows.append(
            {
                "file_id": f"F{index:05d}",
                "relative_path": rel,
                "extension": suffix,
                "size_bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
                "role": role,
                "adapter": adapter,
                "evidence_level": evidence,
                "claim_binding": claim_binding_for(rel),
                "generated_by": generated_by_for(rel, role),
                "tracked_in_git": "yes" if rel in tracked else "no",
                "inside_release_package": "yes" if rel in release_index else "no",
            }
        )
    return rows, private_rows, boundary_hits


def write_private_paths(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["relative_path", "line_no", "matched_path", "context", "allowed_context", "status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root to inventory.")
    parser.add_argument("--out", default="reports/file_inventory_full.csv", help="Inventory CSV path.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)

    rows, private_rows, boundary_hits = build_inventory(root)
    fieldnames = [
        "file_id",
        "relative_path",
        "extension",
        "size_bytes",
        "sha256",
        "role",
        "adapter",
        "evidence_level",
        "claim_binding",
        "generated_by",
        "tracked_in_git",
        "inside_release_package",
    ]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    write_summary(out.with_name("file_inventory_summary.md"), rows, private_rows, boundary_hits)
    write_private_paths(out.with_name("file_inventory_private_paths.csv"), private_rows)
    write_counter_csv(
        out.with_name("file_inventory_by_extension.csv"),
        ("extension", "count"),
        Counter(row["extension"] or "[none]" for row in rows),
    )
    write_counter_csv(out.with_name("file_inventory_by_role.csv"), ("role", "count"), Counter(row["role"] for row in rows))
    print(f"indexed {len(rows)} admissible files -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
