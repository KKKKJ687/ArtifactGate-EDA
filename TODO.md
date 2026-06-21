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
- [ ] Publish Zenodo DOI for v0.1.2 and apply DOI metadata.
- [x] Polish the SoftwareX manuscript draft against released repository and DOI.
- [x] Add author-side metadata request checklist.
- [ ] Complete author-side SoftwareX final submission metadata.

## Next Gate

Complete the v0.1.2 DOI and author-side final submission metadata gate. Local
reproducibility already passes with:

```bash
make preflight
```

Verified public release state:

- Repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Public CI: verified by `scripts/external_release_check.py`
- Release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.2
- Zenodo DOI: pending for v0.1.2

Final external checker after the v0.1.2 DOI is public:

```bash
.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.2 \
  --doi <v0.1.2 DOI>
```
