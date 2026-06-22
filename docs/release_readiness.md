# Release Readiness

## Local Release Commands

```bash
make install
make reproduce-all
make package-release
make supplementary-package
make dist-package
make release-preflight
```

## Required External Release Steps

These steps are intentionally not automated because they create or publish
external state.

1. Done: create a public GitHub repository named `ArtifactGate-EDA`.
2. Done: push the local `main` branch.
3. Done: verify GitHub Actions passes on the public repository.
4. Done: create the `v0.1.2` version tag for Zenodo ingestion.
5. Done: create a GitHub release from that tag and attach release artifacts.
6. Done: connect the v0.1.2 GitHub release to Zenodo and publish a DOI.
7. Done: replace DOI values in `CITATION.cff`,
   `codemeta.json`, `.zenodo.json`, `README.md`, and the manuscript.

Detailed DOI handoff: `docs/zenodo_doi_finalization.md`.

The DOI metadata replacement can be dry-run first:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA \
  --doi 10.5281/zenodo.20789516 \
  --release-date 2026-06-22
```

Apply after the public v0.1.2 DOI is real:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA \
  --doi 10.5281/zenodo.20789516 \
  --release-date 2026-06-22 \
  --apply
```

After those steps, verify the external gates with:

```bash
make external-release-check
```

or, when the repository/DOI are not inferable from local metadata yet:

```bash
.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.2 \
  --doi 10.5281/zenodo.20789516
```

This check is intentionally not part of `make preflight` because it depends on
public GitHub, GitHub Actions, release, and Zenodo state.

## Verified External State

- Public repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Public CI: verified by `scripts/external_release_check.py`
- GitHub release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.2
- Zenodo record: https://zenodo.org/records/20789516
- Zenodo DOI: 10.5281/zenodo.20789516

## Current Codex-Verifiable Status

No local blocker is known after `make reproduce-all`, `make package-release`,
and `make preflight`. Public repository, v0.1.2 GitHub release, Zenodo DOI,
DOI metadata, generated reports, manuscript package, and supplementary package
are complete.

Author-side SoftwareX submission metadata remains a user-side value packet, not
a Codex-verifiable engineering blocker.

## GitHub Connector Status

The public GitHub release work uses authenticated local `gh` CLI access. Zenodo
publication requires the GitHub-Zenodo integration to process the v0.1.2
release.

## External Release Check Contract

`scripts/external_release_check.py` is read-only. It checks:

- local release zips and Python distribution files exist
- repository and release placeholders have been replaced in local metadata
- a Zenodo DOI has been supplied and recorded
- the supplied Zenodo DOI resolves to a public record for ArtifactGate-EDA
- `gh` is authenticated
- the target GitHub repository exists and is public
- the latest `main` GitHub Actions run completed successfully
- the expected GitHub release tag exists and is not a draft

`scripts/prepare_release_metadata.py` is the companion write tool. It is dry-run
by default and requires `--apply` before it changes files.
