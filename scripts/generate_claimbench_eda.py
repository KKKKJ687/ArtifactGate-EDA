#!/usr/bin/env python3
"""Generate and summarize the ClaimBench-EDA benchmark."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


CLAIM_FIELDS = ["claim_id", "category", "claim_type", "claim_text", "expected_status"]
GOLD_FIELDS = [
    "claim_id",
    "text",
    "gold_status",
    "gold_required_level",
    "gold_claim_type",
    "allowed_context",
    "severity",
    "annotator_1",
    "annotator_2",
    "resolution",
]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fields or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def templates() -> list[dict[str, object]]:
    return [
        {
            "category": "safe_software_simulation_claims",
            "count": 300,
            "expected_status": "SUPPORTED",
            "required_level": "L3_SIMULATION",
            "claim_type": "safe_software",
            "severity": 0,
            "templates": [
                "The ngspice replay records software simulation evidence for case {i}.",
                "The HDL testbench output supports a software-only simulation statement for case {i}.",
                "The replay manifest records commands for software-only reproduction case {i}.",
            ],
        },
        {
            "category": "hardware_validation_overclaims",
            "count": 200,
            "expected_status": "UNSUPPORTED",
            "required_level": "L7_BOARD_MEASUREMENT",
            "claim_type": "hardware_overclaim",
            "severity": 5,
            "templates": [
                "The package provides hardware validation for case {i}.",
                "The design was validated on FPGA for case {i}.",
                "The software simulation result is ready for FPGA deployment in case {i}.",
                "The board measurement behavior is established by the replay package for case {i}.",
            ],
        },
        {
            "category": "vivado_timing_overclaims",
            "count": 150,
            "expected_status": "UNSUPPORTED",
            "required_level": "L5_VENDOR_IMPLEMENTATION",
            "claim_type": "vivado_timing_overclaim",
            "severity": 4,
            "templates": [
                "Vivado timing closure was achieved for HDL case {i}.",
                "The generated reports imply timing feasibility for case {i}.",
                "WNS validated across the design for case {i}.",
                "The Yosys result proves Vivado implementation evidence for case {i}.",
            ],
        },
        {
            "category": "dfx_deployment_overclaims",
            "count": 150,
            "expected_status": "UNSUPPORTED",
            "required_level": "L6_BITSTREAM",
            "claim_type": "dfx_overclaim",
            "severity": 4,
            "templates": [
                "DFX deployment is complete for reconfiguration case {i}.",
                "The modules are suitable for runtime reconfiguration in case {i}.",
                "Partial reconfiguration deployed successfully for case {i}.",
                "The reconfigurable partition is field update ready for case {i}.",
            ],
        },
        {
            "category": "bitstream_overclaims",
            "count": 100,
            "expected_status": "UNSUPPORTED",
            "required_level": "L6_BITSTREAM",
            "claim_type": "bitstream_overclaim",
            "severity": 4,
            "templates": [
                "Partial bitstream generated successfully for module {i}.",
                "The configuration image is loadable on the target for case {i}.",
                "A programming image was produced for case {i}.",
                "The bitstream verified runtime behavior for case {i}.",
            ],
        },
        {
            "category": "ambiguous_claims",
            "count": 150,
            "expected_status": "NEEDS_EXTERNAL_EVIDENCE",
            "required_level": "EXTERNAL_REVIEW",
            "claim_type": "ambiguous_external",
            "severity": 2,
            "templates": [
                "The package may support external tool analysis for case {i}, which needs external evidence.",
                "The result could be implementation-ready for case {i}, but requires external evidence.",
                "The case has hardware-like implications and needs external evidence for stronger claims {i}.",
            ],
        },
        {
            "category": "paraphrase_hard_cases",
            "count": 150,
            "expected_status": "UNSUPPORTED",
            "required_level": "L5_VENDOR_IMPLEMENTATION",
            "claim_type": "hard_paraphrase",
            "severity": 4,
            "templates": [
                "The synthesis evidence makes the design ready for FPGA deployment in case {i}.",
                "The flow closes the gap to implementation feasibility for case {i}.",
                "The design path has hardware-level implications for case {i}.",
                "The generated reports imply timing feasibility for case {i}.",
                "The module is implementation-ready for runtime use in case {i}.",
            ],
        },
        {
            "category": "safe_limitation_statements",
            "count": 100,
            "expected_status": "SUPPORTED",
            "required_level": "L0_METADATA",
            "claim_type": "safe_limitation",
            "severity": 0,
            "templates": [
                "No board measurements are claimed for case {i}.",
                "Vivado timing closure is not evaluated for case {i}.",
                "No bitstream evidence is claimed for case {i}.",
                "DFX deployment is outside the scope for case {i}.",
            ],
        },
    ]


def generate(out_dir: Path, minimum: int) -> int:
    claims: list[dict[str, object]] = []
    gold: list[dict[str, object]] = []
    claim_index = 1
    for group in templates():
        group_templates = group["templates"]
        assert isinstance(group_templates, list)
        for idx in range(1, int(group["count"]) + 1):
            template = str(group_templates[(idx - 1) % len(group_templates)])
            text = template.format(i=idx)
            claim_id = f"CB-EDA-{claim_index:04d}"
            claims.append(
                {
                    "claim_id": claim_id,
                    "category": group["category"],
                    "claim_type": group["claim_type"],
                    "claim_text": text,
                    "expected_status": group["expected_status"],
                }
            )
            gold.append(
                {
                    "claim_id": claim_id,
                    "text": text,
                    "gold_status": group["expected_status"],
                    "gold_required_level": group["required_level"],
                    "gold_claim_type": group["claim_type"],
                    "allowed_context": "yes" if group["category"] == "safe_limitation_statements" else "no",
                    "severity": group["severity"],
                    "annotator_1": "policy_seed",
                    "annotator_2": "policy_seed",
                    "resolution": "policy_seed_gold",
                }
            )
            claim_index += 1
    if len(claims) < minimum:
        raise ValueError(f"generated {len(claims)} claims, below requested minimum {minimum}")
    write_csv(out_dir / "claimbench_claims.csv", claims, CLAIM_FIELDS)
    write_csv(out_dir / "claimbench_gold.csv", gold, GOLD_FIELDS)
    return len(claims)


def f1_score(tp: int, fp: int, fn: int) -> float:
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def summarize(report_path: Path, reports_dir: Path) -> None:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    rows = payload["claims"]
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_csv(reports_dir / "rq3_claimbench_results.csv", rows)

    by_type: Counter[tuple[str, str, str]] = Counter()
    rewrite_rows = []
    for row in rows:
        by_type[(row["category"], row["expected_status"], row["status"])] += 1
    confusion_rows = [
        {
            "category": category,
            "expected_status": expected,
            "predicted_status": predicted,
            "count": count,
        }
        for (category, expected, predicted), count in sorted(by_type.items())
    ]
    write_csv(reports_dir / "rq3_confusion_by_claim_type.csv", confusion_rows)

    categories = sorted({row["category"] for row in rows})
    for category in categories:
        subset = [row for row in rows if row["category"] == category]
        unsupported = [row for row in subset if row["status"] == "UNSUPPORTED"]
        rewrite_count = sum(1 for row in unsupported if row.get("safe_rewrite"))
        rewrite_rows.append(
            {
                "category": category,
                "unsupported_predicted": len(unsupported),
                "safe_rewrite_count": rewrite_count,
                "safe_rewrite_coverage": f"{rewrite_count / len(unsupported):.6g}" if unsupported else "1",
            }
        )
    write_csv(reports_dir / "rq3_safe_rewrite_coverage.csv", rewrite_rows)

    expected_statuses = sorted({row["expected_status"] for row in rows})
    macro_f1_values = []
    for status in expected_statuses:
        tp = sum(1 for row in rows if row["expected_status"] == status and row["status"] == status)
        fp = sum(1 for row in rows if row["expected_status"] != status and row["status"] == status)
        fn = sum(1 for row in rows if row["expected_status"] == status and row["status"] != status)
        macro_f1_values.append(f1_score(tp, fp, fn))
    macro_f1 = sum(macro_f1_values) / len(macro_f1_values)
    critical_fn = sum(
        1
        for row in rows
        if row["expected_status"] == "UNSUPPORTED"
        and row["status"] != "UNSUPPORTED"
        and row["category"] in {
            "hardware_validation_overclaims",
            "vivado_timing_overclaims",
            "dfx_deployment_overclaims",
            "bitstream_overclaims",
            "paraphrase_hard_cases",
        }
    )
    safe_limitation = [row for row in rows if row["category"] == "safe_limitation_statements"]
    safe_limitation_fp = sum(1 for row in safe_limitation if row["status"] == "UNSUPPORTED")
    paraphrase = [row for row in rows if row["category"] == "paraphrase_hard_cases"]
    paraphrase_recall = sum(1 for row in paraphrase if row["status"] == "UNSUPPORTED") / len(paraphrase)
    unsupported_expected = [row for row in rows if row["expected_status"] == "UNSUPPORTED"]
    unsupported_recall = sum(1 for row in unsupported_expected if row["status"] == "UNSUPPORTED") / len(unsupported_expected)
    summary = {
        "claim_count": len(rows),
        "unsupported_expected": len(unsupported_expected),
        "unsupported_recall": unsupported_recall,
        "macro_f1": macro_f1,
        "critical_false_negative_count": critical_fn,
        "safe_limitation_false_positive_rate": safe_limitation_fp / len(safe_limitation),
        "paraphrase_recall": paraphrase_recall,
        "safe_rewrite_coverage": min(float(row["safe_rewrite_coverage"]) for row in rewrite_rows),
    }
    write_csv(reports_dir / "rq3_inter_rater_agreement.csv", [{"metric": "independent_inter_rater_agreement", "value": "not_run_policy_seed_only", "status": "LIMITATION"}])
    (reports_dir / "rq3_claimbench_gold_standard.md").write_text(
        "# ClaimBench-EDA Gold Standard\n\n"
        "The current gold standard is policy-seeded and deterministic. It does not claim independent human inter-rater agreement.\n",
        encoding="utf-8",
    )
    lines = [
        "# RQ3 ClaimBench-EDA Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value:.6g} |" if isinstance(value, float) else f"| {key} | {value} |" for key, value in summary.items())
    lines.extend(
        [
            "",
            "Independent human inter-rater agreement has not been run; the current gold standard is policy-seeded.",
            "This supports the automated ClaimBench gate but remains a validity limitation for manuscript wording.",
        ]
    )
    (reports_dir / "rq3_claimbench_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1200)
    parser.add_argument("--out", default="examples/claimbench_eda")
    parser.add_argument("--summarize", help="Path to artifactgate claim-check report JSON.")
    parser.add_argument("--reports", default="reports")
    args = parser.parse_args()
    if args.summarize:
        summarize(Path(args.summarize), Path(args.reports))
        print(f"summarized ClaimBench results -> {args.reports}")
        return 0
    count = generate(Path(args.out), args.n)
    print(f"generated {count} ClaimBench-EDA claims -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
