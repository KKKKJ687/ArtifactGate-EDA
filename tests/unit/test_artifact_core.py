import json
from pathlib import Path

from artifactgate_eda.core.artifact import claim_check, ingest_artifacts, validate_artifacts

ROOT = Path(__file__).resolve().parents[2]


def test_ingest_and_validate(tmp_path):
    out = tmp_path / "ingest"
    result = ingest_artifacts(ROOT / "examples" / "ngspice_minimal", "ngspice", out)
    assert result["ok"]
    assert (out / "artifact_index.json").exists()
    validation = validate_artifacts(out / "artifact_index.json")
    assert validation["ok"], validation


def test_claim_check_blocks_negative_claims(tmp_path):
    ingest_out = tmp_path / "ingest"
    ingest_artifacts(ROOT / "examples" / "ngspice_minimal", "ngspice", ingest_out)
    result = claim_check(
        ROOT / "examples" / "negative_claim_cases" / "claims.md",
        ingest_out / "artifact_index.json",
        ROOT / "repo" / "src" / "artifactgate_eda" / "policies" / "forbidden_claims.yaml",
        tmp_path / "claims",
    )
    assert not result["ok"]
    assert result["unsupported_count"] == result["claim_count"]
    report = json.loads((tmp_path / "claims" / "claim_check_report.json").read_text())
    assert report["result"]["unsupported_count"] == report["result"]["claim_count"]
    assert all(row["status"] == "UNSUPPORTED" for row in report["claims"])
