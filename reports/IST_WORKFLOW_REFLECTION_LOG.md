# IST Workflow Reflection Log

Numeric gate and stage scores are maintained in
`reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md`. This reflection log uses
status fields plus root-cause, correction-path, revision-action, new-rule, and
preventive-check fields so that historical entries are not rewritten with
post-hoc scores.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: E6/G9 external case generalization
- Initial review status: PASS_WITH_LIMITATION
- Final review status: PASS
- Failure type: Evidence grounding and claim-boundary wording
- Root cause: The first E6 implementation mixed selection metadata with observed metrics and used "replay" wording that could be read as external EDA tool execution.
- Minimal correction path: Revise current output and rerun the same gate review.
- Revision actions:
  - Added observed `manual_adapter_fix`, hardware-dependency, and commercial-dependency fields derived from adapter detection, ArtifactGate replay/ingest result, validation result, run manifest, and records.
  - Renamed E6 replay metric to ArtifactGate replay-package success and explicitly stated that external EDA tools are not executed by this benchmark.
  - Added `reports/IST_VERIFICATION_RECEIPTS.json` with machine-readable local command receipts.
  - Updated manuscript and audit wording to distinguish ArtifactGate package-level replay/validation from independent EDA tool execution.
- New rule: For empirical gates, report selection metadata separately from observed benchmark evidence.
- Skill/resource change: None.
- Preventive check next time: Ask subagent to inspect whether every threshold metric is computed from observed outputs before accepting a gate.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: E7/G10 scalability to 100k
- Initial review status: PASS_WITH_LIMITATION
- Final review status: PASS_WITH_LIMITATION
- Failure type: Metric scope and measurement semantics
- Root cause: The first 100k scalability extension directly processed synthetic manifest rows, but per-phase runtime and memory labels could be read as independent measurements.
- Minimal correction path: Revise current output and keep the narrower, evidence-supported claim.
- Revision actions:
  - Renamed scalability fields to distinguish measured manifest-processing runtime, allocated phase-time shares, estimated memory, and measured output size.
  - Updated the scalability report, figure, manuscript, audit, and receipts to state that memory values are estimates and that the benchmark is not EDA algorithm performance.
  - Kept G10 as PASS_WITH_LIMITATION instead of full PASS.
- New rule: A performance gate must name whether each metric is directly measured, allocated from a measured aggregate, or estimated.
- Skill/resource change: None.
- Preventive check next time: Require subagent review to inspect metric provenance before a scalability or baseline claim is promoted to full pass.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: E8/G11 baseline execution
- Initial review status: FAIL
- Final review status: PASS_WITH_LIMITATION
- Failure type: Baseline execution evidence was too close to a static capability table.
- Root cause: The first E8 implementation computed task success directly from method capability fields and did not leave per-baseline run artifacts that a reviewer could inspect.
- Minimal correction path: Replace static task scoring with deterministic baseline emulators that write method-specific outputs, then evaluate T1-T8 by reading those outputs.
- Revision actions:
  - Added a shared software-only baseline fixture under `outputs/rq7_baseline/fixture_package`.
  - Generated per-method artifacts under `outputs/rq7_baseline/<method>/`, including detected defects, claim results, replay manifests, claim-evidence tables, reviewer reports, and run receipts where applicable.
  - Rewrote baseline task scoring to inspect generated files rather than using task IDs from a capability set.
  - Updated reports, manuscript wording, IST gap audit crosswalk, verification receipts, and the IST package script to preserve the generated baseline outputs.
  - Reran `make rq7-baseline`, `make lint`, `make test`, `make ist-reports`, `make ist-package`, `make ist-all`, and `make ist-strong-l2`.
- Remaining limitation: The baseline benchmark is a deterministic emulator harness, not independent real-world execution by human reviewers or third-party baseline tools. Manual time remains an operator-step estimate.
- New rule: A baseline comparison gate may pass only if task-level success can be traced to generated artifacts or an explicitly stated limitation keeps the claim below full empirical execution.
- Skill/resource change: None.
- Preventive check next time: Ask subagent to inspect whether task success is derived from output files and whether package artifacts include those outputs before accepting baseline evidence.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: E9/G12 ablation with effect sizes
- Initial review status: FAIL
- Final review status: PASS
- Failure type: Ablation evidence was a static seven-row table without repeated experiment-family observations, confidence intervals, or effect sizes.
- Root cause: The first RQ8 implementation summarized component removals directly at the variant level and allowed the gate to pass from report existence alone.
- Minimal correction path: Expand the ablation to the strong-plan A0-A9 variant set, generate long-form observations for E3/E4/E5/E8, compute effect-size and bootstrap-CI rows, and make tests assert these structures.
- Revision actions:
  - Added 10 ablation variants from `A0_full` through `A9_no_schema_validation`.
  - Generated 32860 deterministic observation rows across E3 claim detection, E4 corrupted-artifact detection, E5 evidence classification, and E8 baseline-task execution.
  - Added per-experiment Cohen's h effect sizes and bootstrap drop confidence intervals in `reports/rq8_ablation_effect_sizes.csv`.
  - Updated RQ8 reports, manuscript wording, gap audit, verification receipts, CLI documentation, experiment contract, and IST package contents.
  - Added integration-test guardrails requiring at least 9 variants, the four experiment families, effect-size/CI fields, and observation rows.
  - Reran `make lint`, `make test`, `make ist-all`, `make ist-strong-l2`, and `make ist-package`.
- Remaining limitation: The ablation is a deterministic software-only harness derived from configured variant rates, not independent reruns of every full experiment family under physically separate implementations.
- New rule: An ablation gate may not pass from a variant summary table alone; it must expose observation-level data, effect-size fields, confidence intervals, and tests that verify the minimum structure.
- Skill/resource change: None.
- Preventive check next time: Ask subagent to inspect both generated evidence and tests before accepting an ablation gate.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: E10/G13 reviewer walkthrough
- Initial review status: FAIL
- Final review status: AUTHOR_REQUIRED
- Failure type: Human/expert gate overclaim
- Root cause: The first RQ10 artifact was a generated dry-run harness with `human_participants=0`, but the gap audit and manuscript wording could be read as a completed structured expert walkthrough.
- Minimal correction path: Keep the generated dry run as preparatory evidence, downgrade G13 to author-required, and remove wording that presents RQ10 as completed expert or human-study evidence.
- Revision actions:
  - Kept `reports/rq10_reviewer_walkthrough_*` as generated dry-run outputs with command timestamps.
  - Changed the generated report, CLI documentation, manuscript wording, gap audit, and receipt language to state that author-side expert walkthrough evidence is still required for G13.
  - Preserved tests that verify `human_participants=0`, command-log fields, and two-condition dry-run structure.
- Remaining limitation: No real author/expert walkthrough or participant study has been supplied, and no measured human timing is claimed.
- New rule: A human/expert gate may not pass from generated dry-run artifacts; it must remain author-required until real author/expert evidence is supplied or the requirement is explicitly waived.
- Skill/resource change: Routed through `research-claim-os` after subagent review.
- Preventive check next time: Ask subagent to classify human-gate artifacts as direct evidence, preparatory dry run, or author-required before any manuscript wording is promoted.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: G0/S9 workflow-governor package and receipt consistency
- Initial review status: FAIL
- Final review status: PASS
- Failure type: Release-package payload hygiene and stale verification receipts
- Root cause: The IST packager copied generated baseline and walkthrough outputs
  into the archive without scanning their payloads for absolute user-path
  strings, and the workflow receipt did not include the latest `make preflight`
  and `make external-release-check` commands.
- Minimal correction path: Sanitize private-path payloads at IST package write
  time, make the packager fail if a private path remains, add release-preflight
  zip payload scanning, and update the receipt/ledger vocabulary.
- Revision actions:
  - Added IST package payload redaction and post-write private-path scanning.
  - Added release-preflight scanning for absolute user paths inside release zip
    payloads, including the IST archive.
  - Added unit tests that fail on private-path zip payloads and preserve the
    intentional supplementary inventory allowlist.
  - Updated `reports/IST_VERIFICATION_RECEIPTS.json`,
    `.codex_workflow/CALIBRATION_REPORT.md`, and the gate ledger to record the
    latest local verification and combined S11 status.
  - Reran `make ist-all`, `make ist-strong-l2`, `make preflight`,
    `make external-release-check`, `make ist-package`, direct release preflight,
    and direct zip payload inspection.
- Remaining limitation: G13 and G15 still require real author/expert and
  external archive actions before final IST acceptance.
- New rule: A package-clean gate must inspect release archive payloads, not only
  repository files and zip entry names.
- Skill/resource change: Used subagent review as the S9 failure detector and a
  second subagent as the follow-up verifier.
- Preventive check next time: Before marking any release-package gate as clean,
  inspect zip payload bytes for local absolute paths and record the command
  receipt that proves the check.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: Package completeness / manuscript Section 10 consistency
- Initial review status: FAIL
- Final review status: PASS
- Failure type: Evidence-package mismatch
- Root cause: The first IST archive did not include all manuscript-listed data
  and report artifacts, so data availability was stronger than the package.
- Minimal correction path: Add only the missing manuscript-listed artifacts to
  the IST package script and rebuild the archive.
- Revision actions:
  - Updated `scripts/package_ist_artifacts.py` to include the missing Section
    10 data/report files.
  - Rebuilt `release/artifactgate_eda_ist_evaluation_artifacts.zip`.
  - Verified 27 / 27 manuscript-listed data/report artifacts in the archive.
  - Recorded the package consistency follow-up review in the gate ledger.
- Remaining limitation: The IST archive is still local until G15 creates a new
  external release and DOI.
- New rule: A data-availability claim must be checked against the package
  payload, not only against files present in the worktree.
- Skill/resource change: None.
- Preventive check next time: Compare manuscript data-availability lists with
  archive member names before accepting a package gate.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: Release-preflight claim-boundary rule
- Initial review status: FAIL
- Final review status: PASS
- Failure type: Boundary scanner exemption too broad
- Root cause: Positive claim surfaces were initially allowed too broadly,
  allowing boundary-sensitive wording to bypass the release-preflight scanner.
- Minimal correction path: Replace blanket file allowlists with line-scoped
  boundary-context checks and add unit tests.
- Revision actions:
  - Tightened `scripts/release_preflight.py` so positive claim surfaces require
    nearby limitation/boundary markers.
  - Added unit tests for positive overclaim rejection and explicit limitation
    allowance.
  - Reran release preflight, `make preflight`, and follow-up subagent review.
- Remaining limitation: The scanner is a guardrail, not a substitute for human
  domain review.
- New rule: Boundary-sensitive wording in manuscript/README surfaces may pass
  only when local context marks it as limitation, unsupported, or non-claim.
- Skill/resource change: None.
- Preventive check next time: Add a failing fixture before relaxing any
  claim-boundary allowlist.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: Workflow-governor S0-S11 per-stage agent audit
- Initial review status: FAIL
- Final review status: PASS_WITH_LIMITATION
- Failure type: Durable governance evidence missing
- Root cause: Earlier workflow-governor evidence recorded pass/fail status but
  did not provide every stage's required score, threshold, critical flaws,
  revision actions, hard-stop records, and mentor-review packet.
- Minimal correction path: Add explicit control packets and audits without
  changing experiment claims.
- Revision actions:
  - Added `.codex_workflow/STAGE_CONTROL_PACKET.md` for S0-S3.
  - Added `reports/IST_FROZEN_CLAIM_BOUNDARY.md` for S4.
  - Added `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md` for S6/S7.
  - Added `reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md` for S9 and
    mentor review.
  - Added `reports/IST_FINAL_ACCEPTANCE_AUDIT.md` for S11 verified/inferred/
    unchecked state.
- Remaining limitation: S11 remains failed until G13 and G15 are completed by
  real author/external action; the local S0-S10 governance evidence is
  agent-reviewed and passing.
- New rule: A workflow-governor stage cannot be marked pass from a summary row;
  it needs a durable score, threshold, evidence, flaws, and revision-action
  record.
- Skill/resource change: Keep `workflow_governor`, `paper-evidence-auditor`,
  `codex-capability-router`, and subagent review active for final gate audits.
- Preventive check next time: Before a final answer, run a per-stage audit
  against `stage_contracts.md` and `gate_standard.md`.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: S3 skill-resource mapping follow-up audit
- Initial review status: FAIL
- Final review status: PASS
- Failure type: Skill/resource traceability and frozen-mapping drift
- Root cause: The S3 packet had scored mapping rows, but the exact index names,
  rule-complete forbidden-skills table, high-risk Mega-Tron not-adopted record,
  and derivative mapping summaries were still not sufficiently synchronized.
- Minimal correction path: Revise the S3 control packet and derivative summaries
  only; do not reopen experiments, external release state, or author/expert
  gates.
- Revision actions:
  - Added exact skill, resource, resource-library, and agent index identifiers
    under the non-private `CODEX_RESOURCE_ROOT` marker to
    `.codex_workflow/STAGE_CONTROL_PACKET.md`.
  - Added a rule-complete forbidden-skills table with name, reason, misuse
    scenario, and alternative fields.
  - Added a high-risk not-adopted record for approval-gated/autoresearch style
    candidates.
  - Resynchronized `.codex_workflow/CALIBRATION_REPORT.md` and
    `.codex_workflow/WORKFLOW_STATE.md` so they do not broaden the scored S3
    mapping.
  - Reran `make ist-package`, `make ist-strong-l2`, `make preflight`,
    `make external-release-check`, and direct zip payload inspection.
- Remaining limitation: G13 and G15 still require real author/external action,
  and S11 remains failed until real G13/G15 evidence exists.
- New rule: Derivative workflow summaries must mirror the frozen scored mapping
  instead of introducing unscored skills, resources, or reviewers as selected
  items.
- Skill/resource change: No selected skill/resource change; only rejected
  high-risk candidates were recorded more explicitly.
- Preventive check next time: Before marking S3 pass, check exact index evidence,
  selected count limits, forbidden skills/resources, high-risk not-adopted
  records, and derivative-summary synchronization together.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: G13/G15 author-external closure packet readiness
- Initial review status: FAIL
- Final review status: PASS
- Failure type: Author/external operational ambiguity
- Root cause: The author/external packet separated G13 and G15 correctly, but it
  did not contain one explicit post-update rerun/refresh sequence, and the G13
  walkthrough schema left signoff, mandatory columns, exact review materials,
  and unmeasured timing values too implicit.
- Minimal correction path: Clarify the packet only; do not fabricate evaluator
  data, author metadata, release tags, DOI records, or external state.
- Revision actions:
  - Added a minimum current-file checklist for the manual-package and
    ArtifactGate-package review conditions.
  - Added a minimum required observation CSV schema and command-log schema.
  - Defined evaluator attestation/signoff as a typed evaluator ID/role/date and
    task-performance statement, not as ethics approval or device-side evidence.
  - Added the `elapsed_seconds=NA` rule unless timing is directly measured.
  - Added the required closure rerun sequence, state/audit files to refresh, and
    required read-only subagent re-review after real G13/G15 updates.
- Remaining limitation: No real G13 walkthrough evidence or new G15 release/DOI
  exists yet.
- New rule: Author/external gate packets must be executable without inferring
  mandatory schema fields, timing basis, review materials, or rerun sequence.
- Skill/resource change: Used `journal-submission-auditor` as a read-only packet
  reviewer; no selected workflow skill/resource changed.
- Preventive check next time: Ask a submission-readiness subagent to review any
  author/external packet before treating it as ready for handoff.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: G15 external IST release and DOI closure
- Initial review status: EXTERNAL_REQUIRED
- Final review status: PASS_WITH_G13_OPEN
- Failure type: External archive state not yet created
- Root cause: Before explicit user approval, the IST package could only be
  verified locally; it could not be assigned a new public DOI without changing
  external release state.
- Minimal correction path: Create a new versioned IST release without moving or
  mutating the existing `v0.1.2` SoftwareX baseline archive.
- Revision actions:
  - Created and published GitHub release `v0.1.3` for the IST evaluation
    snapshot.
  - Verified Zenodo version DOI `10.5281/zenodo.20798200` at
    `https://zenodo.org/records/20798200`.
  - Updated citation metadata, data-availability wording, and workflow-governor
    state files to record G15 as externally verified.
  - Kept G13 as `AUTHOR_REQUIRED` because no real author/expert walkthrough
    evidence has been supplied.
- Remaining limitation: S11 remains failed until G13 is completed by real
  author/expert action and re-reviewed.
- New rule: A DOI can close an external archive gate only after the public
  record resolves and local metadata names the exact DOI.
- Skill/resource change: No selected workflow skill/resource change.
- Preventive check next time: After a DOI is created, rerun
  `make preflight`, `make ist-strong-l2`, `make ist-package`, and the explicit
  `external_release_check.py --tag <tag> --doi <doi>` command before updating
  final acceptance.

## Reflection Log Entry

- Date: 2026-06-22
- Project: ArtifactGate-EDA IST stronger-plan execution
- Gate: Post-G15 package and metadata consistency
- Initial review status: FAIL
- Final review status: PASS_WITH_G13_OPEN
- Failure type: Package wording and supplementary-report drift
- Root cause: The v0.1.3 DOI refresh updated primary metadata first, but
  supplementary-package reports still contained v0.1.2 wording in current-state
  positions, and packaged documentation contained literal macOS metadata tokens
  that could be misread by content-level payload scans.
- Minimal correction path: Update packaged reports and docs only; preserve
  v0.1.2 as historical baseline evidence and do not mutate the v0.1.2 external
  archive.
- Revision actions:
  - Updated `reports/COMPLETION_AUDIT.md`, `reports/GATE_REVIEW.md`,
    `docs/softwarex_submission_checklist.md`, and `docs/release_readiness.md`
    to use `v0.1.3` / `10.5281/zenodo.20798200` for current release metadata
    while retaining v0.1.2 only as a historical baseline note.
  - Reworded packaged hygiene descriptions to avoid literal macOS metadata
    token hits in archive payloads.
  - Rebuilt `release/artifactgate_eda_ist_evaluation_artifacts.zip` and
    `release/artifactgate_eda_supplementary_artifacts.zip`.
  - Reran `make preflight`, `make ist-strong-l2`, `make ist-package`,
    `scripts/release_preflight.py`, `make external-release-check`, JSON
    validation, and direct zip payload scans.
- Remaining limitation: G13 remains `AUTHOR_REQUIRED`; no real author/expert
  walkthrough evidence has been supplied.
- New rule: After external DOI updates, scan shipped archive payload text for
  stale current-state DOI wording and private-path/resource-fork token hits, not
  only for bad archive member names.
- Skill/resource change: No selected workflow skill/resource change.
- Preventive check next time: Run a read-only package consistency agent before
  committing any DOI-refresh release snapshot.
