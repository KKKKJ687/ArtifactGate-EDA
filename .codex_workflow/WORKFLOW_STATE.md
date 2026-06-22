# Workflow State

Project: ArtifactGate-EDA IST stronger-plan branch

Updated: 2026-06-22

## Current Stage

S11 Final Acceptance audit / Awaiting G13 author/expert evidence.

The Codex-verifiable engineering, manuscript-package, reproducibility, and
claim-boundary gates are passing in the current worktree, including the
workflow-governor S0-S10 local repair loop. G15 has a new `v0.1.3` release and
Zenodo DOI, but the full IST stronger-plan objective is not complete because
G13 requires real author or expert action.

## Confirmed Flags

| Flag | Status |
| --- | --- |
| Skill/resource routing performed | confirmed |
| Claim/objective/boundary frozen | confirmed |
| Codex execution authorized by user | confirmed |
| Local IST experiments generated | confirmed |
| Local package rebuilt | confirmed |
| Subagent review used for failure and final checks | confirmed |
| Dedicated per-stage subagent coverage recorded in stage audit | confirmed |
| Author/expert walkthrough completed | not confirmed |
| New IST DOI created | confirmed: `10.5281/zenodo.20798200` |

## Selected Skills

- `workflow_governor`
- `codex-capability-router`
- `research-claim-os`
- `paper-evidence-auditor`
- `journal-submission-auditor`

## Selected Resources

- `docs/ist_stronger_plan_source_record.md`
- `workflow_governor/stage_contracts.md`
- `workflow_governor/gate_standard.md`
- `workflow_governor/mentor_agents.md` and `workflow_governor/failure_handling.md`
- `.codex_workflow/WORKFLOW_STATE.md`
- `reports/IST_GAP_AUDIT.md` and `reports/IST_VERIFICATION_RECEIPTS.json`
- `docs/ist_author_external_completion_packet.md`

## Derived Local Control Artifacts

- `.codex_workflow/STAGE_CONTROL_PACKET.md`
- `reports/IST_FROZEN_CLAIM_BOUNDARY.md`
- `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md`
- `reports/IST_WORKFLOW_REFLECTION_LOG.md`
- `reports/IST_WORKFLOW_GOVERNOR_GATE_LEDGER.md`
- `reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md`
- `reports/IST_FINAL_ACCEPTANCE_AUDIT.md`
- `release/artifactgate_eda_ist_evaluation_artifacts.zip`

## Hard Stop Records

| Hard stop | Durable record | Status |
| --- | --- | --- |
| H1 Skill-resource mapping | `.codex_workflow/STAGE_CONTROL_PACKET.md` | confirmed for local Codex execution |
| H2 Claim/objective/boundary | `reports/IST_FROZEN_CLAIM_BOUNDARY.md` | confirmed |
| H3 Detailed operation plan | `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md` | confirmed |
| H4 Codex execution start | `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md` | confirmed for local checks only |

## Passed Local Gates

- `make preflight`
- `make ist-all`
- `make ist-strong-l2`
- `make ist-package`
- `make external-release-check`

Latest recorded local receipt:

- `reports/IST_VERIFICATION_RECEIPTS.json`

## Failed And Corrected Gates

- External-case wording/provenance was revised to avoid over-reading package
  replay as independent external tool execution.
- Scalability wording was narrowed to measured manifest-processing runtime and
  estimated memory.
- Baseline comparison was rebuilt from generated per-method outputs.
- Ablation was expanded to observation-level rows with effect sizes and
  bootstrap intervals.
- RQ10 was downgraded from completed expert evidence to generated dry-run
  preparation and G13 remains `AUTHOR_REQUIRED`.
- G15 external release evidence was created as tag/release `v0.1.3` with Zenodo
  DOI `10.5281/zenodo.20798200`; the v0.1.2 SoftwareX baseline was not mutated.
- IST package/data availability mismatch was fixed by adding manuscript-listed
  artifacts to the package.
- Release preflight was tightened so positive claim surfaces are not blanket
  exempt from claim-boundary scanning.
- Workflow-governor per-stage audit gaps were corrected with durable S0-S11
  control, gate-review, reflection, and final-acceptance artifacts.
- S3 follow-up traceability gaps were corrected with exact non-private index
  identifiers, forbidden-skill schema, high-risk rejected-candidate records, and
  an H1 confirmation pointer.

## Forbidden Actions

- Do not fabricate author metadata, author/expert walkthrough data, funding,
  competing-interest, support-contact, CRediT, consent, or future DOI fields.
- Do not mutate the existing `v0.1.2` GitHub release or SoftwareX DOI.
- Do not promote generated dry-run artifacts into real human/expert evidence.
- Do not add device-side or vendor-tool completion claims beyond the current
  software-only evidence ceiling.

## Next Action

Wait for real author/expert input for G13, or continue only with
non-claim-expanding documentation, packaging, and review-hardening work.
