# API Reference

ArtifactGate-EDA is primarily a command-line tool, but the CLI is backed by a
small Python API under `artifactgate_eda.core.artifact`. The API is intentionally
plain-Python and file-oriented so that external reviewers can inspect the
contract without needing a service, database, or commercial EDA installation.

## Data Model

`ArtifactRecord` is the central record type. Each generated artifact index row
contains:

| Field | Meaning |
|---|---|
| `artifact_id` | Stable adapter-local identifier. |
| `relative_path` | Path relative to the output artifact package. |
| `artifact_type` | File classification such as `spice_netlist`, `tool_log`, `verilog_source`, or `synthesis_report`. |
| `sha256` | SHA-256 digest for drift and integrity checks. |
| `size_bytes` | File size at indexing time. |
| `tool` | Tool family or metadata adapter name. |
| `tool_version` | Recorded version field or metadata-only sentinel. |
| `adapter` | Adapter name. |
| `evidence_level` | Evidence layer such as `L3_SIMULATION` or `L4_SYNTHESIS`. |
| `claim_binding` | Claim/evidence binding marker. |
| `unsupported_boundary` | Explicit boundary such as `not_vivado_timing_or_bitstream`. |
| `created_by_command` | Reproduction command label. |

## Public Functions

### `ingest_artifacts(root, adapter, out_dir)`

Indexes a case directory, copies accepted artifacts into `out_dir/raw_artifacts`,
computes hashes, assigns evidence levels, and writes:

- `artifact_index.json`
- `artifact_index.csv`
- `provenance.json`

Returns a result dictionary with `ok`, `status`, `summary`, `out`, and `errors`.

### `validate_artifacts(target, out_dir=None)`

Validates an artifact index or package directory. It checks:

- missing artifact files
- SHA-256 drift
- missing evidence levels
- missing tool-version fields
- broken claim bindings
- non-portable local user paths

When `out_dir` is provided it writes `validation_report.json` and
`validation_report.md`.

### `replay_case(root, adapter, out_dir, full=False)`

Creates a software-only replay package for an example case. It writes a run
manifest, resolved replay manifest, replay summary, replay acceptance report,
claim policy, unsupported ledger, and validation report.

### `claim_check(claims_path, artifact_index, policy_path, out_dir)`

Checks text claims against forbidden-claim policy groups and the maximum
available evidence level in the artifact index. It writes:

- `claim_check_report.json`
- `claim_evidence_table.md`
- `unsupported_ledger.md`
- `safe_rewrite_suggestions.md`

The current implementation is deliberately conservative: hardware, Vivado,
DFX, bitstream, board-level, industrial-deployment, and real-performance claims
are reported as unsupported unless matching higher evidence levels are present.
The SoftwareX package does not include those higher evidence levels.

### `render_report(target, out_path, fmt)`

Generates a reviewer-readable Markdown report for an artifact package.

### `package_capsule(target, out_path)`

Builds a zipped artifact capsule. If required review files are missing from the
target, conservative placeholder files are added so the capsule remains
inspectable.

### `compare_outputs(left, right, out_dir)`

Compares two output directories and writes `drift_report.csv` with
`ADDED_ARTIFACT`, `REMOVED_ARTIFACT`, and `HASH_DRIFT` rows.

### `benchmark_scale(base, scale, out_dir)`

Generates synthetic scalability outputs for artifact-row counts used in the
SoftwareX experiment matrix.

### `render_baseline_report(out_path)`

Generates the baseline comparison table that contrasts ArtifactGate-EDA with
manual zip, shell-script, checksum-manifest, and generic repository-release
artifact-management baselines.

### `render_experiment_summaries(repo_root, reports_dir)`

Aggregates generated outputs into report CSV/Markdown files for the E1-E6
experiment sections.

## Result Contract

API functions return dictionaries suitable for CLI JSON output:

```json
{
  "ok": true,
  "status": "PASS",
  "summary": "human-readable status",
  "out": "path/to/output",
  "errors": []
}
```

Validation and claim-check failures set `ok` to `false` and include structured
error rows with a `code` and `message`.
