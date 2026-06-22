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
| `artifactgate benchmark` | Run IST empirical evaluation suites for reports, external cases, scalability, corrupted cases, baseline comparison, backend audit, and reviewer dry-run preparation. | RQ reports and CSV metrics |
| `artifactgate ablate` | Run the IST component ablation study. | `rq8_ablation.md`, `rq8_ablation_results.csv`, `rq8_ablation_effect_sizes.csv`, `rq8_ablation_observations.csv` |

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

### Benchmark

```bash
artifactgate benchmark \
  --suite scalability \
  --repo . \
  --out outputs/rq6_scalability \
  --reports reports \
  --repeats 5 \
  --json
```

Supported suites are `repository`, `corrupted`, `evidence`, `external`,
`scalability`, `baseline`, `local-backends`, `reviewer-walkthrough`,
`reports`, and `all`.

Reviewer dry-run suite:

```bash
artifactgate benchmark \
  --suite reviewer-walkthrough \
  --repo . \
  --out outputs/rq10_reviewer_walkthrough \
  --reports reports
```

The reviewer dry run emits `rq10_reviewer_walkthrough.md`, observation rows, a
condition summary, and a command log. It prepares material for an author-side
expert walkthrough; it is not itself expert-walkthrough evidence, a
multi-participant human study, or a measured human timing result.

### Ablate

```bash
artifactgate ablate \
  --out outputs/rq8_ablation \
  --reports reports \
  --json
```

The ablation command compares the full method against ten controlled variants
over deterministic E3/E4/E5/E8 observation rows and reports effect sizes plus
bootstrap confidence intervals. It remains a software-only evaluation and does
not execute external EDA tools or claim hardware evidence.

## Makefile Entry Points

| Target | Purpose |
|---|---|
| `make smoke` | Install-path smoke test with ngspice example and negative claim check. |
| `make ingest-all` | Run all core and supplementary adapter ingestion examples. |
| `make reproduce-core` | Generate replay packages and replay reports. |
| `make negative-claims` | Verify forbidden claims are detected. |
| `make corrupted-tests` | Verify corrupted examples fail with expected codes. |
| `make scalability` | Generate legacy 1k, 3k, 5k, and 10k synthetic scalability outputs. |
| `make baseline` | Generate artifact-management baseline comparison. |
| `make rq1-ingest-all` | Run IST RQ1 adapter ingestion cases. |
| `make rq2-replay-core` | Run IST RQ2 replay cases. |
| `make rq3-negative-claims` | Run the 300+ claim-injection dataset. |
| `make rq4-corrupted-artifacts` | Run the 30-class corrupted-artifact suite with clean specificity cases. |
| `make rq5-evidence-classification` | Evaluate the evidence-level gold standard. |
| `make rq6-external-cases` | Prepare and evaluate 10 public software-only external EDA cases. |
| `make rq6-scalability` | Run extended scalability trials up to 100k synthetic manifest rows. |
| `make rq7-baseline` | Generate the IST baseline comparison. |
| `make rq8-ablation` | Generate the IST ablation study. |
| `make rq9-local-backends` | Audit optional local backend availability and fallback status. |
| `make rq10-reviewer-walkthrough` | Generate the reviewer dry-run report and command log for author-side walkthrough preparation. |
| `make ist-all` | Run the IST empirical evaluation command chain and generate summary reports. |
| `make package-release` | Build core release capsules. |
| `make supplementary-package` | Build the SoftwareX supplementary artifact zip. |
| `make dist-package` | Build Python sdist and wheel artifacts. |
| `make preflight` | Run the full local release gate. |
