from __future__ import annotations

from pathlib import Path
from typing import Protocol


class BaseAdapter(Protocol):
    name: str
    supported_extensions: list[str]
    default_evidence_level: str

    def detect(self, path: Path) -> bool:
        ...

    def collect_artifacts(self, root: Path) -> list[Path]:
        ...

    def extract_tool_version(self, root: Path) -> dict:
        ...

    def build_replay_manifest(self, root: Path) -> dict:
        ...

    def classify_artifact(self, path: Path) -> str:
        ...

