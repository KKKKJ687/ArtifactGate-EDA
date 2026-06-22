# IST Frozen Claim, Objective, and Boundary

Generated: 2026-06-22

This is the durable S4 workflow-governor artifact for the IST stronger-plan
branch. It freezes what Codex may claim, what remains unsupported, and which
assumptions govern the current worktree.

## Frozen Claim

ArtifactGate-EDA is a software engineering method and tool for claim-safe,
replay-checkable, and reviewer-auditable artifact preparation in software-only
EDA experiments.

The current IST layer supports claims about:

- adapter-based artifact ingestion for software-only EDA packages;
- evidence-level modelling and claim-to-artifact traceability;
- deterministic replay/package checks for included software artifacts;
- unsupported-claim detection for hardware, Vivado, DFX, bitstream, board, and
  deployment overclaims;
- generated negative-claim, corrupted-artifact, evidence-level, external-case,
  scalability, baseline-emulator, ablation, backend-audit, and reviewer-dry-run
  reports.

## Frozen Objective

Complete the Codex-verifiable IST stronger-plan engineering package within the
local S4-S11 evidence scope while keeping the evidence ceiling below
human/expert study completion and below new external release/DOI publication.
The full IST stronger-plan objective remains incomplete until real G13
author/expert evidence and real G15 external release/DOI evidence exist.

## Boundary

Allowed evidence:

- local source files, policies, schemas, examples, reports, generated figures,
  release zips, and Python package artifacts;
- software simulation, open-source synthesis, metadata fallback, deterministic
  benchmark harnesses, and package-level replay/validation outputs;
- subagent review records and machine receipts for local verification.

Disallowed evidence escalation:

- no device-side validation;
- no vendor implementation signoff;
- no completed reconfiguration deployment;
- no board evidence;
- no human/expert walkthrough evidence unless supplied by a real evaluator;
- no new IST DOI or external archive unless explicitly authorized and created.

## Unsupported Claims

The current worktree must not claim that ArtifactGate-EDA:

- provides hardware validation or board validation;
- completes Vivado timing, Vivado implementation, DFX deployment, or bitstream
  generation;
- proves FPGA speedup or hardware energy savings; industrial deployment and a
  universal EDA workflow remain unsupported;
- converts generated reviewer dry-run rows into real human/expert evidence;
- uses ReconfigRT-I or LA-DFX as core IST results;
- has a new IST public DOI or external archive beyond the existing SoftwareX
  baseline DOI.

## Assumptions

- The current branch is a dirty IST upgrade worktree, not a clean committed
  release snapshot.
- The SoftwareX baseline archive and DOI remain externally verified and are not
  mutated by this IST layer.
- Local experiments are deterministic software-evaluation artifacts unless a
  report explicitly states otherwise.
- Generated walkthrough outputs are author-side preparation only.
- Package cleanliness requires archive-payload scanning, not only file-name
  scanning.

## H2 Hard Stop Record

| Field | Record |
| --- | --- |
| Content to confirm | Freeze the software-only claim boundary above and keep G13/G15 open. |
| Confirmation pointer | `.codex_workflow/WORKFLOW_STATE.md` records H2 as confirmed for local Codex execution; `.codex_workflow/SESSION_STATE.md` records user authorization to execute the selected workflow-governor plan. |
| Risk | Expanding the boundary would create unsupported hardware, human-study, or DOI claims. |
| Next step after confirmation | Design and execute measurable local gates while preserving the boundary. |
| Allowed actions after confirmation | Edit local code, reports, packages, and workflow artifacts inside the approved branch; run local checks; use subagent review. |
| Still forbidden | Author metadata fabrication, real expert-walkthrough fabrication, tag/release mutation, DOI mutation, hardware/Vivado/DFX/board positive claims. |

## Evidence Pointers

- Plan source: `docs/ist_stronger_plan_source_record.md`
- Current state: `.codex_workflow/WORKFLOW_STATE.md`
- Gate ledger: `reports/IST_WORKFLOW_GOVERNOR_GATE_LEDGER.md`
- Receipts: `reports/IST_VERIFICATION_RECEIPTS.json`
- Author/external packet: `docs/ist_author_external_completion_packet.md`
