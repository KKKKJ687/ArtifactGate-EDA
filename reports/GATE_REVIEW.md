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
| G2 | install | 100 | 100 | Pass | `make install`; `.venv/bin/artifactgate --version` returned `0.1.0`. | None local. | None. |
| G3 | CLI | 95 | 90 | Pass | CLI exposes `ingest`, `validate`, `replay`, `claim-check`, `report`, `package`, `compare`, plus local summary helpers. | Core commands are intentionally minimal. | Expand API ergonomics only after release blocker work. |
| G4 | tests/lint | 100 | 100 | Pass | `make reproduce-all` ran `ruff`, `compileall`, and `pytest`: 14 passed. | None local. | None. |
| G5 | CI | 80 | 100 | Blocked external | `.github/workflows/ci.yml` exists and now calls `make lint`, tests, smoke, negative claims, corrupted tests, scalability, baseline, and summaries. Makefile supports both local `.venv` and CI PATH tools. | No public remote run has been observed. | Create/push GitHub repo only after explicit user approval, then verify Actions. |
| G6 | examples | 100 | 100 | Pass | `make ingest-all`: ngspice, icarus, yosys, verilator, plecs, logisim all passed. | None local. | None. |
| G7 | claim-check | 100 | 100 | Pass | `make negative-claims`: 52 dangerous claims checked; expected unsupported-claim failure observed. | None local. | None. |
| G8 | corrupted tests | 100 | 100 | Pass | `make corrupted-tests`: 7 injected cases hit expected failure classes. | None local. | None. |
| G9 | scalability | 100 | 90 | Pass | `make scalability`: 1k, 3k, 5k, 10k synthetic rows generated; `reports/e5_scalability_summary.md` reports 10k pass. | Synthetic timing only, not a full memory profiler. | Keep wording as runtime-overhead smoke evidence, not performance proof. |
| G10 | docs | 95 | 85 | Pass local | README, CLI, API, schema, adapter, reproducibility, SoftwareX submission checklist, and release-readiness docs exist. | Public URL/DOI placeholders remain. | Replace placeholders after external release. |
| G11 | license | 100 | 100 | Pass | `LICENSE` is Apache-2.0; metadata files reference Apache-2.0. | None local. | None. |
| G12 | citation | 80 | 100 | Blocked external | `CITATION.cff`, `codemeta.json`, and `.zenodo.json` exist. | No Zenodo DOI yet. | Archive release on Zenodo after GitHub release. |
| G13 | manuscript | 90 | 85 | Pass skeleton | `paper/softwarex_manuscript.md`, `.tex`, `highlights.md`, `declarations.md`, four generated figures, and `MANUSCRIPT_REPRO_PACKAGE.md` exist. | Public repository URL, DOI, support email, funding, conflicts, and CRediT fields are placeholders. | Fill author-side metadata and DOI after release. |
| G14 | boundary | 100 | 90 | Pass local | `make release-preflight` checks private paths, resource forks, forbidden wording contexts, capsule zip contents, and supplementary zip contents. | None local. | Keep gate review before final release. |
| D22 | supplementary artifact package | 100 | 100 | Pass local | `make supplementary-package` creates `release/artifactgate_eda_supplementary_artifacts.zip`; `make release-preflight` verifies required files inside it. | Release zip is generated and ignored by Git. | Regenerate after manuscript/report changes. |
| D2 | Python distribution package | 100 | 100 | Pass local | `make dist-package` creates sdist and wheel under `dist/`; `make release-preflight` verifies both files exist. | Dist artifacts are generated and ignored by Git. | Regenerate after source/package metadata changes. |

## Mentor Review

| Agent | Score | Pass/Fail | Critical Flaws | Minor Issues | Revision Actions | Change Skill/Resource? | Reduce Claim/Scope? | Next Iteration Target |
|---|---:|---|---|---|---|---|---|---|
| Engineering Mentor | 94 | Pass local | Public CI and DOI are not locally verifiable. | Package implementation is minimal but coherent. | Verify on GitHub Actions after remote creation. | No. | No. | Release readiness. |
| Codex Validator | 92 | Pass local | Final acceptance cannot be declared while G5/G12 are external blockers. | Forbidden wording gate relies on context review. | Keep blocked gates explicit in status files. | No. | No. | External release packet. |
| Reviewer | 88 | Pass skeleton | Manuscript still requires public URL, DOI, author declarations, and final prose polish. | Figures are generated and source-backed but not externally reviewed. | Expand/polish manuscript only from generated reports. | No. | No. | SoftwareX submission polish. |

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

Local engineering, manuscript-package, and supplementary-package gates pass.
Final project acceptance is not complete because G5 requires an observed GitHub
Actions run on a public repository and G12 requires a Zenodo DOI. Those external
actions require user authorization and release metadata.
