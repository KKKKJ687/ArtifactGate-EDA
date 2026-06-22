#!/usr/bin/env python3
"""Build a lightweight evidence graph from the IST file inventory."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import re
from collections import Counter
from pathlib import Path

PNG_FALLBACK = (
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def safe_id(prefix: str, value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in value).strip("_")
    return f"{prefix}:{cleaned[:96] or 'root'}"


def read_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def add_node(nodes: dict[str, dict[str, str]], node_id: str, node_type: str, label: str, **extra: str) -> None:
    nodes.setdefault(
        node_id,
        {
            "node_id": node_id,
            "node_type": node_type,
            "label": label,
            "path_or_key": extra.get("path_or_key", ""),
            "status": extra.get("status", ""),
            "sha256": extra.get("sha256", ""),
            "evidence_level": extra.get("evidence_level", ""),
        },
    )


def build_graph(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []
    rel_to_artifact = {row["relative_path"]: f"artifact:{row['file_id']}" for row in rows}
    add_node(nodes, "policy:claim_boundary", "Policy", "Claim boundary policy", status="ACTIVE")
    add_node(nodes, "tool:artifactgate", "Tool", "artifactgate", status="LOCAL_PACKAGE")

    for row in rows:
        artifact_id = f"artifact:{row['file_id']}"
        add_node(
            nodes,
            artifact_id,
            "Artifact",
            row["relative_path"],
            path_or_key=row["relative_path"],
            status="INDEXED",
            sha256=row["sha256"],
            evidence_level=row["evidence_level"],
        )
        if row["adapter"]:
            adapter_id = safe_id("adapter", row["adapter"])
            add_node(nodes, adapter_id, "Adapter", row["adapter"], status="REFERENCED")
            edges.append(edge(artifact_id, adapter_id, "requires", row["relative_path"]))
        if row["generated_by"]:
            run_id = safe_id("run", row["generated_by"])
            add_node(nodes, run_id, "Run", row["generated_by"], status="DECLARED")
            edges.append(edge(artifact_id, run_id, "produced_by", row["relative_path"]))
        if row["role"] == "report":
            report_id = safe_id("report", row["relative_path"])
            add_node(nodes, report_id, "Report", row["relative_path"], path_or_key=row["relative_path"], status="PRESENT")
            for source_id in report_sources(row["relative_path"], rows, rel_to_artifact):
                edges.append(edge(report_id, source_id, "derived_from", row["relative_path"]))
        if row["role"] == "policy":
            edges.append(edge("policy:claim_boundary", artifact_id, "derived_from", row["relative_path"]))

    for claim in extract_claims(rows):
        claim_id = safe_id("claim", f"{claim['source']}:{claim['line_no']}:{claim['text'][:48]}")
        add_node(
            nodes,
            claim_id,
            "Claim",
            claim["text"][:140],
            path_or_key=f"{claim['source']}:{claim['line_no']}",
            status=claim["status"],
        )
        linked = False
        for target_path in referenced_report_paths(claim["text"]):
            target = rel_to_artifact.get(target_path)
            if target:
                edges.append(edge(claim_id, target, "supports", claim["source"]))
                linked = True
        source_artifact = rel_to_artifact.get(claim["source"])
        if source_artifact:
            edges.append(edge(claim_id, source_artifact, "supports", claim["source"]))
            linked = True
        if not linked:
            edges.append(edge(claim_id, "policy:claim_boundary", "requires", claim["source"]))
        if "UNSUPPORTED" in claim["status"] or "BOUNDARY" in claim["status"] or "LIMITATION" in claim["status"]:
            edges.append(edge("policy:claim_boundary", claim_id, "blocks", claim["source"]))

    node_ids = set(nodes)
    dangling = sum(1 for item in edges if item["source"] not in node_ids or item["target"] not in node_ids)
    metrics = {
        "artifact_nodes": sum(1 for node in nodes.values() if node["node_type"] == "Artifact"),
        "artifact_nodes_with_sha256": sum(
            1 for node in nodes.values() if node["node_type"] == "Artifact" and node["sha256"]
        ),
        "claim_nodes": sum(1 for node in nodes.values() if node["node_type"] == "Claim"),
        "claim_nodes_with_status": sum(1 for node in nodes.values() if node["node_type"] == "Claim" and node["status"]),
        "dangling_edges": dangling,
        "unsupported_claim_nodes": sum(
            1 for node in nodes.values() if node["node_type"] == "Claim" and "UNSUPPORTED" in node["status"]
        ),
        "unsupported_claim_nodes_linked_to_policy": len(
            {item["target"] for item in edges if item["source"] == "policy:claim_boundary" and item["edge_type"] == "blocks"}
        ),
        "report_nodes": sum(1 for node in nodes.values() if node["node_type"] == "Report"),
        "report_nodes_with_source_artifact": report_nodes_with_source_artifact(nodes, edges),
    }
    return list(nodes.values()), edges, metrics


def edge(source: str, target: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": source, "target": target, "edge_type": edge_type, "evidence": evidence}


def report_sources(report_path: str, rows: list[dict[str, str]], rel_to_artifact: dict[str, str]) -> list[str]:
    lowered = report_path.lower()
    candidates: set[str] = set()
    mapping = [
        (("file_inventory",), ("scripts/audit_file_inventory.py",)),
        (("evidence_graph",), ("scripts/build_evidence_graph.py", "reports/file_inventory_full.csv")),
        (("claim_boundary",), ("scripts/find_claim_boundary_terms.py", "repo/src/artifactgate_eda/policies/forbidden_claims.yaml")),
        (
            ("ist_manuscript_claim_gate",),
            ("scripts/check_ist_manuscript_claims.py", "paper/manuscript_ist.md", "paper/manuscript_ist.tex"),
        ),
        (("rq1", "multi_adapter"), ("scripts/generate_ist_datasets.py", "examples/", "outputs/rq1_")),
        (("rq2", "replay"), ("examples/", "outputs/rq2_")),
        (("rq3", "negative_claim"), ("examples/negative_claim_cases/", "outputs/rq3_negative_claims")),
        (("rq4", "corrupt"), ("examples/corrupted_artifact_cases/", "outputs/rq4_corrupted_artifacts")),
        (("rq5", "evidence_level"), ("examples/evidence_level_gold_standard/", "outputs/rq5_evidence_classification")),
        (
            ("rq6_external", "external_case"),
            ("scripts/prepare_external_eda_cases.py", "examples/external_cases/", "outputs/rq6_external_cases"),
        ),
        (("rq6", "scalability"), ("examples/scalability_cases/", "outputs/rq6_scalability")),
        (("rq7", "baseline", "e6_baseline"), ("repo/src/artifactgate_eda/core/artifact.py", "outputs/rq7_baseline")),
        (("rq8", "ablation"), ("repo/src/artifactgate_eda/core/artifact.py", "outputs/rq8_ablation")),
        (("rq9", "backend"), ("repo/src/artifactgate_eda/core/artifact.py", "outputs/rq9_local_backends")),
        (("ist_empirical",), ("repo/src/artifactgate_eda/core/artifact.py", "reports/")),
    ]
    for tokens, sources in mapping:
        if any(token in lowered for token in tokens):
            candidates.update(match_sources(rows, sources, rel_to_artifact))
    if not candidates:
        candidates.update(match_sources(rows, ("repo/src/artifactgate_eda/core/artifact.py", "scripts/"), rel_to_artifact))
    return sorted(candidates)


def match_sources(rows: list[dict[str, str]], prefixes: tuple[str, ...], rel_to_artifact: dict[str, str]) -> set[str]:
    candidates: set[str] = set()
    for prefix in prefixes:
        exact = rel_to_artifact.get(prefix)
        if exact:
            candidates.add(exact)
            continue
        for row in rows:
            rel = row["relative_path"]
            if rel.startswith(prefix) and row["role"] != "report":
                candidates.add(rel_to_artifact[rel])
    return candidates


def extract_claims(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    claims: list[dict[str, str]] = []
    for row in rows:
        rel = row["relative_path"]
        path = Path(rel)
        if not is_claim_source(row):
            continue
        if path.suffix.lower() == ".csv":
            claims.extend(extract_csv_claims(path, rel))
        elif path.suffix.lower() == ".json":
            claims.extend(extract_json_claims(path, rel))
        elif path.suffix.lower() in {".md", ".tex", ".txt"}:
            claims.extend(extract_text_claims(path, rel))
    return claims


def is_claim_source(row: dict[str, str]) -> bool:
    rel = row["relative_path"].lower()
    if rel.startswith("reports/claim_boundary_scan.csv"):
        return False
    return any(token in rel for token in ("claim", "unsupported_ledger", "manuscript_ist", "softwarex_manuscript"))


def extract_csv_claims(path: Path, rel: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    claims: list[dict[str, str]] = []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for index, row in enumerate(reader, start=2):
                text = row.get("text") or row.get("claim_text") or row.get("claim") or row.get("context") or ""
                if not text.strip():
                    continue
                status = row.get("gold_status") or row.get("expected_status") or row.get("status") or infer_status(text)
                claims.append(claim(rel, index, text, status))
    except (OSError, csv.Error):
        return []
    return claims


def extract_json_claims(path: Path, rel: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    claims: list[dict[str, str]] = []
    for index, item in enumerate(walk_json_objects(data), start=1):
        text = item.get("claim_text") or item.get("claim") or item.get("text") or ""
        if text:
            status = item.get("status") or item.get("classification") or item.get("expected_status") or infer_status(text)
            claims.append(claim(rel, index, text, status))
    return claims


def walk_json_objects(data: object) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    if isinstance(data, dict):
        if any(key in data for key in ("claim_text", "claim", "text")):
            found.append({str(key): str(value) for key, value in data.items()})
        for value in data.values():
            found.extend(walk_json_objects(value))
    elif isinstance(data, list):
        for value in data:
            found.extend(walk_json_objects(value))
    return found


def extract_text_claims(path: Path, rel: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    claims: list[dict[str, str]] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not is_claim_line(stripped):
            continue
        claims.append(claim(rel, index, stripped, infer_status(stripped)))
    return claims


def is_claim_line(text: str) -> bool:
    if not text or text.startswith(("|---", "```", "\\", "%")):
        return False
    lowered = text.lower()
    cues = ("rq", "artifactgate", "claim", "support", "reported", "evaluated", "generated", "does not", "cannot")
    return any(cue in lowered for cue in cues)


def infer_status(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ("unsupported", "does not", "cannot", "not ", "no ", "without", "outside")):
        return "LIMITATION_OR_UNSUPPORTED_BOUNDARY"
    if any(term in lowered for term in ("validated on fpga", "vivado", "dfx", "bitstream", "board-level")):
        return "UNSUPPORTED_BOUNDARY_CONTEXT"
    return "DIRECT_OR_REPORTED_CLAIM"


def claim(source: str, line_no: int, text: str, status: str) -> dict[str, str]:
    normalized = " ".join(text.split())
    return {"source": source, "line_no": str(line_no), "text": normalized, "status": status or infer_status(normalized)}


def referenced_report_paths(text: str) -> list[str]:
    return sorted(set(re.findall(r"reports/[A-Za-z0-9_./-]+(?:\.md|\.csv|\.json)", text)))


def report_nodes_with_source_artifact(nodes: dict[str, dict[str, str]], edges: list[dict[str, str]]) -> int:
    report_ids = {node_id for node_id, node in nodes.items() if node["node_type"] == "Report"}
    sourced = {
        item["source"]
        for item in edges
        if item["source"] in report_ids and item["edge_type"] == "derived_from" and item["target"].startswith("artifact:")
    }
    return len(sourced)


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, nodes: list[dict[str, str]], edges: list[dict[str, str]], metrics: dict[str, int]) -> None:
    node_types = Counter(node["node_type"] for node in nodes)
    edge_types = Counter(item["edge_type"] for item in edges)
    lines = [
        "# Evidence Graph Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| nodes | {len(nodes)} |",
        f"| edges | {len(edges)} |",
        f"| artifact nodes with sha256 | {metrics['artifact_nodes_with_sha256']} / {metrics['artifact_nodes']} |",
        f"| claim nodes with status | {metrics['claim_nodes_with_status']} / {metrics['claim_nodes']} |",
        f"| dangling edges | {metrics['dangling_edges']} |",
        f"| report/document nodes linked to source artifacts | "
        f"{metrics['report_nodes_with_source_artifact']} / {metrics['report_nodes']} |",
        "| unsupported claims linked to policy | "
        f"{metrics['unsupported_claim_nodes_linked_to_policy']} / {metrics['unsupported_claim_nodes']} |",
        "",
        "## Node Types",
        "",
        "| Type | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(node_types.items()))
    lines.extend(["", "## Edge Types", "", "| Type | Count |", "|---|---:|"])
    lines.extend(f"| {key} | {value} |" for key, value in sorted(edge_types.items()))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_overview_png(path: Path, nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageDraw, ImageFont

        image = Image.new("RGB", (1100, 620), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        boxes = [
            ("Artifacts", Counter(node["node_type"] for node in nodes)["Artifact"], (70, 100), "#d7ecff"),
            ("Adapters", Counter(node["node_type"] for node in nodes)["Adapter"], (330, 100), "#e7f4d3"),
            ("Policies", Counter(node["node_type"] for node in nodes)["Policy"], (590, 100), "#fff1c7"),
            ("Reports", Counter(node["node_type"] for node in nodes)["Report"], (850, 100), "#eadcff"),
            ("Claims", Counter(node["node_type"] for node in nodes)["Claim"], (460, 360), "#ffdce0"),
        ]
        draw.text((60, 35), "ArtifactGate-EDA IST Evidence Graph Overview", fill="black", font=font)
        for label, count, (x_pos, y_pos), color in boxes:
            draw.rounded_rectangle((x_pos, y_pos, x_pos + 180, y_pos + 90), radius=10, fill=color, outline="black")
            draw.text((x_pos + 16, y_pos + 25), label, fill="black", font=font)
            draw.text((x_pos + 16, y_pos + 52), f"nodes: {count}", fill="black", font=font)
        for start, end in [((250, 145), (330, 145)), ((510, 145), (590, 145)), ((770, 145), (850, 145))]:
            draw.line((start, end), fill="black", width=2)
        draw.line((550, 190, 550, 360), fill="black", width=2)
        draw.text((60, 560), f"Generated from inventory: {len(nodes)} nodes, {len(edges)} edges", fill="black", font=font)
        image.save(path)
    except Exception:
        path.write_bytes(base64.b64decode(PNG_FALLBACK))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="reports/file_inventory_full.csv")
    parser.add_argument("--out", default="reports/evidence_graph_edges.csv")
    args = parser.parse_args()

    inventory = Path(args.inventory)
    out_edges = Path(args.out)
    rows = read_inventory(inventory)
    nodes, edges, metrics = build_graph(rows)
    out_nodes = out_edges.with_name("evidence_graph_nodes.csv")
    summary = out_edges.with_name("evidence_graph_summary.md")

    write_csv(
        out_nodes,
        nodes,
        ["node_id", "node_type", "label", "path_or_key", "status", "sha256", "evidence_level"],
    )
    write_csv(out_edges, edges, ["source", "target", "edge_type", "evidence"])
    write_summary(summary, nodes, edges, metrics)
    write_overview_png(Path("paper/figures/evidence_graph_overview.png"), nodes, edges)
    print(f"built evidence graph: {len(nodes)} nodes, {len(edges)} edges -> {out_edges}")
    return 1 if metrics["dangling_edges"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
