import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "prepare_release_metadata.py"
SPEC = importlib.util.spec_from_file_location("prepare_release_metadata", SCRIPT)
assert SPEC and SPEC.loader
prepare_release_metadata = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare_release_metadata)
update_markdown = prepare_release_metadata.update_markdown
update_tex = prepare_release_metadata.update_tex
update_zenodo = prepare_release_metadata.update_zenodo


def test_update_markdown_replaces_zenodo_placeholder():
    text = (
        "Repository: https://github.com/KKKKJ687/ArtifactGate-EDA. "
        "The archived Zenodo\nDOI will be added before SoftwareX submission.\n"
    )
    updated, changes = update_markdown(text, "https://github.com/KKKKJ687/ArtifactGate-EDA", "10.5281/zenodo.123")

    assert "Archived release DOI: 10.5281/zenodo.123." in updated
    assert "will be added before SoftwareX submission" not in updated
    assert changes


def test_update_tex_replaces_zenodo_placeholder():
    text = (
        "Repository: https://github.com/KKKKJ687/ArtifactGate-EDA. The archived Zenodo DOI\n"
        "will be added before SoftwareX submission.\n\n"
        "\\end{document}\n"
    )
    updated, changes = update_tex(text, "https://github.com/KKKKJ687/ArtifactGate-EDA", "10.5281/zenodo.123")

    assert "Archived release DOI: 10.5281/zenodo.123." in updated
    assert "will be added before SoftwareX submission" not in updated
    assert "\\end{document}" in updated
    assert changes


def test_update_markdown_replaces_pending_release_doi():
    text = (
        "Repository: https://github.com/KKKKJ687/ArtifactGate-EDA. "
        "The v0.1.2 archived release DOI will be finalized after Zenodo processes "
        "the v0.1.2 GitHub release.\n"
    )
    updated, changes = update_markdown(text, "https://github.com/KKKKJ687/ArtifactGate-EDA", "10.5281/zenodo.456")

    assert "Archived release DOI: 10.5281/zenodo.456." in updated
    assert "will be finalized after Zenodo" not in updated
    assert updated.count("10.5281/zenodo.456") == 1
    assert changes


def test_update_zenodo_replaces_previous_version_doi():
    text = """{
  "related_identifiers": [
    {
      "identifier": "https://github.com/KKKKJ687/ArtifactGate-EDA",
      "relation": "isSupplementTo",
      "scheme": "url"
    },
    {
      "identifier": "10.5281/zenodo.123",
      "relation": "isIdenticalTo",
      "scheme": "doi"
    }
  ]
}
"""
    updated, changes = update_zenodo(text, "https://github.com/KKKKJ687/ArtifactGate-EDA", "10.5281/zenodo.456")

    assert "10.5281/zenodo.123" not in updated
    assert "10.5281/zenodo.456" in updated
    assert "related_identifiers.doi.replace" in changes
