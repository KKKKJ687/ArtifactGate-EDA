# Workflow Governor Calibration Report

Project: ArtifactGate-EDA IST stronger-plan branch

Generated: 2026-06-22

## Task Type

Research-code, empirical-evaluation, manuscript-package, and release-readiness
workflow for the IST stronger optimization plan.

## Source Of Truth

- Plan: `docs/ist_stronger_plan_source_record.md`
- Current state: `.codex_workflow/WORKFLOW_STATE.md`
- Stage control packet: `.codex_workflow/STAGE_CONTROL_PACKET.md`
- Frozen claim/boundary: `reports/IST_FROZEN_CLAIM_BOUNDARY.md`
- Current operation/execution packet: `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md`
- Gate ledger: `reports/IST_WORKFLOW_GOVERNOR_GATE_LEDGER.md`
- Stage agent audit: `reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md`
- Final acceptance audit: `reports/IST_FINAL_ACCEPTANCE_AUDIT.md`
- Gap audit: `reports/IST_GAP_AUDIT.md`
- Machine receipts: `reports/IST_VERIFICATION_RECEIPTS.json`
- Reflection log: `reports/IST_WORKFLOW_REFLECTION_LOG.md`
- Author/external packet: `docs/ist_author_external_completion_packet.md`

## Frozen Boundary

- Scope is software-only EDA artifact engineering.
- Evidence claims are limited to generated packages, simulations, open-source
  synthesis artifacts, metadata/schema fallback cases, and local software
  verification.
- The IST layer does not claim device-side validation, vendor implementation
  signoff, reconfiguration deployment, board evidence, completed human/expert
  study evidence.
- The existing `v0.1.2` archive and DOI remain the SoftwareX baseline and were
  not mutated; the IST evaluation snapshot is archived separately as `v0.1.3`
  with DOI `10.5281/zenodo.20798200`.

## Selected Skill Summary

Detailed scored skill/resource mapping, forbidden skills/resources, coverage
gap, and H1 record are now durable in
`.codex_workflow/STAGE_CONTROL_PACKET.md`.

This summary mirrors the five selected skills from the scored S3 mapping. It is
not a broader resource list.

| Selected skill | Use |
| --- | --- |
| `workflow_governor` | Boundary freeze, stage contracts, gate design, failure handling, and final acceptance discipline |
| `codex-capability-router` | Local skill, agent, manual, and resource routing before complex project work |
| `research-claim-os` | Evidence/claim separation and human-gate discipline |
| `paper-evidence-auditor` | Claim-to-local-evidence audit and overclaim prevention |
| `journal-submission-auditor` | Author-side metadata, CRediT/declaration, and external release blocker separation |

The seven selected resources are the scored resources in
`.codex_workflow/STAGE_CONTROL_PACKET.md`; generated control artifacts below are
derived outputs, not extra selected resources.

## Gate Standard

Acceptance requires direct evidence from files, generated reports, command
outputs, package contents, or subagent review. A gate is not passed from intent,
unchecked summaries, or unverified generated files.

Status terms:

- `PASS`: Codex-verifiable evidence currently satisfies the gate.
- `PASS_WITH_LIMITATION`: Evidence satisfies a bounded version of the gate and
  the limitation is recorded in the manuscript or audit.
- `AUTHOR_REQUIRED`: A real author or expert action is needed.
- `EXTERNAL_REQUIRED`: A new external archive, tag, DOI, or public state is
  needed.
- `FAIL`: A hard gate is not satisfied; the blocking owner and required
  evidence must be recorded separately.

## Hard Stops

The four workflow-governor hard stops are satisfied for Codex execution because
the user explicitly directed execution of the selected plan. A hard stop remains
active for any future external publication action:

- Do not create, move, or overwrite any tag or release without explicit user
  approval.
- Do not update manuscript data-availability wording with any future DOI until
  that DOI exists and resolves.
- Do not mark G13 complete until real author/expert evidence exists.

Durable hard-stop packets:

- H1: `.codex_workflow/STAGE_CONTROL_PACKET.md`
- H2: `reports/IST_FROZEN_CLAIM_BOUNDARY.md`
- H3 and H4: `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md`

## Blocking Missing Information

- G13: author/expert walkthrough evidence.
