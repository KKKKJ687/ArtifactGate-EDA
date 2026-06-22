# ArtifactGate-EDA Work Queue

## Active Work Packet

- [x] Initialize clean Git repository.
- [x] Create SoftwareX-safe repository skeleton.
- [x] Add execution contract and workflow state.
- [x] Implement installable Python package skeleton.
- [x] Migrate curated CircuitFaultBench and Spec2DFX seed artifacts into
      `examples/` and `supplementary/`.
- [x] Expand adapters and tests to cover local E0-E6 plan gates.
- [x] Generate SoftwareX manuscript skeleton from verified outputs.
- [x] Add reproducible figures, manuscript package map, and SoftwareX v6
      submission checklist.
- [x] Add local supplementary artifact package and release preflight gates.
- [x] Pass full local preflight, including Python sdist/wheel generation.
- [x] Add read-only external release checker for public repo, CI, release tag,
      DOI, and metadata replacement.
- [x] Add dry-run-first metadata replacement helper for public repo URL, DOI,
      and release date.
- [x] Publish public GitHub repository, push `main`, verify live CI, and
      create the `v0.1.2` GitHub release for Zenodo ingestion.
- [x] Add DOI finalization handoff for Zenodo account-side publication.
- [x] Publish Zenodo DOI for v0.1.2 and apply DOI metadata.
- [x] Polish the SoftwareX manuscript draft against released repository and DOI.
- [x] Add author-side metadata request checklist.
- [x] Complete all Codex-verifiable engineering, release, DOI, report, and
      manuscript-package gates.

## Next Gate

All Codex-verifiable gates are complete. Local reproducibility passes with:

```bash
make preflight
```

Verified public release state:

- Repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Public CI: verified by `scripts/external_release_check.py`
- Release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.2
- Zenodo record: https://zenodo.org/records/20789516
- Zenodo DOI: 10.5281/zenodo.20789516

Final external checker:

```bash
.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.2 \
  --doi 10.5281/zenodo.20789516
```

## User-Side Submission Values

Final journal submission still requires author-provided values that Codex
cannot infer safely:

- support email
- funding statement
- competing interests declaration
- CRediT author roles

The request packet is `docs/author_submission_metadata_request.md`.
