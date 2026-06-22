# Session State

Project: ArtifactGate-EDA

Current stage: S11 Final Acceptance audit / Awaiting G13 author/expert evidence

Confirmed by user: Start executing the selected workflow-governor operation
plan and continue toward the full plan.md project.

Current work packet:

- Local SoftwareX-safe repository, Python package, examples, tests, reports,
  figures, supplementary capsule, and sdist/wheel artifacts are generated and
  verified by `make preflight`.
- IST stronger-plan local experiments, workflow-governor control packets,
  manuscript package, and IST evaluation zip are generated and verified by
  `make ist-strong-l2`, `make ist-package`, and `make preflight`.
- The original discussion package remains read-only.
- External publication state is verified: public GitHub repository, live
  GitHub Actions run, GitHub release, and Zenodo DOI.
- External release checking now infers the Zenodo DOI from local metadata when
  `--doi` is not supplied, so `make external-release-check` is a self-contained
  acceptance target.
- Remaining SoftwareX journal-submission values require author-side metadata,
  tracked outside Codex-verifiable engineering gates.
- IST G13 remains open because it requires real author/expert walkthrough
  evidence. G15 has a new IST tag/release and Zenodo DOI.

Latest verified command:

- `make ist-strong-l2` passed on 2026-06-22 with 12063 admissible files,
  21985 evidence-graph nodes, 171674 edges, 8218 boundary hits, 0 leaks, and
  0 IST manuscript claim violations.
- `make ist-package` passed on 2026-06-22 with 184 zip entries, required
  workflow-governor control artifacts, no resource-fork entries, and no private
  path payload hits.
- `make preflight` passed on 2026-06-22 with lint, 37 pytest tests, replay
  capsules, supplementary package, Python sdist/wheel, and release preflight.
- `make external-release-check` passed on 2026-06-22 using local DOI metadata
  inference for DOI 10.5281/zenodo.20789516.
- GitHub release `v0.1.3` is published and Zenodo DOI
  `10.5281/zenodo.20798200` resolves for the IST evaluation snapshot.
- Strict per-stage workflow-governor subagent re-audit
  `019eef52-0b45-7583-9595-6af88193cde3` returned
  `PASS_WITH_LIMITATION` on 2026-06-22; S0-S10 governance coverage is passing
  with recorded limitations, while S11 remains failed because G13 requires real
  author/expert evidence.
- Dedicated S0-S11 per-stage read-only subagent audits were then recorded in
  `reports/IST_WORKFLOW_GOVERNOR_STAGE_AGENT_AUDIT.md`; S11 remains failed,
  and S8 is explicitly `PASS_WITH_LIMITATION` because raw command output is
  preserved as summarized receipts rather than complete raw logs.
- A continuation verification record was appended to
  `reports/IST_VERIFICATION_RECEIPTS.json` after rerunning
  `make ist-strong-l2`, `make preflight`, `make ist-package`, and
  `make external-release-check`; after later G15 closure, this keeps S11 failed
  until real G13 evidence exists.
- `scripts/external_release_check.py --repo KKKKJ687/ArtifactGate-EDA --tag
  v0.1.2 --doi 10.5281/zenodo.20789516` passed on 2026-06-22.
- Browser verification on 2026-06-22 confirmed the public GitHub v0.1.2 release
  page and Zenodo record page.

Forbidden actions:

- No hardware, Vivado, DFX, bitstream, or board-level positive claims.
- No destructive cleanup of the source discussion package.
- No fabricated support email, funding statement, competing interest statement,
  or CRediT role assignment.
- No fabricated G13 author/expert walkthrough evidence or future DOI.
