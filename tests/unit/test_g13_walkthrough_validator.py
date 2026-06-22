import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate_g13_walkthrough.py"
SPEC = importlib.util.spec_from_file_location("validate_g13_walkthrough", SCRIPT)
assert SPEC and SPEC.loader
validate_g13 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_g13)


def write_valid_g13(root: Path, *, timing_basis: str = "not_measured", elapsed: str = "NA") -> None:
    (root / "README.md").write_text("# Evidence fixture\n", encoding="utf-8")
    reports = root / "reports"
    reports.mkdir()
    (reports / "g13_author_expert_walkthrough.md").write_text(
        "\n".join(
            [
                "# G13 Author/Expert Walkthrough",
                "",
                "## Attestation",
                "",
                "evaluator_id: EVAL_A",
                "evaluator_role: author",
                "review_date_utc: 2026-06-22T00:00:00Z",
                "study_type: single_expert_walkthrough",
                f"timing_basis: {timing_basis}",
                "hardware_claim_made: false",
                "attestation_signed: true",
                "",
                "Attestation statement:",
                "I performed the listed walkthrough tasks on the listed materials.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    rows = [
        "walkthrough_id,evaluator_id,evaluator_role,review_date_utc,condition,task_id,"
        "decision,observed_success,elapsed_seconds,evidence_file,hardware_claim_made,"
        "attestation_signed,comment"
    ]
    for condition in ["manual_package", "artifactgate_package"]:
        for index in range(1, 9):
            rows.append(
                "G13-001,EVAL_A,author,2026-06-22T00:00:00Z,"
                f"{condition},T{index},reviewed,true,{elapsed},README.md,false,true,"
            )
    (reports / "g13_author_expert_walkthrough_observations.csv").write_text(
        "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    (reports / "g13_author_expert_walkthrough_command_log.csv").write_text(
        "\n".join(
            [
                "step,command,started_at_utc,finished_at_utc,status,notes",
                "1,make rq10-reviewer-walkthrough,2026-06-22T00:00:00Z,2026-06-22T00:01:00Z,PASS,",
                "2,make ist-package,2026-06-22T00:01:00Z,2026-06-22T00:02:00Z,PASS,",
                "3,make ist-strong-l2,2026-06-22T00:02:00Z,2026-06-22T00:03:00Z,PASS,",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def check_status(result, name: str) -> str:
    matches = [check for check in result["checks"] if check["name"] == name]
    assert matches, f"missing check {name}"
    return matches[0]["status"]


def test_valid_g13_walkthrough_passes(tmp_path):
    write_valid_g13(tmp_path)

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "PASS"


def test_missing_g13_files_block(tmp_path):
    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "report_exists") == "BLOCKED"
    assert check_status(result, "observations_exists") == "BLOCKED"
    assert check_status(result, "command_log_exists") == "BLOCKED"


def test_hardware_claim_in_observation_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(",false,true,", ",true,true,", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_hardware_claims") == "BLOCKED"


def test_positive_boundary_claim_in_report_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text + "\nThe walkthrough demonstrates hardware validation.\n", encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "report_positive_boundary_claims") == "BLOCKED"


def test_report_boundary_limitation_passes(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text + "\nThis walkthrough does not imply hardware validation.\n", encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "PASS"


def test_positive_boundary_claim_in_observation_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("false,true,", "false,true,hardware validation completed", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_positive_boundary_claims") == "BLOCKED"


def test_positive_boundary_claim_in_command_log_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_command_log.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("PASS,", "PASS,board validation completed", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "command_log_positive_boundary_claims") == "BLOCKED"


def test_numeric_timing_requires_direct_measurement_basis(tmp_path):
    write_valid_g13(tmp_path, timing_basis="not_measured", elapsed="12.5")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "timing_basis_matches_rows") == "BLOCKED"


def test_numeric_timing_passes_when_directly_measured(tmp_path):
    write_valid_g13(tmp_path, timing_basis="directly_measured", elapsed="12.5")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "PASS"


def test_missing_task_pair_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    lines = path.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if ",artifactgate_package,T8," not in line]
    path.write_text("\n".join(filtered) + "\n", encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_task_coverage") == "BLOCKED"


def test_duplicate_task_pair_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    lines = path.read_text(encoding="utf-8").splitlines()
    duplicate = next(line for line in lines if ",artifactgate_package,T8," in line)
    path.write_text("\n".join(lines + [duplicate]) + "\n", encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_unique_task_pairs") == "BLOCKED"


def test_empty_observation_decision_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(",reviewed,true,", ",,true,", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_required_values") == "BLOCKED"


def test_observation_attestation_mismatch_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("G13-001,EVAL_A,author", "G13-001,EVAL_B,author", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_attestation_matches_report") == "BLOCKED"


def test_multiple_walkthrough_ids_block(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("G13-001,EVAL_A", "G13-002,EVAL_A", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_walkthrough_id") == "BLOCKED"


def test_missing_evidence_path_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("README.md", "missing_evidence.md", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_evidence_paths_exist") == "BLOCKED"


def test_absolute_evidence_path_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_observations.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("README.md", "/Users/example/private/evidence.md", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "observation_evidence_paths_portable") == "BLOCKED"


def test_missing_required_command_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_command_log.csv"
    lines = path.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if "make ist-package" not in line]
    path.write_text("\n".join(filtered) + "\n", encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "command_log_required_commands") == "BLOCKED"


def test_missing_command_timestamp_blocks(tmp_path):
    write_valid_g13(tmp_path)
    path = tmp_path / "reports" / "g13_author_expert_walkthrough_command_log.csv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("2026-06-22T00:00:00Z", "", 1), encoding="utf-8")

    result = validate_g13.validate(tmp_path)

    assert result["status"] == "BLOCKED"
    assert check_status(result, "command_log_required_values") == "BLOCKED"
