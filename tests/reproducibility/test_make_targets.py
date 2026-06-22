from pathlib import Path


def test_required_make_targets_present():
    makefile = (Path(__file__).resolve().parents[2] / "Makefile").read_text()
    for target in [
        "smoke",
        "ingest-all",
        "reproduce-core",
        "negative-claims",
        "corrupted-tests",
        "scalability",
        "baseline",
        "summaries",
        "rq1-ingest-all",
        "rq2-replay-core",
        "rq2-replay-repeats",
        "rq3-negative-claims",
        "rq4-corrupted-artifacts",
        "rq5-evidence-classification",
        "external-cases",
        "rq6-external-cases",
        "rq6-scalability",
        "rq7-baseline",
        "rq8-ablation",
        "rq9-local-backends",
        "ist-package",
        "ist-all",
        "g13-check",
    ]:
        assert f"{target}:" in makefile
