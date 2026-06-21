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
      create the `v0.1.0` GitHub release.
- [x] Add DOI finalization handoff for Zenodo account-side publication.
- [ ] Complete remaining external blockers: Zenodo DOI and SoftwareX final
      submission package.

## Next Gate

Complete the DOI and final submission gate. Local reproducibility already
passes with:

```bash
make preflight
```

Verified public release state:

- Repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Passing CI run: https://github.com/KKKKJ687/ArtifactGate-EDA/actions/runs/27919622621
- Release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.0

Zenodo DOI finalization steps are in `docs/zenodo_doi_finalization.md`.

After Zenodo publication, run the external checker with the real DOI:

```bash
.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.0 \
  --doi 10.xxxx/zenodo.xxxxxxx
```
