from pathlib import Path

from artifactgate_eda.cli import main

ROOT = Path(__file__).resolve().parents[2]


def test_ingest_cli(tmp_path):
    out = tmp_path / "cli_ingest"
    assert main(["ingest", str(ROOT / "examples" / "ngspice_minimal"), "--adapter", "ngspice", "--out", str(out)]) == 0
    assert (out / "artifact_index.json").exists()


def test_claim_check_cli_expected_fail(tmp_path):
    ingest_out = tmp_path / "ingest"
    assert main(["ingest", str(ROOT / "examples" / "ngspice_minimal"), "--adapter", "ngspice", "--out", str(ingest_out)]) == 0
    assert (
        main(
            [
                "claim-check",
                "--claims",
                str(ROOT / "examples" / "negative_claim_cases" / "claims.md"),
                "--artifact-index",
                str(ingest_out / "artifact_index.json"),
                "--out",
                str(tmp_path / "claims"),
                "--expect-fail",
                "UNSUPPORTED_CLAIM",
            ]
        )
        == 0
    )

