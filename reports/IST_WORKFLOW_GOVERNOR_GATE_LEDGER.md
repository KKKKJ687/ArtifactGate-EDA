# IST Workflow Governor Gate Ledger

Generated: 2026-06-22

Plan source: `docs/ist_stronger_plan_source_record.md`

This ledger records the workflow-governor gate state for the IST stronger-plan
branch. It is a control artifact, not a new experiment result. It must be read
with `reports/IST_GAP_AUDIT.md`, `reports/IST_VERIFICATION_RECEIPTS.json`, and
`docs/ist_author_external_completion_packet.md`.

## Boundary

The local IST layer remains software-only. It supports claims about artifact
engineering, evidence-level modelling, claim-boundary checking, generated
negative/corruption benchmarks, deterministic baseline harnesses, and local
package reproducibility. It does not close author/expert or external archive
gates by inference.

## Workflow-Governor Stages

| Stage | Required output | Current evidence | Status |
| --- | --- | --- | --- |
| S0 Raw idea intake | IST stronger-plan objective captured | `.codex_workflow/STAGE_CONTROL_PACKET.md` | PASS |
| S1 Brainstorming | IST identity and boundaries identified | route-selection table in `.codex_workflow/STAGE_CONTROL_PACKET.md` | PASS |
| S2 Workflow calibration | Local truth, routing, boundary, gate standard | corrected stage sequence in `.codex_workflow/STAGE_CONTROL_PACKET.md` | PASS |
| S3 Skill-resource mapping | Relevant skills/resources selected | scored skill/resource mapping in `.codex_workflow/STAGE_CONTROL_PACKET.md` | PASS |
| S4 Claim/objective/boundary | Software-only claim boundary frozen | `reports/IST_FROZEN_CLAIM_BOUNDARY.md` | PASS |
| S5 Gate design | Strong-plan gates made measurable | `reports/IST_GAP_AUDIT.md` and this ledger | PASS |
| S6 Detailed operation plan | Executable tasks and checks | `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md` | PASS |
| S7 Execution preparation | Non-destructive branch and forbidden actions | `reports/IST_CURRENT_OPERATION_AND_EXECUTION_PACKET.md` | PASS |
| S8 Codex execution | Local scripts, reports, package, manuscript layer | summarized `make ist-all`, package, L2, and preflight receipts | PASS_WITH_LIMITATION |
| S9 Gate review | Machine checks plus subagent review | `reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md` | PASS |
| S10 Iteration/reflection | Failed gates diagnosed and corrected | `reports/IST_WORKFLOW_REFLECTION_LOG.md` | PASS |
| S11 Final acceptance | Final acceptance audit | `reports/IST_FINAL_ACCEPTANCE_AUDIT.md`; G13 evidence added and validator PASS; final acceptance remains bounded by single-evaluator limitation | PASS_WITH_LIMITATION |

## Strong-Plan Gate Ledger

| Gate | Requirement | Current evidence | Subagent / review status | Verdict |
| --- | --- | --- | --- | --- |
| G0 | Clean package | package zip self-test, no resource forks, no private path payload hits | package reviewer PASS | PASS |
| G1 | File inventory | `reports/file_inventory_full.csv`, 12071 admissible files | L2 gate PASS | PASS |
| G2 | Evidence graph | 21997 nodes and 171797 edges | L2 gate PASS | PASS |
| G3 | Literature matrix | `literature/literature_matrix.csv`, 57 mapped sources | local mapping support artifact; not PRISMA-complete | PASS_WITH_LIMITATION |
| G4 | Multi-adapter coverage | RQ1 reports and generated coverage examples | local gate PASS | PASS |
| G5 | Replay | RQ2 reports, 10 repeats per core case, Docker/CI status recorded separately | local gate PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| G6 | ClaimBench | 1300 ClaimBench-EDA rows, critical false negatives 0 | local gate PASS | PASS |
| G7 | Corruption benchmark | 30 defect classes, 900 defect instances, 30 clean cases | local gate PASS | PASS |
| G8 | Evidence classification | 1000 gold rows, macro-F1 threshold satisfied | local gate PASS | PASS |
| G9 | External cases | 10 public cases, 8 open-source replay-package/validation cases | subagent-reviewed wording fix | PASS |
| G10 | Scalability | 100k synthetic manifest rows, 53 runtime observations | subagent-reviewed limitation | PASS_WITH_LIMITATION |
| G11 | Baseline execution | 7 generated-output baseline/target methods, 56 task observations | subagent-reviewed rebuild | PASS_WITH_LIMITATION |
| G12 | Ablation | 10 deterministic variants, 32860 observations, 40 effect-size rows; no human timing or external EDA execution is claimed | subagent-reviewed expansion | PASS_WITH_LIMITATION |
| G13 | Human/expert reviewer gate | real author walkthrough report, observations CSV, and command log CSV added; `make g13-check` PASS | single-evaluator limitation retained | PASS_WITH_LIMITATION |
| G14 | Manuscript claim gate | `reports/ist_manuscript_claim_gate.md`, 0 violations | L2 gate PASS | PASS |
| G15 | New IST release archive and DOI | tag/release `v0.1.3` exists; Zenodo DOI `10.5281/zenodo.20798200` resolves; v0.1.2 baseline was not mutated | explicit external-release check PASS | PASS |

## Subagent Review Record

| Reviewer session | Scope | Result | Durable local consequence |
| --- | --- | --- | --- |
| `019eeec2-3c04-7ab3-805a-ffeb6c84fb8a` | RQ10/G13 human-gate claim strength | FAIL | RQ10 downgraded to dry-run preparation |
| `019eeec9-0388-7600-ae5b-675a68a85056` | RQ10 downgrade re-review | PASS_WITH_LIMITATION | G13 kept `AUTHOR_REQUIRED` |
| `019eeed1-f227-7ca3-82d6-d2f24083b2bb` | Completion package audit | FAIL | Missing manuscript-listed artifacts added to IST zip |
| `019eeeda-23ce-7ce3-9f33-93ebb7183c45` | IST package consistency | PASS | 27 Section 10 artifacts verified in zip |
| `019eeedf-b1be-78f3-8483-6d2ab7c33807` | Release-preflight claim-boundary rule | FAIL | Positive claim surfaces changed from blanket allowlist to line-scoped boundary contexts |
| `019eeeea-2346-7580-bedf-6c7bccc6bdc6` | Follow-up release-preflight and package review | PASS | New unit tests and tightened gate accepted |
| `019eef00-9062-7082-a405-3c859abc7cd1` | Workflow-governor ledger/package/receipt consistency | FAIL | Found IST zip private-path payloads, stale receipt coverage, and undefined combined status |
| `019eef08-dc60-7350-b6ce-8b6be777f0d1` | Follow-up workflow-governor consistency review | PASS | Confirmed redacted IST zip payloads, release-preflight zip scanning, receipt updates, and status vocabulary fix |
| `019eef0f-ceda-7d30-880c-0149121054a8` | S0-S3 workflow-governor stage audit | FAIL | Required durable S1-S3 route, calibration, skill/resource mapping, forbidden lists, and H1 evidence added |
| `019eef10-1b3b-7f93-b7e3-7f13b96ef906` | S4-S8 workflow-governor stage audit | FAIL | S4 boundary, S6 operation plan, S7 execution packet, and test-count consistency corrected |
| `019eef10-6b2d-7662-a8d6-1811ceb6ccee` | S9-S11 workflow-governor stage audit | FAIL | S9 numeric gate review, S10 missing reflections, and S11 final acceptance audit added; S11 was open at that historical pre-G13 audit |
| `019eef19-b133-7490-8335-c20d690b668c` | S0-S3 follow-up stage audit | FAIL | S3 traceability gaps were found: exact index identifiers, forbidden-skills schema, high-risk rejected candidates, and mapping-summary drift |
| `019eef19-fa5d-7371-b158-6af0e4b63c01` | S4-S8 follow-up stage audit | HISTORICAL_PASS | S4-S8 materially passed in that follow-up; the later dedicated S8 audit narrowed final S8 to `PASS_WITH_LIMITATION` because raw command output is preserved as summarized receipts |
| `019eef1a-461b-78b0-a860-8adc74780f49` | S9-S11 follow-up stage audit | PASS_WITH_LIMITATION | S9/S10 passed; S11 remained failed because G13/G15 were open; stale S11 counts were corrected |
| `019eef23-7d94-7411-ba16-d9b37476dcd4` | S9-S11/package and receipt re-audit | PASS_WITH_LIMITATION | Confirmed then-current zip entry count, then-current L2 counts, then-current pytest count, no private payloads, and S11 still open in that pre-G13 state |
| `019eef23-2d26-7a51-b8a0-791f3147fa2e` | S0-S3 final re-audit | PASS | S3 scored 89/80 after exact non-private index identifiers and H1 confirmation pointer were added |
| `019eef2c-3af6-7922-bf43-69b22d29d747` | G13/G15 author-external packet audit | FAIL_THEN_PASS | Initial Q3/Q5 gaps were closed by adding required schema/signoff, exact review-material checklist, closure rerun sequence, refresh targets, and subagent re-review requirement |
| `019eef52-0b45-7583-9595-6af88193cde3` | Strict per-stage workflow-governor coverage re-audit | PASS_WITH_LIMITATION | Confirmed S0-S11 scored rows exist; found and corrected status vocabulary drift, an over-specific control-packet flag, and a stale G10/G14 label |
| `019eef5b`-`019eef63` dedicated stage agents | Individual S0-S11 workflow-governor audits | PASS_WITH_LIMITATION aggregate | Each S0-S11 stage received a dedicated read-only subagent verdict; local governance wording/threshold/status limitations were corrected; at that historical pre-G13 audit S8 remained `PASS_WITH_LIMITATION` and S11 remained failed pending G13 |
| `019eef96-2694-7521-a63c-6b538d938777` | G13/G15 submission-boundary audit after G15 DOI refresh | PASS_WITH_G13_OPEN | Confirmed G15 was recorded as real `v0.1.3` / `10.5281/zenodo.20798200`; at that pre-G13 audit, G13 remained `AUTHOR_REQUIRED`, author-side metadata was not fabricated, and no hardware/vendor-tool positive claim was introduced |
| `019eef96-6adc-7c61-8c59-a984be989259` | G15 package and metadata consistency audit | FAIL_THEN_PASS | Found package wording and stale v0.1.2 supplementary-report risks; fixed current DOI/version wording, removed content-level macOS metadata token hits from shipped zips, rebuilt packages, and reran release/external checks |
| `019eefe0-b6b9-7270-ae37-691f91301ce2` | G13 final pre-commit audit | FAIL_THEN_FIXED | Found a stale present-tense Open Gates row for G13 after G13 had passed with limitation; the current ledger now records no open Codex-verifiable IST gates and preserves the single-evaluator limitation |

## Latest Local Verification Snapshot

From the latest G13 closure verification and rerun receipts:

- `make test`: 58 collected, 58 passed.
- `make ist-all`: PASS.
- `make ist-package`: 194 zip entries; 27 manuscript-listed data/report artifacts present; workflow-governor control artifacts and G13 evidence files present; private path payload self-test passed.
- `make ist-strong-l2`: 12071 admissible files; 21997 evidence graph nodes; 171797 edges; 8244 boundary hits; 0 leaks; 0 IST manuscript violations.
- `make preflight`: PASS.
- `make external-release-check`: PASS for the published release/DOI metadata;
  explicit `external_release_check.py --tag v0.1.3 --doi
  10.5281/zenodo.20798200` also passed.

Additional local checks performed after package rebuild:

- IST zip self-test: PASS.
- Manifest-listed Section 10 artifacts in zip: 27 / 27.
- Resource-fork entries in zip: 0.
- Private path payload hits in zip: 0.
- Content-level scans for macOS archive metadata tokens, resource-fork sidecar
  tokens, local user-home paths, and Windows user-home paths in the IST and
  supplementary zips: 0 hits.

## Open Gates

| Gate | Current status | Limitation retained |
| --- | --- | --- |
| None for Codex-verifiable IST closure | S11 is `PASS_WITH_LIMITATION` after real G13 author walkthrough evidence, validator PASS, and external G15 verification | G13 is a single-author walkthrough only; no multi-participant human study, measured human timing, hardware/vendor-flow, bitstream, reconfiguration, or board-level evidence is claimed |
