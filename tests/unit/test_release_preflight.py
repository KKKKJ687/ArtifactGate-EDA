import importlib.util
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "release_preflight.py"
SPEC = importlib.util.spec_from_file_location("release_preflight", SCRIPT)
assert SPEC and SPEC.loader
release_preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_preflight)


def test_boundary_context_rejects_positive_hardware_claim():
    text = "The package demonstrates hardware validation on FPGA boards.".lower()
    index = text.find("hardware validation")

    assert not release_preflight.is_boundary_context(text, index)


def test_boundary_context_allows_explicit_limitation():
    text = "This software does not claim hardware validation or board evidence.".lower()
    index = text.find("hardware validation")

    assert release_preflight.is_boundary_context(text, index)


def test_readme_positive_forbidden_wording_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    monkeypatch.setattr(release_preflight, "SOURCE_DIRS", ["README.md"])
    (tmp_path / "README.md").write_text(
        "The package demonstrates hardware validation on FPGA boards.\n",
        encoding="utf-8",
    )

    errors = []
    release_preflight.check_wording_context(errors)

    assert errors == ["forbidden wording outside allowed context: README.md:1 (hardware validation)"]


def test_readme_limitation_wording_passes(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    monkeypatch.setattr(release_preflight, "SOURCE_DIRS", ["README.md"])
    (tmp_path / "README.md").write_text(
        "This software does not claim hardware validation or board evidence.\n",
        encoding="utf-8",
    )

    errors = []
    release_preflight.check_wording_context(errors)

    assert errors == []


def test_g13_template_limitation_wording_passes(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    monkeypatch.setattr(release_preflight, "SOURCE_DIRS", ["docs"])
    template = tmp_path / "docs" / "g13_author_expert_walkthrough_template.md"
    template.parent.mkdir()
    template.write_text(
        "This attestation does not imply hardware validation, DFX deployment, or board validation.\n",
        encoding="utf-8",
    )

    errors = []
    release_preflight.check_wording_context(errors)

    assert errors == []


def test_zip_private_path_payload_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        zip_handle.writestr("outputs/example.csv", "path,/Users/example/private/output.log\n")

    errors = []
    release_preflight.check_zip_private_paths(zip_path, errors)

    assert errors == [
        "private path payload found in release/artifactgate_eda_ist_evaluation_artifacts.zip:outputs/example.csv"
    ]


def test_zip_private_path_allowlist_passes(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_supplementary_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        zip_handle.writestr(
            "reports/file_inventory_private_paths.csv",
            "path,/Users/example/private/output.log,negative fixture\n",
        )

    errors = []
    release_preflight.check_zip_private_paths(zip_path, errors)

    assert errors == []


def test_ist_zip_absent_passes_when_ist_mode_inactive(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)

    errors = []
    release_preflight.check_ist_zip(errors)

    assert errors == []


def test_ist_zip_required_when_ist_mode_active(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    marker = tmp_path / "reports" / "IST_GAP_AUDIT.md"
    marker.parent.mkdir()
    marker.write_text("# IST gap audit\n", encoding="utf-8")

    errors = []
    release_preflight.check_ist_zip(errors)

    assert errors == ["missing IST evaluation zip: release/artifactgate_eda_ist_evaluation_artifacts.zip"]


def test_ist_zip_requires_workflow_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        zip_handle.writestr("docs/ist_author_external_completion_packet.md", "packet\n")

    errors = []
    release_preflight.check_ist_zip(errors)

    assert len(errors) == 1
    assert errors[0].startswith(
        "release/artifactgate_eda_ist_evaluation_artifacts.zip missing IST workflow artifacts:"
    )
    assert "docs/ist_stronger_plan_source_record.md" in errors[0]
    assert "docs/g13_author_expert_walkthrough_template.md" in errors[0]
    assert "scripts/validate_g13_walkthrough.py" in errors[0]
    assert ".codex_workflow/WORKFLOW_STATE.md" in errors[0]


def test_ist_zip_rejects_full_plan_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        for member in release_preflight.IST_ZIP_REQUIRED:
            zip_handle.writestr(member, "ok\n")
        zip_handle.writestr("docs/IST_ArtifactGate_EDA_Stronger_Optimization_Plan.md", "unsafe full plan\n")

    errors = []
    release_preflight.check_ist_zip(errors)

    assert errors == [
        "release/artifactgate_eda_ist_evaluation_artifacts.zip contains full external plan snapshot: "
        "['docs/IST_ArtifactGate_EDA_Stronger_Optimization_Plan.md']"
    ]


def test_ist_zip_rejects_partial_g13_evidence_set(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        for member in release_preflight.IST_ZIP_REQUIRED:
            zip_handle.writestr(member, "ok\n")
        zip_handle.writestr("reports/g13_author_expert_walkthrough_command_log.csv", "partial\n")

    errors = []
    release_preflight.check_ist_zip(errors)

    assert len(errors) == 1
    assert errors[0].startswith(
        "release/artifactgate_eda_ist_evaluation_artifacts.zip contains partial optional artifact set:"
    )
    assert "reports/g13_author_expert_walkthrough.md" in errors[0]
    assert "reports/g13_author_expert_walkthrough_observations.csv" in errors[0]


def test_ist_zip_accepts_complete_g13_evidence_set(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        for member in release_preflight.IST_ZIP_REQUIRED:
            zip_handle.writestr(member, "ok\n")
        for optional_set in release_preflight.IST_ZIP_OPTIONAL_COMPLETE_SETS:
            for member in optional_set:
                zip_handle.writestr(member, "ok\n")

    errors = []
    release_preflight.check_ist_zip(errors)

    assert errors == []


def test_ist_zip_rejects_resource_fork_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(release_preflight, "ROOT", tmp_path)
    zip_path = tmp_path / "release" / "artifactgate_eda_ist_evaluation_artifacts.zip"
    zip_path.parent.mkdir()
    with zipfile.ZipFile(zip_path, "w") as zip_handle:
        for member in release_preflight.IST_ZIP_REQUIRED:
            zip_handle.writestr(member, "ok\n")
        zip_handle.writestr("__MACOSX/._junk", "fork\n")

    errors = []
    release_preflight.check_ist_zip(errors)

    assert errors == [
        "release/artifactgate_eda_ist_evaluation_artifacts.zip contains macOS resource fork entries: "
        "['__MACOSX/._junk']"
    ]
