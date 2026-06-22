# ArtifactGate-EDA

## What Is ArtifactGate-EDA?

ArtifactGate-EDA is an open-source, adapter-based artifact evaluation framework
for software-only EDA experiments. It standardizes artifact ingestion,
provenance hashing, replay manifest generation, evidence-level classification,
reproducibility checking, unsupported-claim reporting, and reviewer-ready report
generation across bounded SPICE/ngspice, HDL simulation, and Yosys synthesis
workflows.

ArtifactGate-EDA is not another EDA experiment result. It is a reusable
software layer that makes EDA experiment artifacts claim-safe,
replay-checkable, and reviewer-auditable.

## What It Does Not Claim

This software does not validate hardware, Vivado timing, DFX deployment, bitstreams, or board-level behavior.

## Installation

```bash
make install
.venv/bin/artifactgate --version
```

## Quick Start

```bash
make install
.venv/bin/artifactgate --version
make smoke
make ingest-all
make reproduce-core
make negative-claims
make corrupted-tests
make scalability
make baseline
make package-release
```

## CLI Reference

The core commands are:

```text
artifactgate ingest
artifactgate validate
artifactgate replay
artifactgate claim-check
artifactgate report
artifactgate package
artifactgate compare
```

Each command supports `--help`, `--json`, and `--out` where applicable.

Detailed command notes are in `docs/cli_reference.md`. API and schema notes are
in `docs/api_reference.md` and `docs/schema_reference.md`.

## Supported Adapters

Core adapters:

- `ngspice`
- `icarus`
- `yosys`
- `verilator`

Supplementary adapters:

- `plecs` metadata-only
- `logisim` metadata-only
- `ltspice` optional metadata-only
- `vivado_stub` schema-only and unsupported-boundary oriented

## Evidence Levels

The SoftwareX core may make positive claims only up to `L4_SYNTHESIS`.
`L5_VENDOR_IMPLEMENTATION`, `L6_BITSTREAM`, and `L7_BOARD_MEASUREMENT` are
unsupported in the current core package.

## Claim Checking Policy

Claim checking uses `repo/src/artifactgate_eda/policies/forbidden_claims.yaml`,
`evidence_levels.yaml`, `required_evidence_rules.yaml`, and
`safe_rewrite_rules.yaml`. The policy classifies statements as directly
supported, partial, inference, schema-only, blocked, or unsupported, and writes
reviewer-readable ledgers plus JSON reports.

## Reproducibility Commands

```bash
make smoke
make ingest-all
make reproduce-core
make negative-claims
make corrupted-tests
make scalability
make baseline
make package-release
```

Use `make preflight` before release or submission-package checks.

## Examples

The repository includes bounded ngspice, HDL/Icarus, Yosys, Verilator,
PLECS metadata-only, Logisim metadata-only, negative claim, corrupted artifact,
and scalability examples.

## Tests

Run:

```bash
make test
make preflight
```

## Citation

Use `CITATION.cff` for software citation metadata. Archived release DOI:
10.5281/zenodo.20789516.

## License

Apache-2.0.

## Limitations

ArtifactGate-EDA checks artifact-level support for stated claims. It does not
prove circuit correctness, exhaustive HDL verification, Vivado implementation,
DFX partition compatibility, hardware behavior, or real FPGA performance.
