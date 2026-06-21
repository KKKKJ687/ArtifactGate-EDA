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
find . -name '._*' | wc -l
grep -R "<local-user-home>" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=__pycache__ || true
grep -R "<windows-user-home>" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=__pycache__ || true
```

## Gate Table

| Gate | Check | Score | Threshold | Pass/Fail | Evidence | Critical Flaws | Revision Actions |
|---|---|---:|---:|---|---|---|---|
| G1 | clean repo | 100 | 100 | Pass | `find . -name '._*'` returned 0; local path grep returned no private user-home or Windows user-home hits. | None local. | Keep generated metadata out of `repo/src`. |
| G2 | install | 100 | 100 | Pass | `make install`; `.venv/bin/artifactgate --version` returned `0.1.2`. | None local. | None. |
| G3 | CLI | 95 | 90 | Pass | CLI exposes `ingest`, `validate`, `replay`, `claim-check`, `report`, `package`, `compare`, plus local summary helpers. | Core commands are intentionally minimal. | Expand API ergonomics only after release blocker work. |
| G4 | tests/lint | 100 | 100 | Pass | `make preflight` ran `ruff`, `compileall`, and `pytest`: 19 passed. | None local. | None. |
| G5 | CI | 100 | 100 | Pending v0.1.2 external check | Public GitHub Actions on `main` must be verified after the v0.1.2 release commit. | None local. | Run the external checker after publishing v0.1.2. |
| G6 | examples | 100 | 100 | Pass | `make ingest-all`: ngspice, icarus, yosys, verilator, plecs, logisim all passed. | None local. | None. |
| G7 | claim-check | 100 | 100 | Pass | `make negative-claims`: 52 dangerous claims checked; all 52 classified as unsupported with safe rewrite suggestions. | None local. | None. |
| G8 | corrupted tests | 100 | 100 | Pass | `make corrupted-tests`: 7 injected cases hit expected failure classes. | None local. | None. |
| G9 | scalability | 100 | 90 | Pass | `make scalability`: 1k, 3k, 5k, 10k synthetic rows generated; `reports/e5_scalability_summary.md` reports 10k pass. | Synthetic timing only, not a full memory profiler. | Keep wording as runtime-overhead smoke evidence, not performance proof. |
| G10 | docs | 98 | 85 | Pass local | README, CLI, API, schema, adapter, reproducibility, SoftwareX submission checklist, and release-readiness docs exist. | v0.1.2 DOI and author-side submission metadata remain. | Fill DOI after Zenodo publication and author metadata before journal submission. |
| G11 | license | 100 | 100 | Pass | `LICENSE` is Apache-2.0; metadata files reference Apache-2.0. | None local. | None. |
| G12 | citation | 80 | 100 | Pending external | v0.1.2 citation metadata is prepared but the v0.1.2 Zenodo DOI is pending. | DOI metadata cannot be finalized before Zenodo creates the new record. | Publish v0.1.2 release, wait for Zenodo DOI, apply DOI metadata, rerun external checker. |
| G13 | manuscript | 96 | 85 | Pass draft | `paper/softwarex_manuscript.md`, `.tex`, `highlights.md`, `declarations.md`, four generated figures, and `MANUSCRIPT_REPRO_PACKAGE.md` exist; manuscript text is expanded beyond skeleton while staying within the software-only boundary. | DOI, support email, funding, conflicts, and CRediT fields remain placeholders. | Fill DOI after Zenodo and author-side metadata before final journal submission. |
| G14 | boundary | 100 | 90 | Pass local | `make release-preflight` checks private paths, resource forks, forbidden wording contexts, capsule zip contents, and supplementary zip contents. | None local. | Keep gate review before final release. |
| D22 | supplementary artifact package | 100 | 100 | Pass local | `make supplementary-package` creates `release/artifactgate_eda_supplementary_artifacts.zip`; `make release-preflight` verifies required files inside it. | Release zip is generated and ignored by Git. | Regenerate after manuscript/report changes. |
| D2 | Python distribution package | 100 | 100 | Pass local | `make dist-package` creates sdist and wheel under `dist/`; `make release-preflight` verifies both files exist. | Dist artifacts are generated and ignored by Git. | Regenerate after source/package metadata changes. |

## Mentor Review

| Agent | Score | Pass/Fail | Critical Flaws | Minor Issues | Revision Actions | Change Skill/Resource? | Reduce Claim/Scope? | Next Iteration Target |
|---|---:|---|---|---|---|---|---|---|
| Engineering Mentor | 96 | Pass local | v0.1.2 external release is not yet published. | Package implementation is minimal but coherent. | Publish v0.1.2 and keep CI green after release metadata changes. | No. | No. | v0.1.2 release. |
| Codex Validator | 96 | Pass local | Final SoftwareX submission still needs author-side metadata. | Forbidden wording gate relies on context review. | Keep author-side placeholders explicit. | No. | No. | Submission packet. |
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
repository readiness, and manuscript draft gates pass. Final acceptance still
requires the v0.1.2 GitHub release, v0.1.2 Zenodo DOI, DOI metadata update,
external release checker pass, and author-side support email, funding,
competing interests, and CRediT confirmation.
