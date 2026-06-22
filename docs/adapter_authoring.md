# Adapter Authoring

Adapters convert heterogeneous EDA experiment directories into a common
ArtifactGate-EDA artifact index. An adapter is intentionally small: it declares
which file extensions belong to a workflow and how those files should be
classified.

## Adapter Responsibilities

Each adapter must:

- discover accepted files under a case directory
- ignore repository metadata, Python cache files, and macOS metadata sidecars
- assign an `artifact_type`
- compute SHA-256
- record a tool name and tool-version field
- assign an evidence level
- mark unsupported evidence boundaries
- keep paths relative to the package root

## Built-In Adapters

| Adapter | Evidence role | Core reproducibility dependency |
|---|---|---|
| `ngspice` | SPICE source and simulation outputs. | Core software-only example. |
| `icarus` | Verilog source and Icarus/VVP simulation outputs. | Core software-only example. |
| `yosys` | RTL source and open synthesis logs/reports. | Core software-only example. |
| `verilator` | HDL source and Verilator simulation-style outputs. | Core software-only example. |
| `plecs` | Power-electronics model metadata. | Supplementary metadata-only. |
| `logisim` | Educational digital-logic circuit metadata. | Supplementary metadata-only. |
| `ltspice` | Optional LTspice-style metadata. | Optional; not required for core reproducibility. |
| `vivado_stub` | Schema-only boundary marker. | Unsupported-boundary documentation only. |

PLECS, LTspice, Vivado, Codex, and MCP are not required for core
reproducibility.

## Evidence Ceiling

Adapter authors must not promote evidence beyond what the files prove.

- Simulation logs and CSVs can reach `L3_SIMULATION`.
- Yosys reports can reach `L4_SYNTHESIS`.
- Vendor implementation, bitstream, and board evidence are unsupported in the
  current SoftwareX package.

The correct behavior for a Vivado-like extension in this package is to classify
it as schema-only or unsupported-boundary evidence unless real vendor
implementation artifacts are deliberately added in a future, separately gated
release.

## Adding An Adapter

1. Add the adapter name and accepted extensions in `ADAPTER_EXTENSIONS`.
2. Add a user-facing tool name in `tool_name`.
3. Extend `evidence_level` only if the adapter introduces a defensible evidence
   category.
4. Add an example under `examples/`.
5. Add or update tests and `make ingest-all` if the adapter is part of the core
   SoftwareX matrix.
6. Run `make preflight`.

Do not add a new adapter by weakening the claim-safety policy. The adapter
should describe what the artifacts prove, and the claim checker should continue
to reject unsupported escalation.
