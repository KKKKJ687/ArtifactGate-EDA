# IST Current Operation and Codex Execution Packet

Generated: 2026-06-22

This packet is the durable S6/S7 workflow-governor artifact for the current IST
stronger-plan worktree. It updates the original plan's stale artifact names to
the current repository state without expanding the claim boundary.

## S6 Detailed Operation Plan

### Current Artifact Names

The current repository uses these names:

- Baseline execution: `outputs/rq7_baseline/`,
  `reports/rq7_baseline_task_execution.md`,
  `reports/rq7_baseline_task_results.csv`, and
  `reports/rq7_baseline_comparison.md`.
- Ablation: `outputs/rq8_ablation/`, `reports/rq8_ablation.md`,
  `reports/rq8_ablation_results.csv`,
  `reports/rq8_ablation_effect_sizes.csv`, and
  `reports/rq8_ablation_observations.csv`.
- Reviewer dry run: `outputs/rq10_reviewer_walkthrough/`,
  `reports/rq10_reviewer_walkthrough.md`,
  `reports/rq10_reviewer_walkthrough_summary.csv`,
  `reports/rq10_reviewer_walkthrough_observations.csv`, and
  `reports/rq10_reviewer_walkthrough_command_log.csv`.

The stale names `rq8_baseline_*` and `rq10_reviewer_simulation.md` from the
source plan are superseded by the current files above.

### Step Order

| Step | Command or artifact family | Checkpoint |
| --- | --- | --- |
| 1 | `make lint` and `make test` | Static checks and 37 pytest cases pass. |
| 2 | `make ist-all` | RQ0-RQ10, reports, and IST package regenerate. |
| 3 | `make ist-strong-l2` | File inventory, evidence graph, boundary scan, and manuscript claim gate pass. |
| 4 | `make ist-package` | IST archive is rebuilt with private-path payload self-test. |
| 5 | `make preflight` | SoftwareX baseline packaging and release preflight pass with the tightened zip scanner. |
| 6 | `make external-release-check` | Published release and DOI metadata are verified without mutating the v0.1.2 baseline. |
| 7 | Subagent review | Failed gates are reflected and re-reviewed. |

### Verification Plan

| Check family | Required evidence | Runtime ceiling |
| --- | --- | --- |
| Unit and integration checks | `make test`/`make preflight` receipts with 37 collected pytest cases passing. | One full run per correction pass. |
| IST generation | `make ist-all` and `make ist-package` receipts plus zip self-test and payload scan. | One full regeneration per correction pass. |
| L2 gates | `make ist-strong-l2` receipt with inventory, graph, boundary, and manuscript-claim counts. | One full L2 run per correction pass. |
| External release metadata | `make external-release-check` verifies the selected release tag and DOI. | One check after local package or metadata-affecting edits. |
| Subagent review | Read-only S-stage or gate-specific review with score, threshold, pass/fail, flaws, and required revision. | One focused follow-up after each material correction. |

### Local Gate Thresholds and One-Vote-Fail Conditions

| Gate family | Threshold | One-vote-fail condition |
| --- | ---: | --- |
| S0-S3 workflow setup | >=80 | Missing Mega-Tron call, missing skill/resource index evidence, missing forbidden skills/resources, or missing H1 record. |
| S4 claim/objective/boundary | >=85 | Any unverifiable or hardware/Vivado/DFX/bitstream/board positive claim. |
| S5-S8 execution design and execution | >=80 | Unmeasurable gate, missing rollback/verification packet, private-path payload, or protected release mutation. |
| S9-S10 review and iteration | >=80 | Missing numeric score, mentor review, failed-gate reflection, or follow-up revision action. |
| S11 final acceptance | >=90 | Any open G13 author/expert evidence gate. |

### Attempt and Runtime Budget

| Item | Budget |
| --- | --- |
| Local gate rerun attempts before reflection | 2 attempts per failing gate before escalating. |
| Same-gate repeated failure threshold | 3 failures triggers scope reduction, re-routing, or user escalation. |
| Long command budget | Prefer one complete run per command family; avoid repeated polling; use the runtime ceilings in the verification plan. |
| External publication actions | 0 attempts without explicit user approval; the G15 `v0.1.3` release path was explicitly approved. |
| Author/expert evidence fabrication | 0 attempts; not allowed. |

### Rollback Strategy

- Use file-level review and targeted patches for workflow/report/code changes.
- Do not run destructive Git commands.
- Do not move, rewrite, or delete existing external release records.
- If a local edit breaks `make preflight`, `make external-release-check`, or
  `make ist-all`, correct the specific file or revert the specific edit after
  reviewing the diff.

### H3 Hard Stop Record

| Field | Record |
| --- | --- |
| Content to confirm | The current operation plan above replaces stale plan file names with current artifact names. |
| Risk | Executing from stale names would create false missing-artifact or false-pass records. |
| Next step | Prepare Codex execution packet with exact paths, commands, deviations, and release exception. |
| Allowed actions after confirmation | Update local scripts/reports/control files and rerun local verification only. |

## S7 Codex Execution Packet

### Editable Paths

- `.codex_workflow/`
- `docs/`
- `examples/`
- `paper/manuscript_ist.md`
- `paper/manuscript_ist.tex`
- `paper/figures/`
- `paper/tables/`
- `repo/src/artifactgate_eda/`
- `reports/`
- `scripts/`
- `tests/`
- `Makefile`
- `README.md`

### Protected Paths

- Existing external release state, Git tags, GitHub release records, and Zenodo
  records, except the explicitly approved `v0.1.3` G15 release path.
- Existing SoftwareX manuscript author metadata fields unless the author
  supplies values.
- Existing release archives under `release/`.

Named release exceptions:

- The generated local IST archive
  `release/artifactgate_eda_ist_evaluation_artifacts.zip` and normal
  reproducibility zips produced by Make targets may be rebuilt by local Make
  targets. This exception does not permit tag, GitHub release, or Zenodo
  mutation.
- The user explicitly approved G15 external release work; the resulting IST
  release is `v0.1.3` with DOI `10.5281/zenodo.20798200`. This does not permit
  moving or mutating the existing `v0.1.2` SoftwareX baseline release.

### Allowed Commands

- `make lint`
- `make test`
- `make ist-all`
- `make ist-strong-l2`
- `make ist-package`
- `make preflight`
- `make external-release-check`
- direct Python/json/zip inspection commands that do not mutate external state
- read-only subagent reviews

### Expected Artifacts

- `reports/IST_FROZEN_CLAIM_BOUNDARY.md`
- `.codex_workflow/STAGE_CONTROL_PACKET.md`
- `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md`
- `reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md`
- `reports/IST_FINAL_ACCEPTANCE_AUDIT.md`
- `reports/IST_WORKFLOW_GOVERNOR_GATE_LEDGER.md`
- `reports/IST_WORKFLOW_REFLECTION_LOG.md`
- `reports/IST_VERIFICATION_RECEIPTS.json`
- `release/artifactgate_eda_ist_evaluation_artifacts.zip`

### Start Checklist

| Check | Required state |
| --- | --- |
| Branch | Work remains on the current IST upgrade branch. |
| External release | Existing SoftwareX release and DOI are not mutated. |
| Claim boundary | Software-only boundary is frozen. |
| G13 | Real author/expert walkthrough remains open. |
| G15 | New IST release/DOI exists as `v0.1.3` / `10.5281/zenodo.20798200`. |
| Local verification | Use receipts and command output, not intent. |

### Deviation Report Triggers

Current deviation status: none open for local Codex execution; G13 remains open
by design.

- Any need to edit author metadata.
- Any future need to create, move, or delete a tag/release/DOI.
- Any proposed hardware, Vivado, DFX, bitstream, or board claim.
- Any command failure in `make preflight`, `make ist-all`,
  `make ist-strong-l2`, or `make external-release-check`.
- Any package payload containing a local absolute path.

### H4 Hard Stop Record

| Field | Record |
| --- | --- |
| Content to confirm | Codex may execute only the local actions listed in this packet. |
| Risk | Broad execution could mutate protected release state or create unsupported claims. |
| Next step | Execute local checks and record results in receipts and gate ledgers. |
| Allowed actions after confirmation | Local edits, local tests, local package rebuilds, and subagent review. |
| Still forbidden | Unapproved external release/DOI mutation and author-side data fabrication. |
