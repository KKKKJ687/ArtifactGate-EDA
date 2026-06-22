from __future__ import annotations

import argparse
from pathlib import Path

from artifactgate_eda.core.artifact import generate_corrupted_artifact_cases_extended


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the extended IST corrupted-artifact fixture set.")
    parser.add_argument("--classes", type=int, default=30, help="Expected defect-class count.")
    parser.add_argument("--instances", type=int, default=30, help="Instances per defect class.")
    parser.add_argument("--clean-cases", type=int, default=30, help="Clean specificity cases.")
    parser.add_argument("--out", required=True, help="Output fixture directory.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.classes != 30:
        raise SystemExit("the extended IST corruption taxonomy is fixed at 30 defect classes")
    result = generate_corrupted_artifact_cases_extended(
        Path(args.out),
        instances_per_defect=args.instances,
        clean_cases=args.clean_cases,
    )
    print(f"status: {result['status']}")
    print(f"summary: {result['summary']}")
    print(f"out: {result['out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
