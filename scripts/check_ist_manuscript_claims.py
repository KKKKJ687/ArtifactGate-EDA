#!/usr/bin/env python3
"""Gate IST manuscript claims against the software-only evidence boundary."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import yaml

BOUNDARY_CATEGORIES = {"hardware_overclaim", "vivado_overclaim", "bitstream_overclaim", "dfx_overclaim"}
HIGH_RISK_SECTIONS = {"title", "abstract", "introduction", "results", "discussion"}
ALLOW_TERMS = {
    "does not",
    "do not",
    "not ",
    "no ",
    "without",
    "unsupported",
    "outside",
    "boundary",
    "ceiling",
    "limitation",
    "future",
    "rather than",
}
RQ_RE = re.compile(r"\bRQ([0-9]+)\b")


def normalize_section(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"^[0-9]+(\.[0-9]+)*\s*[\).:-]?\s*", "", lowered)
    return lowered


def load_boundary_patterns(policy: Path) -> list[str]:
    data = yaml.safe_load(policy.read_text(encoding="utf-8")) or {}
    patterns: list[str] = []
    for name in BOUNDARY_CATEGORIES:
        patterns.extend(data.get(name, {}).get("forbidden_patterns", []))
    return sorted(set(patterns), key=str.lower)


def section_for_line(path: Path, line: str, current: str) -> str:
    stripped = line.strip()
    lowered = stripped.lower()
    if path.suffix == ".md":
        if stripped.startswith("# "):
            return "title"
        if stripped.startswith("## "):
            return normalize_section(stripped.lstrip("#").strip().split(":", 1)[0])
        return current
    if lowered.startswith("\\title"):
        return "title"
    if lowered.startswith("\\begin{abstract}"):
        return "abstract"
    if lowered.startswith("\\end{abstract}"):
        return "frontmatter"
    section_match = re.match(r"\\section\{([^}]+)\}", stripped)
    if section_match:
        return normalize_section(section_match.group(1))
    return current


def allowed_line(line: str) -> bool:
    lowered = line.lower()
    return any(term in lowered for term in ALLOW_TERMS)


def report_refs_near(lines: list[str], index: int) -> bool:
    window = "\n".join(lines[index : min(index + 3, len(lines))])
    return "reports/" in window or "reports\\" in window


def scan_file(path: Path, patterns: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, str]] = []
    rq_rows: list[dict[str, str]] = []
    section = "frontmatter"
    compiled = [(pattern, re.compile(re.escape(pattern), re.IGNORECASE)) for pattern in patterns]
    for index, line in enumerate(lines):
        section = section_for_line(path, line, section)
        high_risk = section in HIGH_RISK_SECTIONS
        for pattern, regex in compiled:
            if not regex.search(line):
                continue
            status = "ALLOWED" if allowed_line(line) or not high_risk else "VIOLATION"
            rows.append(
                {
                    "file": path.as_posix(),
                    "line_no": str(index + 1),
                    "section": section,
                    "matched_term": pattern,
                    "context": line.strip()[:240],
                    "status": status,
                }
            )
        if section == "results" and RQ_RE.search(line):
            has_report_ref = report_refs_near(lines, index)
            rq_rows.append(
                {
                    "file": path.as_posix(),
                    "line_no": str(index + 1),
                    "section": section,
                    "matched_term": "RQ_RESULT_REPORT_REFERENCE",
                    "context": line.strip()[:240],
                    "status": "ALLOWED" if has_report_ref else "VIOLATION",
                }
            )
    return rows, rq_rows


def write_markdown(path: Path, rows: list[dict[str, str]], rq_rows: list[dict[str, str]]) -> None:
    violations = [row for row in rows + rq_rows if row["status"] == "VIOLATION"]
    lines = [
        "# IST Manuscript Claim Gate",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| boundary term hits | {len(rows)} |",
        f"| RQ result reference checks | {len(rq_rows)} |",
        f"| violations | {len(violations)} |",
        "",
    ]
    if violations:
        lines.extend(["## Violations", "", "| File | Line | Section | Issue | Context |", "|---|---:|---|---|---|"])
        for row in violations:
            context = row["context"].replace("|", "\\|")
            lines.append(f"| {row['file']} | {row['line_no']} | {row['section']} | {row['matched_term']} | {context} |")
    else:
        lines.append("No forbidden positive hardware/Vivado/DFX/bitstream/board claims were found.")
        lines.append("All detected RQ result claims in the Results section have nearby report references.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscripts", nargs="*", default=["paper/manuscript_ist.md", "paper/manuscript_ist.tex"])
    parser.add_argument("--policy", default="repo/src/artifactgate_eda/policies/forbidden_claims.yaml")
    parser.add_argument("--out", default="reports/ist_manuscript_claim_gate.md")
    args = parser.parse_args()

    policy = Path(args.policy)
    patterns = load_boundary_patterns(policy)
    all_rows: list[dict[str, str]] = []
    rq_rows: list[dict[str, str]] = []
    for manuscript in args.manuscripts:
        path = Path(manuscript)
        if not path.exists():
            continue
        boundary, rq = scan_file(path, patterns)
        all_rows.extend(boundary)
        rq_rows.extend(rq)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(out, all_rows, rq_rows)
    csv_out = out.with_suffix(".csv")
    with csv_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "line_no", "section", "matched_term", "context", "status"])
        writer.writeheader()
        writer.writerows(all_rows + rq_rows)
    violations = sum(1 for row in all_rows + rq_rows if row["status"] == "VIOLATION")
    print(f"IST manuscript claim gate: {violations} violations -> {out}")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
