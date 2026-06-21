# CLI Reference

ArtifactGate-EDA exposes the `artifactgate` command after installation.

```bash
make install
.venv/bin/artifactgate --version
```

All core commands provide `--help` and machine-readable `--json` output.
Commands that write files accept `--out`.

## Core Commands

| Command | Purpose | Typical output |
|---|---|---|
| `artifactgate ingest` | Index artifacts, copy them into a package directory, compute hashes, and assign evidence levels. | `artifact_index.json`, `artifact_index.csv`, `provenance.json` |
| `artifactgate validate` | Validate artifact paths, hashes, evidence levels, tool-version fields, and claim bindings. | `validation_report.json`, `validation_report.md` |
| `artifactgate replay` | Rebuild a software-only replay package for an example case. | `run_manifest.json`, `replay_summary.csv`, `replay_acceptance_report.md` |
| `artifactgate claim-check` | Check claims against forbidden-claim and evidence-level policy rules. | `claim_check_report.json`, `claim_evidence_table.md`, `unsupported_ledger.md` |
| `artifactgate report` | Render a reviewer-readable artifact report. | Markdown report |
| `artifactgate package` | Create a zipped artifact capsule with required review files. | release zip |
| `artifactgate compare` | Compare two output directories for artifact drift. | `drift_report.csv` |

The repository also includes helper commands used by the Makefile:
`benchmark-scale`, `report-baseline`, and `summarize`.

## Examples

### Ingest

```bash
artifactgate ingest examples/ngspice_minimal \
  --adapter ngspice \
  --out outputs/ngspice_minimal \
  --json
```

Required arguments:

- `root`: input case directory.
- `--adapter`: adapter name, such as `ngspice`, `icarus`, `yosys`,
  `verilator`, `plecs`, `logisim`, `ltspice`, or `vivado_stub`.
- `--out`: output directory.

### Validate

```bash
artifactgate validate outputs/ngspice_minimal/artifact_index.json \
  --out outputs/ngspice_minimal \
  --json
```

Validation failures return a nonzero exit code unless `--expect-fail CODE`
matches an observed error code. Supported gate codes include
`MISSING_ARTIFACT`, `HASH_MISMATCH`, `MISSING_EVIDENCE_LEVEL`,
`BROKEN_CLAIM_REFERENCE`, `NON_PORTABLE_PATH`, and `MISSING_TOOL_VERSION`.

### Replay

```bash
artifactgate replay examples/hdl_icarus_yosys_minimal \
  --adapter icarus \
  --out outputs/replay_icarus \
  --smoke
```

`--smoke` is used for CI-style replay. `--full` marks a fuller supplementary
package mode. Core replay does not require commercial EDA software.

### Claim Check

```bash
artifactgate claim-check \
  --claims examples/negative_claim_cases/claims.md \
  --artifact-index outputs/e1_ngspice/artifact_index.json \
  --policy repo/src/artifactgate_eda/policies/forbidden_claims.yaml \
  --out outputs/e3_negative_claims \
  --expect-fail UNSUPPORTED_CLAIM
```

The claim checker reports unsupported claims and evidence-level escalations.
The SoftwareX core boundary is software-only evidence up to `L4_SYNTHESIS`.

### Report

```bash
artifactgate report outputs/replay_ngspice \
  --format markdown \
  --out reports/replay_ngspice.md
```

### Package

```bash
artifactgate package outputs/replay_ngspice \
  --out release/ngspice_minimal_artifactgate.zip
```

Release capsules include the artifact index, run manifest, claim policy,
validation report, replay report, unsupported ledger, raw artifacts, and a
README file.

### Compare

```bash
artifactgate compare outputs/replay_ngspice outputs/replay_icarus \
  --out outputs/drift_report \
  --json
```

The compare command reports added, removed, and hash-drifted files.

## Makefile Entry Points

| Target | Purpose |
|---|---|
| `make smoke` | Install-path smoke test with ngspice example and negative claim check. |
| `make ingest-all` | Run all core and supplementary adapter ingestion examples. |
| `make reproduce-core` | Generate replay packages and replay reports. |
| `make negative-claims` | Verify forbidden claims are detected. |
| `make corrupted-tests` | Verify corrupted examples fail with expected codes. |
| `make scalability` | Generate 1k, 3k, 5k, and 10k synthetic scalability outputs. |
| `make baseline` | Generate artifact-management baseline comparison. |
| `make package-release` | Build core release capsules. |
| `make supplementary-package` | Build the SoftwareX supplementary artifact zip. |
| `make dist-package` | Build Python sdist and wheel artifacts. |
| `make preflight` | Run the full local release gate. |
