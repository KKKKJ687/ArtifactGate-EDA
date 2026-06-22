from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT = "reports/g13_author_expert_walkthrough.md"
OBSERVATIONS = "reports/g13_author_expert_walkthrough_observations.csv"
COMMAND_LOG = "reports/g13_author_expert_walkthrough_command_log.csv"

REQUIRED_OBSERVATION_COLUMNS = {
    "walkthrough_id",
    "evaluator_id",
    "evaluator_role",
    "review_date_utc",
    "condition",
    "task_id",
    "decision",
    "observed_success",
    "elapsed_seconds",
    "evidence_file",
    "hardware_claim_made",
    "attestation_signed",
}
REQUIRED_COMMAND_COLUMNS = {"step", "command", "started_at_utc", "finished_at_utc", "status"}
REQUIRED_CONDITIONS = {"manual_package", "artifactgate_package"}
REQUIRED_TASKS = {f"T{index}" for index in range(1, 9)}
REQUIRED_COMMANDS = {
    "make rq10-reviewer-walkthrough",
    "make ist-package",
    "make ist-strong-l2",
}
ALLOWED_STUDY_TYPES = {"single_expert_walkthrough", "participant_study"}
ALLOWED_TIMING_BASIS = {"directly_measured", "not_measured"}
BOUNDARY_CONTEXT_MARKERS = (
    "cannot",
    "does not",
    "do not",
    "must not",
    "no ",
    "not ",
    "not claimed",
    "not evidence",
    "not imply",
    "unsupported",
    "boundary",
    "limitation",
)
FORBIDDEN_POSITIVE_PATTERNS = (
    "hardware validation",
    "board validation",
    "dfx deployment",
    "vivado timing closure",
    "vivado implementation evidence",
    "full bitstream generated",
    "partial bitstream generated",
    "bitstream verified",
    "real fpga speedup",
    "energy saving measured",
    "external eda execution",
    "independent external eda execution",
)


def as_bool(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])


def parse_attestation(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {
            "evaluator_id",
            "evaluator_role",
            "review_date_utc",
            "study_type",
            "timing_basis",
            "hardware_claim_made",
            "attestation_signed",
        }:
            fields[key] = value.strip()
    return fields


def add_check(checks: list[dict[str, str]], name: str, status: str, detail: str) -> None:
    checks.append({"name": name, "status": status, "detail": detail})


def is_boundary_context(text: str, index: int) -> bool:
    window = text[max(0, index - 220) : min(len(text), index + 220)]
    return any(marker in window for marker in BOUNDARY_CONTEXT_MARKERS)


def find_positive_boundary_claims(text: str, source: str) -> list[str]:
    findings: list[str] = []
    lowered = text.lower()
    for pattern in FORBIDDEN_POSITIVE_PATTERNS:
        start = 0
        while True:
            index = lowered.find(pattern, start)
            if index == -1:
                break
            if not is_boundary_context(lowered, index):
                line_no = lowered.count("\n", 0, index) + 1
                findings.append(f"{source}:{line_no}:{pattern}")
            start = index + len(pattern)
    return findings


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def display_missing_path(path: Path) -> str:
    if path.parent.name == "reports":
        return display_path(path, path.parent.parent)
    return path.as_posix()


def is_nonportable_path(value: str) -> bool:
    normalized = value.strip()
    return (
        Path(normalized).is_absolute()
        or normalized.startswith("~")
        or normalized.startswith("C:\\")
        or normalized.startswith("c:\\")
        or "/Users/" in normalized
        or "\\Users\\" in normalized
    )


def validate_report(path: Path, checks: list[dict[str, str]]) -> dict[str, str]:
    if not path.exists():
        add_check(checks, "report_exists", "BLOCKED", display_missing_path(path))
        return {}
    text = path.read_text(encoding="utf-8")
    fields = parse_attestation(text)
    positive_boundary_claims = find_positive_boundary_claims(text, REPORT)
    if positive_boundary_claims:
        add_check(
            checks,
            "report_positive_boundary_claims",
            "BLOCKED",
            f"claims: {', '.join(positive_boundary_claims)}",
        )
    else:
        add_check(checks, "report_positive_boundary_claims", "PASS", "no positive boundary claims")

    missing = [
        key
        for key in [
            "evaluator_id",
            "evaluator_role",
            "review_date_utc",
            "study_type",
            "timing_basis",
            "hardware_claim_made",
            "attestation_signed",
        ]
        if not fields.get(key)
    ]
    if missing:
        add_check(checks, "report_attestation", "BLOCKED", f"missing: {', '.join(missing)}")
    else:
        add_check(checks, "report_attestation", "PASS", "required attestation fields present")

    if fields.get("study_type") and fields["study_type"] not in ALLOWED_STUDY_TYPES:
        add_check(checks, "study_type", "BLOCKED", fields["study_type"])
    elif fields.get("study_type"):
        add_check(checks, "study_type", "PASS", fields["study_type"])

    if fields.get("timing_basis") and fields["timing_basis"] not in ALLOWED_TIMING_BASIS:
        add_check(checks, "timing_basis", "BLOCKED", fields["timing_basis"])
    elif fields.get("timing_basis"):
        add_check(checks, "timing_basis", "PASS", fields["timing_basis"])

    hardware_claim = as_bool(fields.get("hardware_claim_made", ""))
    if hardware_claim is not False:
        add_check(checks, "report_hardware_claim", "BLOCKED", "hardware_claim_made must be false")
    else:
        add_check(checks, "report_hardware_claim", "PASS", "false")

    signed = as_bool(fields.get("attestation_signed", ""))
    if signed is not True:
        add_check(checks, "report_attestation_signed", "BLOCKED", "attestation_signed must be true")
    else:
        add_check(checks, "report_attestation_signed", "PASS", "true")

    return fields


def validate_observations(
    path: Path,
    report_fields: dict[str, str],
    checks: list[dict[str, str]],
    root: Path,
) -> None:
    if not path.exists():
        add_check(checks, "observations_exists", "BLOCKED", display_missing_path(path))
        return
    rows, columns = read_csv(path)
    missing_columns = sorted(REQUIRED_OBSERVATION_COLUMNS - set(columns))
    if missing_columns:
        add_check(checks, "observation_columns", "BLOCKED", f"missing: {', '.join(missing_columns)}")
        return
    add_check(checks, "observation_columns", "PASS", "minimum columns present")

    if not rows:
        add_check(checks, "observation_rows", "BLOCKED", "no rows")
        return

    positive_claim_rows = [
        finding
        for index, row in enumerate(rows, start=2)
        for finding in find_positive_boundary_claims(
            "\n".join(str(value) for value in row.values()),
            f"{OBSERVATIONS}:{index}",
        )
    ]
    if positive_claim_rows:
        add_check(
            checks,
            "observation_positive_boundary_claims",
            "BLOCKED",
            f"claims: {', '.join(positive_claim_rows)}",
        )
    else:
        add_check(checks, "observation_positive_boundary_claims", "PASS", "no positive boundary claims")

    required_value_columns = [
        "walkthrough_id",
        "evaluator_id",
        "evaluator_role",
        "review_date_utc",
        "condition",
        "task_id",
        "decision",
        "observed_success",
        "evidence_file",
    ]
    missing_values = [
        f"{index}:{column}"
        for index, row in enumerate(rows, start=2)
        for column in required_value_columns
        if not row.get(column, "").strip()
    ]
    if missing_values:
        add_check(checks, "observation_required_values", "BLOCKED", f"missing: {', '.join(missing_values)}")
    else:
        add_check(checks, "observation_required_values", "PASS", "required row values present")

    attestation_mismatches = [
        f"{index}:{column}"
        for index, row in enumerate(rows, start=2)
        for column in ["evaluator_id", "evaluator_role", "review_date_utc"]
        if report_fields.get(column) and row.get(column, "").strip() != report_fields[column]
    ]
    if attestation_mismatches:
        add_check(
            checks,
            "observation_attestation_matches_report",
            "BLOCKED",
            f"mismatches: {', '.join(attestation_mismatches)}",
        )
    else:
        add_check(checks, "observation_attestation_matches_report", "PASS", "rows match report attestation")

    walkthrough_ids = {row.get("walkthrough_id", "").strip() for row in rows if row.get("walkthrough_id", "").strip()}
    if len(walkthrough_ids) != 1:
        add_check(
            checks,
            "observation_walkthrough_id",
            "BLOCKED",
            f"expected exactly one nonempty walkthrough_id, found: {', '.join(sorted(walkthrough_ids)) or 'none'}",
        )
    else:
        add_check(checks, "observation_walkthrough_id", "PASS", next(iter(walkthrough_ids)))

    task_pairs = {(row["condition"].strip(), row["task_id"].strip()) for row in rows}
    missing_pairs = sorted(
        f"{condition}:{task}"
        for condition in REQUIRED_CONDITIONS
        for task in REQUIRED_TASKS
        if (condition, task) not in task_pairs
    )
    if missing_pairs:
        add_check(checks, "observation_task_coverage", "BLOCKED", f"missing: {', '.join(missing_pairs)}")
    else:
        add_check(checks, "observation_task_coverage", "PASS", "manual_package and artifactgate_package T1-T8 present")

    duplicate_pairs = sorted(
        f"{condition}:{task_id}"
        for condition, task_id in task_pairs
        if sum(1 for row in rows if row["condition"].strip() == condition and row["task_id"].strip() == task_id) > 1
    )
    if duplicate_pairs:
        add_check(checks, "observation_unique_task_pairs", "BLOCKED", f"duplicates: {', '.join(duplicate_pairs)}")
    else:
        add_check(checks, "observation_unique_task_pairs", "PASS", "exactly one row per listed task pair")

    bad_conditions = sorted({row["condition"].strip() for row in rows} - REQUIRED_CONDITIONS)
    if bad_conditions:
        add_check(checks, "observation_conditions", "BLOCKED", f"unexpected: {', '.join(bad_conditions)}")
    else:
        add_check(checks, "observation_conditions", "PASS", "conditions valid")

    bad_hardware_rows = [
        str(index)
        for index, row in enumerate(rows, start=2)
        if as_bool(row.get("hardware_claim_made", "")) is not False
    ]
    if bad_hardware_rows:
        add_check(checks, "observation_hardware_claims", "BLOCKED", f"rows: {', '.join(bad_hardware_rows)}")
    else:
        add_check(checks, "observation_hardware_claims", "PASS", "all false")

    unsigned_rows = [
        str(index)
        for index, row in enumerate(rows, start=2)
        if as_bool(row.get("attestation_signed", "")) is not True
    ]
    if unsigned_rows:
        add_check(checks, "observation_attestation_signed", "BLOCKED", f"rows: {', '.join(unsigned_rows)}")
    else:
        add_check(checks, "observation_attestation_signed", "PASS", "all true")

    bad_success_rows = [
        str(index)
        for index, row in enumerate(rows, start=2)
        if as_bool(row.get("observed_success", "")) is None
    ]
    if bad_success_rows:
        add_check(checks, "observation_success_values", "BLOCKED", f"rows: {', '.join(bad_success_rows)}")
    else:
        add_check(checks, "observation_success_values", "PASS", "all true or false")

    numeric_timing_rows: list[str] = []
    bad_timing_rows: list[str] = []
    for index, row in enumerate(rows, start=2):
        value = row.get("elapsed_seconds", "").strip()
        if value.upper() == "NA":
            continue
        try:
            elapsed = float(value)
        except ValueError:
            bad_timing_rows.append(str(index))
            continue
        if elapsed < 0:
            bad_timing_rows.append(str(index))
        else:
            numeric_timing_rows.append(str(index))
    if bad_timing_rows:
        add_check(checks, "observation_elapsed_seconds", "BLOCKED", f"invalid rows: {', '.join(bad_timing_rows)}")
    else:
        add_check(checks, "observation_elapsed_seconds", "PASS", "NA or nonnegative numeric values")

    if numeric_timing_rows and report_fields.get("timing_basis") != "directly_measured":
        add_check(
            checks,
            "timing_basis_matches_rows",
            "BLOCKED",
            "numeric elapsed_seconds requires timing_basis: directly_measured",
        )
    else:
        add_check(checks, "timing_basis_matches_rows", "PASS", "timing basis consistent with observations")

    missing_evidence = [
        f"{index}:{row.get('evidence_file', '').strip()}"
        for index, row in enumerate(rows, start=2)
        if not row.get("evidence_file", "").strip()
    ]
    if missing_evidence:
        add_check(checks, "observation_evidence_files", "BLOCKED", f"missing rows: {', '.join(missing_evidence)}")
    else:
        add_check(checks, "observation_evidence_files", "PASS", "all rows list evidence files")

    nonportable_evidence = [
        f"{index}:{row.get('evidence_file', '').strip()}"
        for index, row in enumerate(rows, start=2)
        if row.get("evidence_file", "").strip() and is_nonportable_path(row.get("evidence_file", ""))
    ]
    if nonportable_evidence:
        add_check(
            checks,
            "observation_evidence_paths_portable",
            "BLOCKED",
            f"nonportable rows: {', '.join(nonportable_evidence)}",
        )
    else:
        add_check(checks, "observation_evidence_paths_portable", "PASS", "all evidence paths are portable")

    missing_evidence_paths = [
        f"{index}:{row.get('evidence_file', '').strip()}"
        for index, row in enumerate(rows, start=2)
        if row.get("evidence_file", "").strip()
        and not is_nonportable_path(row.get("evidence_file", ""))
        and not (root / row["evidence_file"].strip()).exists()
    ]
    if missing_evidence_paths:
        add_check(
            checks,
            "observation_evidence_paths_exist",
            "BLOCKED",
            f"missing paths: {', '.join(missing_evidence_paths)}",
        )
    else:
        add_check(checks, "observation_evidence_paths_exist", "PASS", "all evidence paths exist")


def validate_command_log(path: Path, checks: list[dict[str, str]]) -> None:
    if not path.exists():
        add_check(checks, "command_log_exists", "BLOCKED", display_missing_path(path))
        return
    rows, columns = read_csv(path)
    missing_columns = sorted(REQUIRED_COMMAND_COLUMNS - set(columns))
    if missing_columns:
        add_check(checks, "command_log_columns", "BLOCKED", f"missing: {', '.join(missing_columns)}")
        return
    add_check(checks, "command_log_columns", "PASS", "minimum columns present")

    positive_claim_rows = [
        finding
        for index, row in enumerate(rows, start=2)
        for finding in find_positive_boundary_claims(
            "\n".join(str(value) for value in row.values()),
            f"{COMMAND_LOG}:{index}",
        )
    ]
    if positive_claim_rows:
        add_check(
            checks,
            "command_log_positive_boundary_claims",
            "BLOCKED",
            f"claims: {', '.join(positive_claim_rows)}",
        )
    else:
        add_check(checks, "command_log_positive_boundary_claims", "PASS", "no positive boundary claims")

    missing_values = [
        f"{index}:{column}"
        for index, row in enumerate(rows, start=2)
        for column in REQUIRED_COMMAND_COLUMNS
        if not row.get(column, "").strip()
    ]
    if missing_values:
        add_check(checks, "command_log_required_values", "BLOCKED", f"missing: {', '.join(missing_values)}")
    else:
        add_check(checks, "command_log_required_values", "PASS", "required row values present")

    commands = {row["command"].strip() for row in rows}
    missing_commands = sorted(REQUIRED_COMMANDS - commands)
    if missing_commands:
        add_check(checks, "command_log_required_commands", "BLOCKED", f"missing: {', '.join(missing_commands)}")
    else:
        add_check(checks, "command_log_required_commands", "PASS", "required commands present")

    nonpass = [
        f"{index}:{row.get('command', '').strip()}={row.get('status', '').strip()}"
        for index, row in enumerate(rows, start=2)
        if row.get("status", "").strip().upper() != "PASS"
    ]
    if nonpass:
        add_check(checks, "command_log_status", "BLOCKED", f"non-PASS rows: {', '.join(nonpass)}")
    else:
        add_check(checks, "command_log_status", "PASS", "all PASS")


def validate(root: Path = ROOT) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    report_fields = validate_report(root / REPORT, checks)
    validate_observations(root / OBSERVATIONS, report_fields, checks, root)
    validate_command_log(root / COMMAND_LOG, checks)
    blocked = [check for check in checks if check["status"] == "BLOCKED"]
    return {
        "ok": not blocked,
        "status": "PASS" if not blocked else "BLOCKED",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate real G13 author/expert walkthrough evidence.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(ROOT)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"G13 walkthrough validation: {result['status']}")
        for check in result["checks"]:
            print(f"- {check['status']}: {check['name']} - {check['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
