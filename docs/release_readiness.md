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
4. Done: create the `v0.1.0` version tag.
5. Done: create a GitHub release from that tag and attach release artifacts.
6. Pending: connect the GitHub release to Zenodo and reserve/publish a DOI.
7. Pending: replace DOI values in `CITATION.cff`,
   `codemeta.json`, `.zenodo.json`, `README.md`, and the manuscript.

The replacement step can be dry-run first:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA \
  --doi 10.xxxx/zenodo.xxxxxxx \
  --release-date YYYY-MM-DD
```

Apply only after the public repository and DOI are real:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA \
  --doi 10.xxxx/zenodo.xxxxxxx \
  --release-date YYYY-MM-DD \
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
  --tag v0.1.0 \
  --doi 10.xxxx/zenodo.xxxxxxx
```

This check is intentionally not part of `make preflight` because it should fail
until the external DOI exists.

## Verified External State

- Public repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Passing CI run: https://github.com/KKKKJ687/ArtifactGate-EDA/actions/runs/27919622621
- GitHub release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.0

## Current Local Blockers

No local blocker is known after `make reproduce-all`, `make package-release`,
and `make preflight`. Public repository, CI run evidence, and GitHub release
are complete. Zenodo DOI and final DOI metadata remain external blockers.

## GitHub Connector Status

The public GitHub release work has been completed with authenticated local
`gh` CLI access. The remaining release step is account-side Zenodo publication
and DOI metadata application.

## External Release Check Contract

`scripts/external_release_check.py` is read-only. It checks:

- local release zips and Python distribution files exist
- repository and release placeholders have been replaced in local metadata
- a Zenodo DOI has been supplied and recorded
- `gh` is authenticated
- the target GitHub repository exists and is public
- the latest `main` GitHub Actions run completed successfully
- the expected GitHub release tag exists and is not a draft

`scripts/prepare_release_metadata.py` is the companion write tool. It is dry-run
by default and requires `--apply` before it changes files.
