#!/usr/bin/env python3
"""Run repeated software-only replay checks for the IST RQ2 gate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import statistics
import time
from pathlib import Path

from artifactgate_eda.core.artifact import replay_case

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("rq2_ngspice_minimal", "ngspice", "examples/ngspice_minimal"),
    ("rq2_cfb_sample", "ngspice", "examples/ngspice_circuitfaultbench_sample"),
    ("rq2_icarus", "icarus", "examples/hdl_icarus_yosys_minimal"),
    ("rq2_verilator", "verilator", "examples/hdl_verilator_minimal"),
    ("rq2_yosys", "yosys", "examples/hdl_icarus_yosys_minimal"),
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def artifact_signature(out_dir: Path) -> tuple[int, str]:
    records = json.loads((out_dir / "artifact_index.json").read_text(encoding="utf-8"))
    payload = [
        {
            "artifact_id": record.get("artifact_id", ""),
            "artifact_type": record.get("artifact_type", ""),
            "sha256": record.get("sha256", ""),
            "evidence_level": record.get("evidence_level", ""),
            "unsupported_boundary": record.get("unsupported_boundary", ""),
        }
        for record in records
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return len(records), hashlib.sha256(encoded).hexdigest()


def summarize(rows: list[dict[str, object]], repeats: int) -> list[dict[str, object]]:
    summary_rows = []
    for case, adapter, _root in CASES:
        case_rows = [row for row in rows if row["case"] == case]
        durations = [float(row["duration_s"]) for row in case_rows]
        signatures = {str(row["artifact_signature"]) for row in case_rows}
        passed = sum(1 for row in case_rows if row["status"] == "PASS")
        summary_rows.append(
            {
                "case": case,
                "adapter": adapter,
                "required_repeats": repeats,
                "completed_repeats": len(case_rows),
                "passed_repeats": passed,
                "unique_artifact_signatures": len(signatures),
                "drift_detected": "yes" if len(signatures) != 1 else "no",
                "artifact_count": case_rows[0]["artifact_count"] if case_rows else 0,
                "duration_mean_s": f"{statistics.mean(durations):.6g}" if durations else "0",
                "duration_max_s": f"{max(durations):.6g}" if durations else "0",
                "hardware_dependency": "0",
                "status": "PASS" if passed == repeats and len(signatures) == 1 else "FAIL",
            }
        )
    return summary_rows


def write_markdown(summary_rows: list[dict[str, object]], docker_rows: list[dict[str, object]], path: Path) -> None:
    lines = [
        "# RQ2 Replay Repeatability",
        "",
        "| case | adapter | completed_repeats | passed_repeats | unique_artifact_signatures | drift_detected | artifact_count | status |",
        "|---|---|---:|---:|---:|---|---:|---|",
    ]
    for row in summary_rows:
        lines.append(
            "| {case} | {adapter} | {completed_repeats} | {passed_repeats} | "
            "{unique_artifact_signatures} | {drift_detected} | {artifact_count} | {status} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Docker And CI Status",
            "",
            "| check | status | detail |",
            "|---|---|---|",
        ]
    )
    for row in docker_rows:
        lines.append(f"| {row['check']} | {row['status']} | {row['detail']} |")
    lines.extend(
        [
            "",
            "Docker availability is reported separately. A missing local Docker binary does not create a false Docker pass.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def docker_ci_rows(repo_root: Path) -> list[dict[str, object]]:
    docker = shutil.which("docker")
    ci_path = repo_root / ".github" / "workflows" / "ci.yml"
    ci_text = ci_path.read_text(encoding="utf-8") if ci_path.exists() else ""
    return [
        {
            "check": "local_docker_binary",
            "status": "PASS" if docker else "NOT_RUN_ENVIRONMENT_MISSING",
            "detail": docker or "docker command not found on this machine",
        },
        {
            "check": "ci_workflow_present",
            "status": "PASS" if ci_path.exists() else "FAIL",
            "detail": ".github/workflows/ci.yml" if ci_path.exists() else "missing .github workflow",
        },
        {
            "check": "ci_replay_command_present",
            "status": "PASS" if "reproduce-core" in ci_text or "rq2-replay-core" in ci_text else "FAIL",
            "detail": "CI includes replay/reproduction command" if "reproduce-core" in ci_text or "rq2-replay-core" in ci_text else "CI replay command not found",
        },
    ]


def run_repeats(repeats: int, out_dir: Path, reports_dir: Path) -> int:
    rows: list[dict[str, object]] = []
    for case, adapter, root_rel in CASES:
        root = ROOT / root_rel
        for repeat_index in range(1, repeats + 1):
            repeat_dir = out_dir / case / f"repeat_{repeat_index:02d}"
            start = time.perf_counter()
            result = replay_case(root, adapter, repeat_dir)
            duration = time.perf_counter() - start
            artifact_count, signature = artifact_signature(repeat_dir)
            manifest = json.loads((repeat_dir / "run_manifest.json").read_text(encoding="utf-8"))
            rows.append(
                {
                    "case": case,
                    "adapter": adapter,
                    "repeat_index": repeat_index,
                    "artifact_count": artifact_count,
                    "status": result.get("status", "UNKNOWN"),
                    "hardware_required": manifest.get("hardware_required", ""),
                    "commercial_dependency_required": manifest.get("commercial_dependency_required", ""),
                    "artifact_signature": signature,
                    "manifest_present": (repeat_dir / "run_manifest.json").exists(),
                    "acceptance_report_present": (repeat_dir / "replay_acceptance_report.md").exists(),
                    "validation_report_present": (repeat_dir / "validation_report.json").exists(),
                    "duration_s": f"{duration:.6g}",
                }
            )
    summary_rows = summarize(rows, repeats)
    docker_rows = docker_ci_rows(ROOT)
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_csv(reports_dir / "rq2_replay_repeats.csv", rows)
    write_csv(reports_dir / "rq2_replay_repeat_summary.csv", summary_rows)
    write_csv(reports_dir / "rq2_docker_ci_status.csv", docker_rows)
    write_markdown(summary_rows, docker_rows, reports_dir / "rq2_replay_repeats.md")
    repeat_gate = all(row["status"] == "PASS" for row in summary_rows)
    print(f"replay repeats: {sum(int(row['passed_repeats']) for row in summary_rows)} / {len(CASES) * repeats} passed")
    if not all(row["status"] == "PASS" for row in docker_rows):
        print("docker/ci status includes non-pass rows; see reports/rq2_docker_ci_status.csv")
    return 0 if repeat_gate else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--out", default="outputs/replay_repeats")
    parser.add_argument("--reports", default="reports")
    args = parser.parse_args()
    if args.repeats < 10:
        raise SystemExit("--repeats must be >= 10 for the strong replay gate")
    return run_repeats(args.repeats, Path(args.out), Path(args.reports))


if __name__ == "__main__":
    raise SystemExit(main())
