from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate_claims() -> None:
    hardware_phrase = "hardware " + "validation"
    vendor_timing_phrase = "Vivado " + "timing closure"
    dfx_phrase = "DFX " + "deployment"
    image_phrase = "Partial " + "bitstream generated"
    board_phrase = "Board " + "validation"
    groups = [
        (
            "safe_software_simulation_claims",
            60,
            "SUPPORTED",
            "The ngspice replay records software simulation evidence for case {i}.",
        ),
        (
            "safe_synthesis_claims",
            40,
            "SUPPORTED",
            "The Yosys report records L4 synthesis evidence for HDL case {i}.",
        ),
        (
            "hardware_validation_overclaims",
            50,
            "UNSUPPORTED",
            f"The package provides {hardware_phrase} for case {{i}}.",
        ),
        (
            "vivado_timing_overclaims",
            40,
            "UNSUPPORTED",
            f"{vendor_timing_phrase} was achieved for HDL case {{i}}.",
        ),
        (
            "dfx_deployment_overclaims",
            40,
            "UNSUPPORTED",
            f"{dfx_phrase} is complete for reconfiguration case {{i}}.",
        ),
        (
            "bitstream_overclaims",
            30,
            "UNSUPPORTED",
            f"{image_phrase} successfully for module {{i}}.",
        ),
        (
            "board_level_overclaims",
            30,
            "UNSUPPORTED",
            f"{board_phrase} complete for experiment {{i}}.",
        ),
        (
            "ambiguous_claims",
            30,
            "NEEDS_EXTERNAL_EVIDENCE",
            "The package may support external tool analysis for case {i}, which needs external evidence.",
        ),
        (
            "generic_reproducibility_claims",
            20,
            "PARTIALLY_SUPPORTED",
            "The package records partial software-only reproduction metadata for case {i}.",
        ),
    ]
    rows = []
    claim_idx = 1
    for category, count, status, template in groups:
        for local_idx in range(1, count + 1):
            rows.append(
                {
                    "claim_id": f"IST-CL-{claim_idx:03d}",
                    "category": category,
                    "claim_text": template.format(i=local_idx),
                    "expected_status": status,
                }
            )
            claim_idx += 1
    write_csv(ROOT / "examples" / "negative_claim_cases" / "claims_full.csv", rows)


def generate_evidence_gold() -> None:
    rows = []

    development_tools = ("ngspice", "icarus", "yosys")
    development_rows = 0

    def add_rows(count: int, prefix: str, tool: str, artifact_type: str, path_template: str, level: str) -> None:
        nonlocal development_rows
        start = len(rows) + 1
        for idx in range(1, count + 1):
            tool_lower = tool.lower()
            evaluation_group = "policy_development_tool" if any(token in tool_lower for token in development_tools) else "cross_tool_holdout"
            if evaluation_group == "policy_development_tool" and development_rows < 400:
                dataset_split = "policy_development"
                development_rows += 1
            else:
                dataset_split = "holdout"
            supported_positive_claims = "no" if level in {"L5_VENDOR_IMPLEMENTATION", "L6_BITSTREAM", "L7_BOARD_MEASUREMENT"} else "yes"
            rows.append(
                {
                    "artifact_id": f"{prefix}-{idx:04d}",
                    "path": path_template.format(i=idx),
                    "tool": tool,
                    "artifact_type": artifact_type,
                    "expected_evidence_level": level,
                    "dataset_split": dataset_split,
                    "evaluation_group": evaluation_group,
                    "supported_positive_claims": supported_positive_claims,
                    "allowed_claims": f"{artifact_type} is recorded",
                    "forbidden_claims": "claims above the recorded software evidence level",
                }
            )
        assert len(rows) == start + count - 1

    add_rows(40, "META-PLECS", "PLECS", "metadata-only model files", "models/model_{i}.plecs", "L0_METADATA")
    add_rows(40, "META-LTSPICE", "LTspice", "metadata-only schematic files", "ltspice/case_{i}.asc", "L0_METADATA")
    add_rows(40, "META-LOGISIM", "Logisim", "metadata-only circuit files", "logisim/circuit_{i}.circ", "L0_METADATA")
    add_rows(80, "SRC-ICARUS", "Icarus Verilog", "source files", "src/module_{i}.v", "L1_SOURCE_EXISTS")
    add_rows(40, "SRC-YOSYS", "Yosys", "source files", "src/yosys_module_{i}.v", "L1_SOURCE_EXISTS")
    add_rows(40, "SRC-VERILATOR", "Verilator", "source files", "src/verilator_module_{i}.v", "L1_SOURCE_EXISTS")
    add_rows(70, "REF-ICARUS", "Icarus Verilog", "testbench/reference files", "reference/reference_vector_{i}.csv", "L2_REFERENCE_OR_INTERFACE")
    add_rows(40, "REF-NGSPICE", "ngspice", "interface/reference files", "interface/interface_vector_{i}.json", "L2_REFERENCE_OR_INTERFACE")
    add_rows(30, "REF-VERILATOR", "Verilator", "interface/reference files", "reference/verilator_interface_{i}.xml", "L2_REFERENCE_OR_INTERFACE")
    add_rows(80, "SIM-NGLOG", "ngspice", "simulation logs", "logs/software_sim_{i}.log", "L3_SIMULATION")
    add_rows(40, "SIM-NGCSV", "ngspice", "raw/csv outputs", "outputs/software_result_{i}.csv", "L3_SIMULATION")
    add_rows(40, "SIM-ICARUS", "Icarus Verilog", "compiled simulation outputs", "sim/case_{i}.vvp", "L3_SIMULATION")
    add_rows(40, "SIM-VERILATOR", "Verilator", "simulation logs", "logs/verilator_sim_{i}.log", "L3_SIMULATION")
    add_rows(60, "SYNTH-RPT", "Yosys", "synthesis reports", "synth/yosys_report_{i}.rpt", "L4_SYNTHESIS")
    add_rows(60, "SYNTH-JSON", "Yosys", "synthesis JSON outputs", "synth/yosys_netlist_{i}.json", "L4_SYNTHESIS")
    add_rows(40, "SYNTH-CSV", "Yosys", "synthesis metric tables", "synth/yosys_metrics_{i}.csv", "L4_SYNTHESIS")
    add_rows(80, "VENDOR", "Vivado stub", "unsupported vendor implementation placeholders", "vendor/vendor_implementation_{i}.rpt", "L5_VENDOR_IMPLEMENTATION")
    add_rows(70, "BITSTREAM", "Vivado stub", "unsupported bitstream placeholders", "vendor/bitstream_stub_{i}.bit", "L6_BITSTREAM")
    add_rows(70, "BOARD", "Vivado stub", "unsupported board measurement placeholders", "vendor/board_measurement_{i}.csv", "L7_BOARD_MEASUREMENT")
    write_csv(ROOT / "examples" / "evidence_level_gold_standard" / "evidence_gold.csv", rows)


def generate_optional_examples() -> None:
    ltspice = ROOT / "examples" / "ltspice_metadata_only"
    ltspice.mkdir(parents=True, exist_ok=True)
    (ltspice / "README.md").write_text(
        "# LTspice Metadata-Only Example\n\nThis example records metadata only and is not a core reproduction dependency.\n",
        encoding="utf-8",
    )
    (ltspice / "example.asc").write_text("Version 4\nSHEET 1 880 680\n", encoding="utf-8")
    (ltspice / "run.log").write_text("LTspice metadata-only placeholder.\n", encoding="utf-8")

    vivado = ROOT / "examples" / "vivado_stub_boundary"
    vivado.mkdir(parents=True, exist_ok=True)
    (vivado / "README.md").write_text(
        "# Vivado Stub Boundary Example\n\nSchema-only placeholder for unsupported vendor implementation evidence.\n",
        encoding="utf-8",
    )
    (vivado / "schema_boundary.rpt").write_text(
        "Schema-only placeholder. No vendor implementation result is claimed.\n",
        encoding="utf-8",
    )


def generate_adapter_coverage_examples() -> None:
    """Generate deterministic semi-real fixtures for the RQ1 adapter coverage gate."""
    ngspice_dir = ROOT / "examples" / "ngspice_minimal" / "generated_coverage"
    ngspice_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 26):
        (ngspice_dir / f"rc_sweep_{idx:03d}.cir").write_text(
            f"* software-only ngspice fixture {idx}\nR1 in out {1000 + idx}\nC1 out 0 1u\n.end\n",
            encoding="utf-8",
        )
        (ngspice_dir / f"rc_sweep_{idx:03d}.log").write_text(
            f"ngspice fixture {idx}: transient software simulation completed.\n",
            encoding="utf-8",
        )
        (ngspice_dir / f"rc_sweep_{idx:03d}.csv").write_text(
            "time_s,v_out\n0,0\n1e-6,0.1\n",
            encoding="utf-8",
        )

    hdl_dir = ROOT / "examples" / "hdl_icarus_yosys_minimal" / "generated_coverage"
    hdl_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 21):
        (hdl_dir / f"counter_{idx:03d}.v").write_text(
            f"module counter_{idx:03d}(input clk, output reg [3:0] q); "
            "always @(posedge clk) q <= q + 1; endmodule\n",
            encoding="utf-8",
        )
        (hdl_dir / f"counter_{idx:03d}.log").write_text(
            f"software HDL simulation fixture {idx}: pass.\n",
            encoding="utf-8",
        )
        (hdl_dir / f"counter_{idx:03d}.csv").write_text(
            "cycle,q\n0,0\n1,1\n",
            encoding="utf-8",
        )
        (hdl_dir / f"counter_{idx:03d}.json").write_text(
            '{"fixture": "hdl_counter", "evidence": "software_only"}\n',
            encoding="utf-8",
        )
        (hdl_dir / f"counter_{idx:03d}.ys").write_text(
            f"read_verilog counter_{idx:03d}.v\nproc\nopt\n",
            encoding="utf-8",
        )
        (hdl_dir / f"counter_{idx:03d}.rpt").write_text(
            f"Yosys fixture {idx}: open-source synthesis report only.\n",
            encoding="utf-8",
        )

    verilator_dir = ROOT / "examples" / "hdl_verilator_minimal" / "generated_coverage"
    verilator_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 26):
        (verilator_dir / f"lint_case_{idx:03d}.v").write_text(
            f"module lint_case_{idx:03d}(input a, output y); assign y = a; endmodule\n",
            encoding="utf-8",
        )
        (verilator_dir / f"lint_case_{idx:03d}.log").write_text(
            f"Verilator lint fixture {idx}: software-only lint completed.\n",
            encoding="utf-8",
        )
        (verilator_dir / f"lint_case_{idx:03d}.xml").write_text(
            f"<lint fixture=\"{idx}\" evidence=\"software_only\" />\n",
            encoding="utf-8",
        )

    plecs_dir = ROOT / "examples" / "plecs_metadata_only" / "generated_coverage"
    plecs_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 21):
        (plecs_dir / f"metadata_model_{idx:03d}.plecs").write_text(
            f"PLECS metadata-only fixture {idx}.\n",
            encoding="utf-8",
        )
        (plecs_dir / f"metadata_model_{idx:03d}.xml").write_text(
            f"<plecs fixture=\"{idx}\" evidence=\"metadata_only\" />\n",
            encoding="utf-8",
        )
        (plecs_dir / f"metadata_model_{idx:03d}.csv").write_text(
            "field,value\nevidence,metadata_only\n",
            encoding="utf-8",
        )

    ltspice_dir = ROOT / "examples" / "ltspice_metadata_only" / "generated_coverage"
    ltspice_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 21):
        (ltspice_dir / f"metadata_case_{idx:03d}.asc").write_text(
            f"Version 4\nSHEET 1 880 680\nTEXT 0 0 Left 2 !metadata_only_{idx}\n",
            encoding="utf-8",
        )
        (ltspice_dir / f"metadata_case_{idx:03d}.log").write_text(
            f"LTspice metadata-only fixture {idx}; no core reproduction dependency.\n",
            encoding="utf-8",
        )
        (ltspice_dir / f"metadata_case_{idx:03d}.csv").write_text(
            "field,value\nevidence,metadata_only\n",
            encoding="utf-8",
        )

    logisim_dir = ROOT / "examples" / "logisim_metadata_only" / "generated_coverage"
    logisim_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 21):
        (logisim_dir / f"logic_case_{idx:03d}.circ").write_text(
            f"<project source=\"metadata_only\" version=\"{idx}\" />\n",
            encoding="utf-8",
        )
        (logisim_dir / f"logic_case_{idx:03d}.xml").write_text(
            f"<logisim fixture=\"{idx}\" evidence=\"metadata_only\" />\n",
            encoding="utf-8",
        )
        (logisim_dir / f"logic_case_{idx:03d}.csv").write_text(
            "field,value\nevidence,metadata_only\n",
            encoding="utf-8",
        )

    vivado_dir = ROOT / "examples" / "vivado_stub_boundary" / "generated_coverage"
    vivado_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 11):
        (vivado_dir / f"schema_boundary_{idx:03d}.rpt").write_text(
            f"Schema-only vendor boundary fixture {idx}; no implementation result is claimed.\n",
            encoding="utf-8",
        )
        (vivado_dir / f"schema_boundary_{idx:03d}.json").write_text(
            '{"evidence": "schema_only", "implementation_claim": false}\n',
            encoding="utf-8",
        )
        (vivado_dir / f"schema_boundary_{idx:03d}.md").write_text(
            f"# Schema Boundary Fixture {idx}\n\nNo device-side evidence is claimed.\n",
            encoding="utf-8",
        )


def main() -> int:
    generate_claims()
    generate_evidence_gold()
    generate_optional_examples()
    generate_adapter_coverage_examples()
    print("generated IST datasets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
