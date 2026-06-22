from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceFile:
    repo: str
    commit: str
    path: str
    license_note: str

    @property
    def raw_url(self) -> str:
        return f"https://raw.githubusercontent.com/{self.repo}/{self.commit}/{self.path}"


@dataclass(frozen=True)
class ExternalCase:
    case_id: str
    subset: str
    adapter: str
    replayable_open_source: bool
    metadata_only: bool
    description: str
    source_files: tuple[SourceFile, ...]


YOSYS_COMMIT = "5d7486115ae5c5a4f87a4b8f9173b5f245a22536"
VERILATOR_COMMIT = "eafe9636cf58a74a6a90b6127821b2f4fab8940f"
NGSPICE_COMMIT = "032b1c32c4dbad45ff132bcfac1dbecadbd8abb0"
LOGISIM_EXAMPLES_COMMIT = "6e9fd4abe7d71b3767099a7a404d9ad7d47f0e2b"


CASES: tuple[ExternalCase, ...] = (
    ExternalCase(
        case_id="yosys_cmos_counter",
        subset="yosys_examples_subset",
        adapter="yosys",
        replayable_open_source=True,
        metadata_only=False,
        description="Yosys CMOS counter example subset",
        source_files=(
            SourceFile("YosysHQ/yosys", YOSYS_COMMIT, "examples/cmos/counter.v", "Yosys repository license"),
            SourceFile("YosysHQ/yosys", YOSYS_COMMIT, "examples/cmos/counter.ys", "Yosys repository license"),
            SourceFile("YosysHQ/yosys", YOSYS_COMMIT, "examples/cmos/cmos_cells.v", "Yosys repository license"),
        ),
    ),
    ExternalCase(
        case_id="yosys_osu035_example",
        subset="yosys_examples_subset",
        adapter="yosys",
        replayable_open_source=True,
        metadata_only=False,
        description="Yosys osu035 example subset",
        source_files=(
            SourceFile("YosysHQ/yosys", YOSYS_COMMIT, "examples/osu035/example.v", "Yosys repository license"),
            SourceFile("YosysHQ/yosys", YOSYS_COMMIT, "examples/osu035/example.ys", "Yosys repository license"),
        ),
    ),
    ExternalCase(
        case_id="yosys_smtbmc_demo1",
        subset="yosys_examples_subset",
        adapter="yosys",
        replayable_open_source=True,
        metadata_only=False,
        description="Yosys smtbmc Verilog demo subset",
        source_files=(SourceFile("YosysHQ/yosys", YOSYS_COMMIT, "examples/smtbmc/demo1.v", "Yosys repository license"),),
    ),
    ExternalCase(
        case_id="verilator_make_hello_c",
        subset="verilog_open_core_subset",
        adapter="verilator",
        replayable_open_source=True,
        metadata_only=False,
        description="Verilator make_hello_c top module",
        source_files=(SourceFile("verilator/verilator", VERILATOR_COMMIT, "examples/make_hello_c/top.v", "Verilator repository license"),),
    ),
    ExternalCase(
        case_id="verilator_make_tracing_c",
        subset="verilog_open_core_subset",
        adapter="verilator",
        replayable_open_source=True,
        metadata_only=False,
        description="Verilator make_tracing_c top and submodule",
        source_files=(
            SourceFile("verilator/verilator", VERILATOR_COMMIT, "examples/make_tracing_c/top.v", "Verilator repository license"),
            SourceFile("verilator/verilator", VERILATOR_COMMIT, "examples/make_tracing_c/sub.v", "Verilator repository license"),
        ),
    ),
    ExternalCase(
        case_id="ngspice_gain_stage",
        subset="ngspice_examples_subset",
        adapter="ngspice",
        replayable_open_source=True,
        metadata_only=False,
        description="ngspice gain stage circuit",
        source_files=(SourceFile("ngspice/ngspice", NGSPICE_COMMIT, "examples/various/gain_stage.cir", "ngspice repository license"),),
    ),
    ExternalCase(
        case_id="ngspice_param_sweep",
        subset="ngspice_examples_subset",
        adapter="ngspice",
        replayable_open_source=True,
        metadata_only=False,
        description="ngspice parameter sweep circuit",
        source_files=(SourceFile("ngspice/ngspice", NGSPICE_COMMIT, "examples/various/param_sweep.cir", "ngspice repository license"),),
    ),
    ExternalCase(
        case_id="ngspice_rc_meas_ac",
        subset="ngspice_examples_subset",
        adapter="ngspice",
        replayable_open_source=True,
        metadata_only=False,
        description="ngspice AC measurement circuit",
        source_files=(SourceFile("ngspice/ngspice", NGSPICE_COMMIT, "examples/measure/rc-meas-ac.sp", "ngspice repository license"),),
    ),
    ExternalCase(
        case_id="logisim_example_1",
        subset="logisim_sample_subset",
        adapter="logisim",
        replayable_open_source=False,
        metadata_only=True,
        description="Public Logisim combinational circuit example",
        source_files=(
            SourceFile(
                "NenadPantelic/Simple-digital-logic-circuits-in-LogiSim",
                LOGISIM_EXAMPLES_COMMIT,
                "Example_1.circ",
                "source repository license or homework example notice",
            ),
        ),
    ),
    ExternalCase(
        case_id="logisim_combinational_circuit",
        subset="logisim_sample_subset",
        adapter="logisim",
        replayable_open_source=False,
        metadata_only=True,
        description="Public Logisim combinational circuit bundle",
        source_files=(
            SourceFile(
                "NenadPantelic/Simple-digital-logic-circuits-in-LogiSim",
                LOGISIM_EXAMPLES_COMMIT,
                "Combinational_circuit.circ",
                "source repository license or homework example notice",
            ),
        ),
    ),
)


def _download(url: str, destination: Path, refresh: bool) -> str:
    if destination.exists() and not refresh:
        return "cached"
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "ArtifactGate-EDA external case fetcher"})
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
    destination.write_bytes(content)
    return "downloaded"


def _write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def prepare_external_cases(out_dir: Path, refresh: bool = False) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, object]] = []
    fetched_at = int(time.time())
    for case in CASES:
        case_dir = out_dir / case.subset / case.case_id
        source_dir = case_dir / "source"
        source_statuses = []
        for source in case.source_files:
            filename = Path(source.path).name
            destination = source_dir / filename
            status = _download(source.raw_url, destination, refresh)
            source_statuses.append(status)
            manifest_rows.append(
                {
                    "case_id": case.case_id,
                    "subset": case.subset,
                    "expected_adapter": case.adapter,
                    "replayable_open_source": str(case.replayable_open_source).lower(),
                    "metadata_only": str(case.metadata_only).lower(),
                    "public_source": "true",
                    "hardware_required": "false",
                    "commercial_dependency_required": "false",
                    "manual_adapter_fix_required": "false",
                    "source_repo": source.repo,
                    "source_commit": source.commit,
                    "source_path": source.path,
                    "source_url": source.raw_url,
                    "local_path": destination.relative_to(out_dir).as_posix(),
                    "license_note": source.license_note,
                    "fetch_status": status,
                    "fetched_at_epoch": fetched_at,
                }
            )
        case_manifest = {
            "case_id": case.case_id,
            "subset": case.subset,
            "expected_adapter": case.adapter,
            "replayable_open_source": case.replayable_open_source,
            "metadata_only": case.metadata_only,
            "public_source": True,
            "hardware_required": False,
            "commercial_dependency_required": False,
            "manual_adapter_fix_required": False,
            "description": case.description,
            "source_statuses": source_statuses,
        }
        (case_dir / "case_manifest.json").write_text(json.dumps(case_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_csv(manifest_rows, out_dir / "source_manifest.csv")
    readme = [
        "# External EDA Cases",
        "",
        "This directory contains public, software-only EDA artifact cases used for the IST external-case generalization benchmark.",
        "The replayable cases use ngspice, Yosys, or Verilator adapters as artifact-ingestion/replay evidence.",
        "Logisim cases are metadata-only and do not claim simulator execution.",
        "",
        "No case requires board hardware, Vivado licensing, bitstreams, vendor timing closure, or FPGA deployment evidence.",
        "",
        f"- external cases: {len(CASES)}",
        f"- replayable open-source cases: {sum(1 for case in CASES if case.replayable_open_source)}",
        f"- metadata-only cases: {sum(1 for case in CASES if case.metadata_only)}",
    ]
    (out_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    return {"ok": True, "status": "PASS", "summary": f"prepared {len(CASES)} external cases", "out": out_dir.as_posix()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare public external EDA cases for ArtifactGate-EDA IST evaluation.")
    parser.add_argument("--out", default="examples/external_cases")
    parser.add_argument("--refresh", action="store_true", help="Re-download files even when local copies already exist.")
    args = parser.parse_args()
    result = prepare_external_cases(Path(args.out), refresh=args.refresh)
    print(result["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
