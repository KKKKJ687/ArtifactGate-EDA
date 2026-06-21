from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from artifactgate_eda import __version__
from artifactgate_eda.core.artifact import (
    benchmark_scale,
    claim_check,
    compare_outputs,
    ingest_artifacts,
    package_capsule,
    render_baseline_report,
    render_experiment_summaries,
    render_report,
    replay_case,
    validate_artifacts,
)


def _print_result(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    status = result.get("status", "UNKNOWN")
    print(f"status: {status}")
    for key in ("summary", "out", "errors", "warnings"):
        if key in result:
            print(f"{key}: {result[key]}")


def _finish(result: dict, as_json: bool, expect_fail: str | None = None) -> int:
    if expect_fail:
        codes = {err.get("code") for err in result.get("errors", [])}
        if expect_fail in codes:
            result["status"] = "EXPECTED_FAIL"
            _print_result(result, as_json)
            return 0
        result["status"] = "UNEXPECTED_PASS"
        result.setdefault("errors", []).append(
            {"code": "EXPECTED_FAILURE_NOT_SEEN", "message": expect_fail}
        )
        _print_result(result, as_json)
        return 1
    _print_result(result, as_json)
    return 0 if result.get("ok", False) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="artifactgate")
    parser.add_argument("--version", action="store_true", help="Print version and exit.")
    sub = parser.add_subparsers(dest="command")

    ingest = sub.add_parser("ingest", help="Ingest EDA artifacts into an index.")
    ingest.add_argument("root")
    ingest.add_argument("--adapter", required=True)
    ingest.add_argument("--out", required=True)
    ingest.add_argument("--json", action="store_true")

    validate = sub.add_parser("validate", help="Validate an artifact index or package directory.")
    validate.add_argument("target")
    validate.add_argument("--out")
    validate.add_argument("--expect-fail")
    validate.add_argument("--json", action="store_true")

    replay = sub.add_parser("replay", help="Replay or package-check a software-only case.")
    replay.add_argument("root")
    replay.add_argument("--adapter", required=True)
    replay.add_argument("--out", required=True)
    replay.add_argument("--smoke", action="store_true")
    replay.add_argument("--full", action="store_true")
    replay.add_argument("--json", action="store_true")

    claim = sub.add_parser("claim-check", help="Check claims against evidence policy.")
    claim.add_argument("--claims", required=True)
    claim.add_argument("--artifact-index")
    claim.add_argument("--policy")
    claim.add_argument("--out")
    claim.add_argument("--expect-fail")
    claim.add_argument("--json", action="store_true")

    report = sub.add_parser("report", help="Generate reviewer-ready report files.")
    report.add_argument("target")
    report.add_argument("--format", default="markdown")
    report.add_argument("--out", required=True)
    report.add_argument("--json", action="store_true")

    package = sub.add_parser("package", help="Create a zipped artifact capsule.")
    package.add_argument("target")
    package.add_argument("--out", required=True)
    package.add_argument("--json", action="store_true")

    compare = sub.add_parser("compare", help="Compare two artifact outputs for drift.")
    compare.add_argument("left")
    compare.add_argument("right")
    compare.add_argument("--out", required=True)
    compare.add_argument("--json", action="store_true")

    scale = sub.add_parser("benchmark-scale", help="Generate a synthetic scalability report.")
    scale.add_argument("--base", required=True)
    scale.add_argument("--scale", required=True, type=int)
    scale.add_argument("--out", required=True)
    scale.add_argument("--json", action="store_true")

    baseline = sub.add_parser("report-baseline", help="Generate baseline-comparison report.")
    baseline.add_argument("--out", required=True)
    baseline.add_argument("--json", action="store_true")

    summaries = sub.add_parser("summarize", help="Generate experiment summary reports.")
    summaries.add_argument("--repo", default=".")
    summaries.add_argument("--out", default="reports")
    summaries.add_argument("--json", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    if not args.command:
        parser.print_help()
        return 0

    try:
        if args.command == "ingest":
            result = ingest_artifacts(Path(args.root), args.adapter, Path(args.out))
            return _finish(result, args.json)
        if args.command == "validate":
            result = validate_artifacts(Path(args.target), Path(args.out) if args.out else None)
            return _finish(result, args.json, args.expect_fail)
        if args.command == "replay":
            result = replay_case(Path(args.root), args.adapter, Path(args.out), full=args.full)
            return _finish(result, args.json)
        if args.command == "claim-check":
            result = claim_check(
                claims_path=Path(args.claims),
                artifact_index=Path(args.artifact_index) if args.artifact_index else None,
                policy_path=Path(args.policy) if args.policy else None,
                out_dir=Path(args.out) if args.out else None,
            )
            return _finish(result, args.json, args.expect_fail)
        if args.command == "report":
            result = render_report(Path(args.target), Path(args.out), args.format)
            return _finish(result, args.json)
        if args.command == "package":
            result = package_capsule(Path(args.target), Path(args.out))
            return _finish(result, args.json)
        if args.command == "compare":
            result = compare_outputs(Path(args.left), Path(args.right), Path(args.out))
            return _finish(result, args.json)
        if args.command == "benchmark-scale":
            result = benchmark_scale(Path(args.base), args.scale, Path(args.out))
            return _finish(result, args.json)
        if args.command == "report-baseline":
            result = render_baseline_report(Path(args.out))
            return _finish(result, args.json)
        if args.command == "summarize":
            result = render_experiment_summaries(Path(args.repo), Path(args.out))
            return _finish(result, args.json)
    except Exception as exc:  # pragma: no cover - CLI guardrail
        print(f"artifactgate error: {exc}", file=sys.stderr)
        return 2
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
