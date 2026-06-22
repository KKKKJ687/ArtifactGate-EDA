# Reproducibility

ArtifactGate-EDA is designed to be reproducible through local Makefile and CLI
commands. The core path does not require Codex, MCP, Vivado, PLECS, LTspice, or
board access.

## Environment

```bash
python3 --version
make install
.venv/bin/artifactgate --version
```

The package requires Python 3.10 or newer. Development dependencies are declared
in `pyproject.toml`.

## Core Reproduction

```bash
make smoke
make ingest-all
make reproduce-core
make negative-claims
make corrupted-tests
make rq6-external-cases
make scalability
make baseline
make summaries
```

These commands regenerate the E0-E6 local experiment evidence:

| Experiment | Command | Evidence |
|---|---|---|
| E0 smoke | `make smoke` | basic ingest, validate, and claim-check path |
| E1 multi-adapter ingestion | `make ingest-all` | ngspice, Icarus, Yosys, Verilator, PLECS metadata, Logisim metadata |
| E2 replay reproducibility | `make reproduce-core` | replay manifests and acceptance reports |
| E3 negative claim injection | `make negative-claims` | unsupported-claim ledgers and claim table |
| E4 corrupted artifacts | `make corrupted-tests`; IST extension: `make rq4-corrupted-artifacts` | expected failures plus the 30-class corruption benchmark |
| E5 scalability | `make scalability`; IST extension: `make rq6-scalability` | synthetic manifest processing up to 100k rows in the IST extension |
| E6 external cases | `make rq6-external-cases` | 10 public software-only EDA cases with 8 open-source ArtifactGate replay-package/validation cases |
| E7 baseline comparison | `make baseline` | artifact-management comparison table |

## Release Preflight

Run the full local gate before public release:

```bash
make preflight
```

This target runs linting, tests, all local experiments, report generation,
figure generation, manuscript package mapping, release capsule generation,
supplementary package generation, Python sdist/wheel generation, and final
release preflight checks.

## Generated Artifacts

Important generated outputs include:

- `outputs/*` replay and claim-check working outputs
- `reports/*.csv` and `reports/*.md`
- `paper/figures/*.png`
- `release/*_artifactgate.zip`
- `release/artifactgate_eda_supplementary_artifacts.zip`
- `dist/artifactgate_eda-0.1.3.tar.gz`
- `dist/artifactgate_eda-0.1.3-py3-none-any.whl`

Generated release and distribution artifacts are ignored by Git and should be
rebuilt from source after checkout.

## Boundary

Passing these commands proves local software-package reproducibility and
claim-safety behavior. It does not prove hardware-level acceptance, vendor
timing, DFX runtime use, bitstream creation, board-level behavior, FPGA
performance, or energy measurements.
