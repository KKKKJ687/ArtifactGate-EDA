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
- [ ] Complete external release blockers: public GitHub repository, live CI
      pass, GitHub release, Zenodo DOI, and SoftwareX final submission package.

## Next Gate

Complete the external release gate. Local reproducibility already passes with:

```bash
make preflight
```

The GitHub connector can operate on an existing repository but does not expose a
repository-creation tool. Provide an existing empty `owner/name` repository or
authorize local `gh` CLI login and repository creation before push/CI/DOI work.

After external publication, run:

```bash
make external-release-check
```
