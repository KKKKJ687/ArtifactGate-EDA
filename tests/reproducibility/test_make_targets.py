from pathlib import Path


def test_required_make_targets_present():
    makefile = (Path(__file__).resolve().parents[2] / "Makefile").read_text()
    for target in ["smoke", "ingest-all", "reproduce-core", "negative-claims", "corrupted-tests", "scalability", "baseline", "summaries"]:
        assert f"{target}:" in makefile
