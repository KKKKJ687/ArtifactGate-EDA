# Schema Reference

JSON schema files are stored under
`repo/src/artifactgate_eda/schemas/`. They document the stable file contracts
used by the CLI, reports, and release capsules.

## Schema Files

| File | Contract |
|---|---|
| `artifact_schema.json` | Artifact index row fields, including hash, tool, adapter, evidence level, and claim boundary metadata. |
| `run_manifest_schema.json` | Replay manifest fields, including command list and hardware/commercial dependency flags. |
| `evidence_level_schema.json` | Evidence-level labels from metadata/source evidence through board measurement. |
| `claim_policy_schema.json` | Forbidden-claim policy groups and safe rewrite messages. |
| `adapter_schema.json` | Adapter metadata, supported extensions, and replayability markers. |

## Artifact Index

An artifact index is generated as both CSV and JSON. Required record fields are:

```text
artifact_id
relative_path
artifact_type
sha256
size_bytes
tool
tool_version
adapter
evidence_level
claim_binding
unsupported_boundary
created_by_command
```

Paths must be relative to the package directory. Local user paths and macOS
resource fork files are rejected by the local gates.

## Evidence Levels

The policy files define the software evidence ceiling used by the SoftwareX
package:

| Level | Meaning | Current SoftwareX use |
|---|---|---|
| `L0_METADATA` | Metadata-only artifact. | Supplementary adapter evidence. |
| `L1_SOURCE_EXISTS` | Source or model file exists and is indexed. | SPICE/HDL/Yosys source files. |
| `L2_REFERENCE_OR_INTERFACE` | Interface or reference-level artifact. | Limited supporting evidence. |
| `L3_SIMULATION` | Software simulation output. | ngspice, Icarus, Verilator outputs. |
| `L4_SYNTHESIS` | Open synthesis output. | Yosys reports and logs. |
| `L5_VENDOR_IMPLEMENTATION` | Vendor implementation evidence. | Unsupported in current core. |
| `L6_BITSTREAM` | Bitstream evidence. | Unsupported in current core. |
| `L7_BOARD_MEASUREMENT` | Board measurement evidence. | Unsupported in current core. |

Claims above `L4_SYNTHESIS` are outside the current package boundary.

## Claim Policy

`forbidden_claims.yaml` groups unsafe wording into policy families such as:

- hardware or board-level acceptance claims
- vendor timing or implementation claims
- bitstream generation or verification
- DFX runtime/use claims or partial reconfiguration claims
- real FPGA performance or energy measurement claims
- broad universal-framework claims

Each group provides a safe rewrite message used in generated ledgers.

## Capsule Contract

Release capsules produced by `artifactgate package` are checked for:

```text
artifact_index.json
run_manifest.json
claim_policy.yaml
validation_report.md
replay_acceptance_report.md
unsupported_ledger.md
README.md
```

The supplementary package is checked separately by
`scripts/release_preflight.py`.
