#!/usr/bin/env python3
"""Scan repository text for forbidden claim-boundary wording."""

from __future__ import annotations

import argparse
import csv
import os
import re
from pathlib import Path

import yaml

EXCLUDED_DIRS = {".git", ".venv", "__MACOSX", ".pytest_cache", ".ruff_cache", "__pycache__", "build"}
EXCLUDED_FILES = {
    "reports/claim_boundary_scan.csv",
    "reports/evidence_graph_edges.csv",
    "reports/evidence_graph_nodes.csv",
    "reports/file_inventory_full.csv",
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
CONTEXT_ALLOW_TERMS = {
    "allowed",
    "boundary",
    "ceiling",
    "do not",
    "does not",
    "forbidden",
    "limitation",
    "negative",
    "never",
    "no ",
    "not ",
    "outside",
    "policy",
    "safe rewrite",
    "unsupported",
    "without",
}
BOUNDARY_CATEGORIES = {"hardware_overclaim", "vivado_overclaim", "bitstream_overclaim", "dfx_overclaim"}


def load_patterns(policy: Path | None) -> list[str]:
    if policy is None:
        return []
    data = yaml.safe_load(policy.read_text(encoding="utf-8")) or {}
    patterns: list[str] = []
    for name in BOUNDARY_CATEGORIES:
        patterns.extend(data.get(name, {}).get("forbidden_patterns", []))
    return sorted(set(patterns), key=str.lower)


def iter_text_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        dirnames[:] = [d for d in sorted(dirnames) if d not in EXCLUDED_DIRS]
        for filename in sorted(filenames):
            path = current_path / filename
            rel = path.relative_to(root).as_posix()
            if rel in EXCLUDED_FILES:
                continue
            if path.suffix.lower() in TEXT_EXTENSIONS:
                paths.append(path)
    return paths


def allowed_context(rel: str, window: str) -> tuple[str, str]:
    lowered_path = rel.lower()
    lowered_window = window.lower()
    if "policies/" in lowered_path or "forbidden_claims" in lowered_path:
        return "policy definition", "ALLOWED"
    if lowered_path.endswith("claim_policy.yaml"):
        return "policy definition", "ALLOWED"
    if any(
        token in lowered_path
        for token in ("negative_claim", "claimbench", "claim_check_report", "corrupted_artifact")
    ):
        return "negative claim test case", "ALLOWED"
    if lowered_path.startswith("tests/"):
        return "test fixture for boundary rejection", "ALLOWED"
    if "unsupported_ledger" in lowered_path:
        return "unsupported ledger", "ALLOWED"
    if "current_pack_audit" in lowered_path or "boundary" in lowered_path:
        return "research boundary record", "ALLOWED"
    if lowered_path.startswith("scripts/"):
        return "tooling rule definition", "ALLOWED"
    if lowered_path.startswith("docs/") and any(
        token in lowered_path for token in ("claim", "schema", "reproducibility", "api", "adapter")
    ):
        return "documentation of boundary checks", "ALLOWED"
    if lowered_path == "agents.md":
        return "repository boundary rule", "ALLOWED"
    if any(token in lowered_path for token in ("agents.md", "readme.md", "todo.md", "gap_audit", "claim_policy")):
        if any(term in lowered_window for term in CONTEXT_ALLOW_TERMS):
            return "limitation or boundary section", "ALLOWED"
    if any(term in lowered_window for term in CONTEXT_ALLOW_TERMS):
        return "limitation or safe rewrite context", "ALLOWED"
    return "positive or ambiguous context", "LEAK"


def scan(root: Path, patterns: list[str]) -> list[dict[str, str]]:
    compiled = [(pattern, re.compile(re.escape(pattern), re.IGNORECASE)) for pattern in patterns]
    rows: list[dict[str, str]] = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="latin-1").splitlines()
        for line_no, line in enumerate(lines, start=1):
            for pattern, regex in compiled:
                if not regex.search(line):
                    continue
                window = "\n".join(lines[max(0, line_no - 3) : min(len(lines), line_no + 2)])
                context, status = allowed_context(rel, window)
                rows.append(
                    {
                        "file": rel,
                        "path": rel,
                        "line_no": str(line_no),
                        "matched_term": pattern,
                        "context": line.strip()[:240],
                        "allowed_context": context,
                        "status": status,
                    }
                )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--policy", default="repo/src/artifactgate_eda/policies/forbidden_claims.yaml")
    parser.add_argument("--out", default="reports/claim_boundary_scan.csv")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    patterns = load_patterns(root / args.policy if args.policy else None)
    rows = scan(root, patterns)
    fieldnames = ["file", "path", "line_no", "matched_term", "context", "allowed_context", "status"]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    leaks = sum(1 for row in rows if row["status"] == "LEAK")
    print(f"boundary scan: {len(rows)} hits, {leaks} leaks -> {out}")
    return 1 if leaks else 0


if __name__ == "__main__":
    raise SystemExit(main())
