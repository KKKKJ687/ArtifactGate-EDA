from pathlib import Path

from artifactgate_eda.core.artifact import claim_check, validate_artifacts

ROOT = Path(__file__).resolve().parents[2]


def test_absolute_path_rejected():
    result = validate_artifacts(ROOT / "examples" / "corrupted_artifact_cases" / "absolute_path")
    assert not result["ok"]
    assert any(err["code"] == "NON_PORTABLE_PATH" for err in result["errors"])


def test_missing_log_rejected():
    result = validate_artifacts(ROOT / "examples" / "corrupted_artifact_cases" / "missing_log")
    assert not result["ok"]
    assert any(err["code"] == "MISSING_ARTIFACT" for err in result["errors"])


def test_hash_mismatch_rejected():
    result = validate_artifacts(ROOT / "examples" / "corrupted_artifact_cases" / "hash_mismatch")
    assert not result["ok"]
    assert any(err["code"] == "HASH_MISMATCH" for err in result["errors"])


def test_missing_tool_version_rejected():
    result = validate_artifacts(ROOT / "examples" / "corrupted_artifact_cases" / "missing_tool_version")
    assert not result["ok"]
    assert any(err["code"] == "MISSING_TOOL_VERSION" for err in result["errors"])


def test_broken_claim_reference_rejected():
    result = validate_artifacts(ROOT / "examples" / "corrupted_artifact_cases" / "broken_claim_reference")
    assert not result["ok"]
    assert any(err["code"] == "BROKEN_CLAIM_REFERENCE" for err in result["errors"])


def test_simulation_to_hardware_escalation_rejected():
    result = claim_check(
        ROOT / "examples" / "corrupted_artifact_cases" / "simulation_to_hardware_escalation" / "claims.md",
        None,
        ROOT / "repo" / "src" / "artifactgate_eda" / "policies" / "forbidden_claims.yaml",
        None,
    )
    assert not result["ok"]
    assert any(err["code"] == "EVIDENCE_LEVEL_ESCALATION" for err in result["errors"])


def test_yosys_to_vivado_escalation_rejected():
    result = claim_check(
        ROOT / "examples" / "corrupted_artifact_cases" / "yosys_to_vivado_escalation" / "claims.md",
        None,
        ROOT / "repo" / "src" / "artifactgate_eda" / "policies" / "forbidden_claims.yaml",
        None,
    )
    assert not result["ok"]
    assert any(err["code"] == "EVIDENCE_LEVEL_ESCALATION" for err in result["errors"])
