# ArtifactGate-EDA Gate Review

Date: 2026-06-22

## Verification Commands

```text
make install
.venv/bin/artifactgate --version
make reproduce-all
make package-release
make supplementary-package
make dist-package
make release-preflight
make preflight
make lint
find . -name '<macOS-resource-fork-sidecar-pattern>' | wc -l
grep -R "<local-user-home>" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=__pycache__ || true
grep -R "<windows-user-home>" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=__pycache__ || true
```

## Gate Table

| Gate | Check | Score | Threshold | Pass/Fail | Evidence | Critical Flaws | Revision Actions |
|---|---|---:|---:|---|---|---|---|
| G1 | clean repo | 100 | 100 | Pass | Local scan returned 0 macOS resource-fork sidecars; local path grep returned no private user-home or Windows user-home hits. | None local. | Keep generated metadata out of `repo/src`. |
| G2 | install | 100 | 100 | Pass | `make install`; `.venv/bin/artifactgate --version` returned `0.1.3`. | None local. | None. |
| G3 | CLI | 95 | 90 | Pass | CLI exposes `ingest`, `validate`, `replay`, `claim-check`, `report`, `package`, `compare`, plus local summary helpers. | Core commands are intentionally minimal. | Expand API ergonomics only after release blocker work. |
| G4 | tests/lint | 100 | 100 | Pass | Baseline `make preflight` ran `ruff`, `compileall`, and `pytest`; current IST verification receipts record `make test`: 26 passed. | None local. | Keep `reports/IST_VERIFICATION_RECEIPTS.json` aligned after test-count changes. |
| G5 | CI | 100 | 100 | Pass external | `scripts/external_release_check.py` verifies the latest `main` CI run before final acceptance. | None local. | None. |
| G6 | examples | 100 | 100 | Pass | `make ingest-all`: ngspice, icarus, yosys, verilator, plecs, logisim all passed. | None local. | None. |
| G7 | claim-check | 100 | 100 | Pass | `make negative-claims`: 52 dangerous claims checked; all 52 classified as unsupported with safe rewrite suggestions. | None local. | None. |
| G8 | corrupted tests | 100 | 100 | Pass | `make corrupted-tests`: 7 injected cases hit expected failure classes. | None local. | None. |
| G9 | scalability | 100 | 90 | Pass | `make scalability`: 1k, 3k, 5k, 10k synthetic rows generated; `reports/e5_scalability_summary.md` reports 10k pass. | Synthetic timing only, not a full memory profiler. | Keep wording as runtime-overhead smoke evidence, not performance proof. |
| G10 | docs | 98 | 85 | Pass local | README, CLI, API, schema, adapter, reproducibility, SoftwareX submission checklist, and release-readiness docs exist. | Author-side submission metadata remains. | Fill author metadata before journal submission. |
| G11 | license | 100 | 100 | Pass | `LICENSE` is Apache-2.0; metadata files reference Apache-2.0. | None local. | None. |
| G12 | citation | 100 | 100 | Pass external | DOI 10.5281/zenodo.20798200 is recorded locally and resolves to https://zenodo.org/records/20798200; external release checker passed. The earlier v0.1.2 DOI remains historical baseline evidence only. | None. | None. |
| G13 | manuscript | 96 | 85 | Codex-verifiable pass | `paper/softwarex_manuscript.md`, `.tex`, `highlights.md`, `declarations.md`, four generated figures, and `MANUSCRIPT_REPRO_PACKAGE.md` exist; manuscript text is expanded beyond skeleton while staying within the software-only boundary and includes DOI 10.5281/zenodo.20798200. | Support email, funding, conflicts, and CRediT fields are author-provided values. | Fill author-side metadata before final journal submission. |
| E8 | Codex/MCP execution audit | 100 | 90 | Pass | `reports/e8_codex_mcp_execution_audit.md` documents Codex/MCP as engineering automation only and confirms Makefile/CLI reproducibility does not depend on it. | None local. | None. |
| G14 | boundary | 100 | 90 | Pass local | `make release-preflight` checks private paths, resource forks, forbidden wording contexts, capsule zip contents, and supplementary zip contents. | None local. | Keep gate review before final release. |
| D22 | supplementary artifact package | 100 | 100 | Pass local | `make supplementary-package` creates `release/artifactgate_eda_supplementary_artifacts.zip`; `make release-preflight` verifies required files inside it. | Release zip is generated and ignored by Git. | Regenerate after manuscript/report changes. |
| D2 | Python distribution package | 100 | 100 | Pass local | `make dist-package` creates sdist and wheel under `dist/`; `make release-preflight` verifies both files exist. | Dist artifacts are generated and ignored by Git. | Regenerate after source/package metadata changes. |

## Mentor Review

| Agent | Score | Pass/Fail | Critical Flaws | Minor Issues | Revision Actions | Change Skill/Resource? | Reduce Claim/Scope? | Next Iteration Target |
|---|---:|---|---|---|---|---|---|---|
| Engineering Mentor | 98 | Pass external | None. | Package implementation is minimal but coherent. | Keep CI green after author-side metadata changes. | No. | No. | Author metadata. |
| Codex Validator | 98 | Pass local | None for Codex-verifiable gates. | Final journal submission still needs author-side metadata. | Keep author-side placeholders explicit. | No. | No. | Submission packet. |
| Reviewer | 93 | Pass draft | Manuscript still requires author declarations. | Figures are generated and source-backed but not externally reviewed. | Fill author-side metadata before journal submission. | No. | No. | Author metadata. |

## SoftwareX Template Audit

The SoftwareX OSP template checked on 2026-06-22 was Version 6, March 2026.
It requires a GitHub repository in the metadata table, a documented README, a
`Licence.txt` file, a 4000-word body limit, no more than six figures, and the
five main templated sections: Motivation and significance, Software
description, Illustrative examples, Impact, and Conclusions. The local package
now contains `Licence.txt`, `docs/softwarex_submission_checklist.md`, four
generated figures, and manuscript skeletons using those sections.

## Release Package Audit

`make preflight` passes locally. It regenerates local reports, figures,
manuscript package maps, three replay capsules, the supplementary artifact
package, Python sdist/wheel artifacts, and then runs
`scripts/release_preflight.py`. The generated release files are intentionally
ignored by Git and should be rebuilt after checkout.

## Final Acceptance Status

Local engineering, manuscript-package, supplementary-package, public GitHub
repository, v0.1.3 GitHub release, v0.1.3 Zenodo DOI, DOI metadata, E8
automation audit, and external release checker gates pass. Codex-verifiable
final acceptance is PASS. Final journal submission still requires author-side
support email, funding, competing interests, and CRediT confirmation.
