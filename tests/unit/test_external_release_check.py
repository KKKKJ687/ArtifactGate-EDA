import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "external_release_check.py"
SPEC = importlib.util.spec_from_file_location("external_release_check", SCRIPT)
assert SPEC and SPEC.loader
external_release_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(external_release_check)


def test_check_public_doi_passes_for_matching_zenodo_record(monkeypatch):
    def fake_fetch_json(url, timeout=20):
        assert url == "https://zenodo.org/api/records/123"
        assert timeout == 20
        return {
            "doi": "10.5281/zenodo.123",
            "metadata": {"title": "ArtifactGate-EDA: archived software"},
            "links": {"self_html": "https://zenodo.org/records/123"},
        }, None

    monkeypatch.setattr(external_release_check, "fetch_json", fake_fetch_json)
    checks = []

    external_release_check.check_public_doi(checks, "10.5281/zenodo.123", "KKKKJ687/ArtifactGate-EDA")

    assert checks == [
        {
            "name": "zenodo_record",
            "status": "PASS",
            "detail": "https://zenodo.org/records/123 (ArtifactGate-EDA: archived software)",
        }
    ]


def test_check_public_doi_blocks_non_zenodo_doi():
    checks = []

    external_release_check.check_public_doi(checks, "10.9999/example.123", "KKKKJ687/ArtifactGate-EDA")

    assert checks[0]["name"] == "zenodo_record"
    assert checks[0]["status"] == "BLOCKED"
    assert "not a Zenodo DOI" in checks[0]["detail"]


def test_check_public_doi_blocks_mismatched_record(monkeypatch):
    def fake_fetch_json(url, timeout=20):
        return {
            "doi": "10.5281/zenodo.123",
            "metadata": {"title": "Unrelated software"},
            "links": {"self_html": "https://zenodo.org/records/123"},
        }, None

    monkeypatch.setattr(external_release_check, "fetch_json", fake_fetch_json)
    checks = []

    external_release_check.check_public_doi(checks, "10.5281/zenodo.123", "KKKKJ687/ArtifactGate-EDA")

    assert checks[0]["name"] == "zenodo_record"
    assert checks[0]["status"] == "BLOCKED"
    assert "does not reference ArtifactGate-EDA" in checks[0]["detail"]
