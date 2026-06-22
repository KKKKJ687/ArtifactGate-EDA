# Workflow Governor Stage Control Packet

Generated: 2026-06-22

Project: ArtifactGate-EDA IST stronger-plan branch

This packet supplies the durable S0-S3 workflow-governor evidence that was
missing from the first per-stage agent audit. It records intake, route
selection, calibration, skill/resource mapping, forbidden choices, and H1
confirmation state without changing the scientific claim boundary.

## S0 Raw Idea Intake

| Field | Record |
| --- | --- |
| Task type | Research-code, empirical-evaluation, manuscript-package, release-readiness workflow. |
| Complexity | High: project execution, paper claims, local packages, release checks, and subagent reviews. |
| Initial objective | Complete the IST stronger-plan Codex-verifiable work using workflow-governor gates and subagent review. |
| Known open final-acceptance blockers | G13 real author/expert walkthrough evidence. |
| Gate result | PASS after durable recording; missing information is known and isolated from Codex-completable work. |

## S1 Brainstorming Route Selection

| Candidate route | Fit | Risk | Decision | Rationale |
| --- | ---: | ---: | --- | --- |
| Software engineering method + tool + empirical evaluation | 10 | 3 | Selected | Matches IST scope and existing ArtifactGate-EDA evidence while staying software-only. |
| SoftwareX-style software/package article | 6 | 2 | Rejected for IST layer | Already covered by the baseline release; insufficient empirical depth for the stronger-plan objective. |
| Hardware/FPGA/DFX validation article | 2 | 10 | Forbidden | Would exceed available evidence and violate the frozen boundary. |

Calibration questions carried into S2:

- Which IST gates are locally verifiable by Codex?
- Which gates require author/external action?
- How can generated dry-run evidence be kept separate from real human/expert
  evidence?
- How can package cleanliness be proven from archive payloads, not only file
  names?

## S2 Workflow Calibration

Corrected stage sequence:

```text
S0 intake
S1 route selection
S2 calibration
S3 skill/resource mapping
S4 frozen claim/objective/boundary
S5 gate design
S6 current operation plan
S7 Codex execution packet
S8 Codex execution
S9 gate review and mentor review
S10 failure reflection and iteration
S11 final acceptance audit
```

Workflow corrections:

- Treat the IST plan as the target plan, but treat the current worktree as the
  authoritative artifact state when names or counts have drifted.
- Keep G13 as an open gate instead of trying to satisfy it with generated
  artifacts; record G15 only from real external release/DOI evidence.
- Require subagent review for failure discovery and follow-up acceptance.
- Require package-payload scanning for release cleanliness.
- Require a formal S11 audit even when final acceptance is not reached.

H1 preparation record:

| Field | Record |
| --- | --- |
| Content to confirm | Use candidate local skills/resources and subagents to execute the IST stronger-plan inside the frozen software-only boundary after H1 confirmation. |
| Risk | Wrong skill/resource routing could expand scope, overclaim evidence, or mutate external release state. |
| Next step | Proceed to S3 skill/resource mapping; freeze selected skills/resources only at H1/S3 before S4/S5. |
| Allowed actions after confirmation | Read local manuals, inspect project files, edit local workflow/report/code artifacts, run local verification, spawn read-only subagents. |

## S3 Skill Mapping

Index evidence:

- Mega-Tron routing was called in the active session.
- Index root used for S3 mapping: `CODEX_RESOURCE_ROOT`; backup roots under
  `CODEX_RESOURCE_ROOT/backups/` were not used.
- The exact local skills index was
  `CODEX_RESOURCE_ROOT/codex_operating_manual/SKILLS_INDEX.md`.
- The exact local resource index was `CODEX_RESOURCE_ROOT/RESOURCE_INDEX.md`.
- The exact resource-library detail index was
  `CODEX_RESOURCE_ROOT/codex_operating_manual/RESOURCE_LIBRARY_INDEX.md`.
- The exact local agent index was
  `CODEX_RESOURCE_ROOT/codex_operating_manual/AGENTS_INDEX.md`.
- The workflow-governor skill, stage contracts, skill routing rules, resource
  routing rules, gate standard, mentor agents, and failure handling manuals were
  read.
- Absolute filesystem roots are intentionally omitted from this reproducible
  control artifact.

| Stage family | Candidate skill | Fit | Risk | Confidence | Selected? | Why | Forbidden / risk note |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| Routing/control | `codex-capability-router` | 9 | 2 | 9 | Yes | Selects local skills, agents, and manuals before complex project work. | None for routing use. |
| Workflow control | `workflow_governor` | 10 | 2 | 10 | Yes | Supplies stage contracts, hard stops, gate scoring, and failure handling. | Must not be reduced to a naming-only citation. |
| Claim discipline | `research-claim-os` | 9 | 3 | 8 | Yes | Separates direct evidence, assumptions, unsupported claims, and human gates. | Must not promote generated dry-run rows into human evidence. |
| Evidence audit | `paper-evidence-auditor` | 9 | 2 | 9 | Yes | Checks paper/report claims against local evidence and receipts. | Must not invent citations or source snippets. |
| Submission boundary | `journal-submission-auditor` | 8 | 3 | 8 | Yes | Keeps author metadata, CRediT, declarations, and external DOI actions separated. | Must not fill author-side declarations without author input. |
| Plot-only review | `publication-plot-auditor` | 5 | 2 | 7 | No | Figures are not the current blocker. | Use only if figure claims change. |
| Hardware review | `fpga-dfx-reviewer` | 4 | 8 | 8 | No | Useful only to police boundaries, not to add hardware claims. | Forbidden as a route to hardware/Vivado/DFX validation. |
| Implementation-only worker | `implementation_worker` | 6 | 7 | 7 | No | Could patch files, but the current failure is governance evidence. | Use only after scope and write set are explicit. |
| Broad autoresearch loop | `approval-gated-autoresearch-loop` | 6 | 6 | 8 | No | Useful for bounded experiment loops, but the current work is locked gate closure and evidence synchronization. | Do not reopen the experimental plan or create new unapproved loops. |

Coverage gap:

- No skill can complete G13 without real author/expert action.
- No skill should create hardware, Vivado, DFX, bitstream, or board-validation
  evidence.

Forbidden skills:

| Name | Forbidden Reason | Misuse Scenario | Alternative |
| --- | --- | --- | --- |
| `fpga-dfx-reviewer` | Forbidden as a route to add hardware/Vivado/DFX evidence. | Turning a claim-boundary audit into hardware validation, timing closure, bitstream, or board-readiness claims. | `research-claim-os` and claim-boundary scans. |
| `implementation_worker` | Forbidden before the scope, write set, and gate review are explicit. | Broad edits that satisfy tests while bypassing workflow-governor hard stops. | Read-only reviewers first, then scoped patches inside the execution packet. |
| `publication-plot-auditor` | Forbidden as a substitute for workflow-governor gate closure. | Treating figure polish or caption review as proof that evidence, package, or author/external gates are closed. | `paper-evidence-auditor` plus machine receipts. |
| `skill-installer` | Forbidden for this locked project state. | Installing or changing tools to satisfy a paper-package gate. | Existing installed skills and local manuals. |
| `plugin-creator` | Forbidden for this locked project state. | Creating runtime/plugin surface area while release materials are being audited. | Existing repo scripts and read-only subagents. |
| `autonomous-research-workbench` | Not adopted because it would reopen broad experiment-loop design after the IST plan is already locked. | Expanding RQ scope, budgets, or dependencies instead of closing known gates. | `workflow_governor`, `research-claim-os`, current reports, and `approval-gated-autoresearch-loop` only as a rejected candidate. |

High-risk Mega-Tron not-adopted record:

| Candidate | Original appeal | Risk or mismatch | Selected alternative | User confirmation state |
| --- | --- | --- | --- | --- |
| `approval-gated-autoresearch-loop` | Supports bounded modify-run-evaluate-keep/revert loops with metrics and rollback. | Current failures are governance traceability and stale evidence counts, not a request to launch new experiments. | `workflow_governor` with local receipts and subagent re-audits. | H1 mapping keeps it rejected unless a later gate fail requires re-routing. |
| `autonomous-research-workbench` | Can orchestrate broad research/experiment workflows. | Too broad for a locked IST gate-audit pass and could reopen completed experiment scope. | Current IST plan, gate ledger, receipts, and author/external packet. | Not selected; would require explicit user approval to reintroduce. |

## S3 Resource Mapping

Resource index evidence:

- The local resource index was read from
  `CODEX_RESOURCE_ROOT/RESOURCE_INDEX.md`.
- The resource-library detail index was read from
  `CODEX_RESOURCE_ROOT/codex_operating_manual/RESOURCE_LIBRARY_INDEX.md`.
- Project source-of-truth files were selected over raw external repositories.
- Community resources remain discovery inputs only, not execution instructions.

| Stage family | Candidate resource | Fit | Trust | Risk | Context Cost | Selected? | Why | Forbidden / risk note |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| Plan source | `docs/ist_stronger_plan_source_record.md` | 10 | 8 | 3 | 5 | Yes | Defines target IST gates and stronger-plan scope. | Use current worktree when plan artifact names are stale. |
| Workflow contracts | `workflow_governor/stage_contracts.md` | 10 | 10 | 1 | 4 | Yes | Defines S0-S11 required outputs and hard stops. | None. |
| Gate scoring | `workflow_governor/gate_standard.md` | 10 | 10 | 1 | 2 | Yes | Defines score, threshold, flaws, and revision-action requirements. | None. |
| Mentor/failure control | `workflow_governor/mentor_agents.md` and `failure_handling.md` | 9 | 10 | 1 | 3 | Yes | Defines subagent/mentor review and reflection rules. | None. |
| Project state | `.codex_workflow/WORKFLOW_STATE.md` | 9 | 9 | 2 | 2 | Yes | Current stage, selected artifacts, and open gates. | Must be updated only after gate review. |
| Gate evidence | `reports/IST_GAP_AUDIT.md` and `reports/IST_VERIFICATION_RECEIPTS.json` | 10 | 9 | 2 | 5 | Yes | Maps gates to current evidence and commands. | Counts must stay synchronized. |
| Author/external protocol | `docs/ist_author_external_completion_packet.md` | 9 | 9 | 2 | 3 | Yes | Defines G13/G15 closure conditions. | G15 closure must stay tied to real external DOI evidence; G13 must not be treated as completed evidence. |
| Raw external repos | Downloaded community workflow repositories | 3 | 5 | 8 | 8 | No | Not needed for this locked project state. | Could introduce untrusted instructions or scope drift. |
| Commercial/vendor tools | PLECS, LTspice, Vivado as core dependencies | 2 | 4 | 9 | 6 | No | Not required for reproducibility claims. | Forbidden as core reproducibility dependencies. |

Forbidden resources:

| Resource | Forbidden reason | Bad match scenario | Alternative |
| --- | --- | --- | --- |
| Unreviewed community install scripts | Could mutate local/global environment. | Running setup hooks while preparing a paper package. | Use local manuals and current repo scripts. |
| External release/tag mutation tools | Would change archive state without explicit user approval. | Moving `v0.1.2` or editing Zenodo to satisfy G15. | Use only explicitly approved new-version releases such as the completed `v0.1.3` path. |
| Hardware/Vivado/board logs not present in repo | Would fabricate or imply unavailable evidence. | Treating stubs or negative fixtures as validation. | Keep unsupported-claim ledgers and boundary wording. |

H1 confirmation record:

| Field | Record |
| --- | --- |
| Content confirmed | Selected skills/resources above are the active workflow-governor mapping for this branch. |
| Confirmation pointer | `.codex_workflow/SESSION_STATE.md` records user confirmation to execute the selected workflow-governor operation plan; `.codex_workflow/WORKFLOW_STATE.md` records H1 as confirmed for local Codex execution. |
| Risk | Over-broad routing can create scope drift; under-routing can miss gate failures. |
| Next step | Freeze claim/objective/boundary in S4. |
| Allowed actions after confirmation | Use selected resources to edit local control artifacts, run local checks, and request read-only subagent reviews. |
