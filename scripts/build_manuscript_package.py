from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_row(path: Path, role: str, command: str) -> dict[str, str]:
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "role": role,
        "sha256": sha256(path),
        "rebuild_command": command,
    }


def main() -> int:
    rows: list[dict[str, str]] = []
    for path in [ROOT / "paper" / "softwarex_manuscript.md", ROOT / "paper" / "softwarex_manuscript.tex"]:
        if path.exists():
            rows.append(file_row(path, "manuscript_source", "manual edit, then make manuscript-package"))
    for path in sorted((ROOT / "paper" / "figures").glob("*.png")):
        rows.append(file_row(path, "generated_figure", "make figures"))
    for path in sorted((ROOT / "reports").glob("e*_*.csv")) + sorted((ROOT / "reports").glob("e*_*.md")):
        rows.append(file_row(path, "generated_report", "make reproduce-all"))
    out = ROOT / "paper" / "MANUSCRIPT_REPRO_PACKAGE.md"
    lines = [
        "# Manuscript Reproducibility Package",
        "",
        "## Rebuild Commands",
        "",
        "```bash",
        "make install",
        "make reproduce-all",
        "make package-release",
        "```",
        "",
        "## Artifact Map",
        "",
        "| file | role | sha256 | rebuild_command |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['file']} | {row['role']} | `{row['sha256']}` | `{row['rebuild_command']}` |")
    lines += [
        "",
        "## Claim-Evidence Boundary",
        "",
        "The manuscript package is limited to software-only artifact evidence. Reports under `reports/` are generated from local CLI/Makefile commands and do not provide hardware, vendor implementation, bitstream, or board-measurement evidence.",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    csv_path = ROOT / "paper" / "manuscript_artifact_manifest.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "role", "sha256", "rebuild_command"])
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
