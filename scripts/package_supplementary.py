from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release" / "artifactgate_eda_supplementary_artifacts.zip"

INCLUDE_ROOTS = [
    ROOT / "supplementary",
    ROOT / "reports",
    ROOT / "paper" / "figures",
]

INCLUDE_FILES = [
    ROOT / "paper" / "softwarex_manuscript.md",
    ROOT / "paper" / "softwarex_manuscript.tex",
    ROOT / "paper" / "highlights.md",
    ROOT / "paper" / "declarations.md",
    ROOT / "paper" / "MANUSCRIPT_REPRO_PACKAGE.md",
    ROOT / "paper" / "manuscript_artifact_manifest.csv",
    ROOT / "docs" / "softwarex_submission_checklist.md",
    ROOT / "docs" / "release_readiness.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files() -> list[Path]:
    files: set[Path] = set()
    for root in INCLUDE_ROOTS:
        if root.exists():
            files.update(path for path in root.rglob("*") if path.is_file())
    for path in INCLUDE_FILES:
        if path.exists():
            files.add(path)
    return sorted(files)


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    files = iter_files()
    manifest = []
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arcname = path.relative_to(ROOT).as_posix()
            zf.write(path, arcname)
            manifest.append(
                {
                    "path": arcname,
                    "sha256": sha256(path),
                    "size_bytes": path.stat().st_size,
                }
            )
        zf.writestr(
            "README.md",
            "ArtifactGate-EDA supplementary artifact package. Rebuild with `make supplementary-package`.\n",
        )
        zf.writestr("supplementary_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(OUT.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
