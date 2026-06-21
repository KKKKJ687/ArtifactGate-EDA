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

1. Create a public GitHub repository named `ArtifactGate-EDA`.
2. Push the local `main` branch.
3. Verify GitHub Actions passes on the public repository.
4. Create a version tag, for example `v0.1.0`.
5. Create a GitHub release from that tag and attach release capsules if desired.
6. Connect the GitHub release to Zenodo and reserve/publish a DOI.
7. Replace placeholder repository and DOI values in `CITATION.cff`,
   `codemeta.json`, `.zenodo.json`, `README.md`, and the manuscript.

The replacement step can be dry-run first:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/OWNER/ArtifactGate-EDA \
  --doi 10.xxxx/zenodo.xxxxxxx \
  --release-date YYYY-MM-DD
```

Apply only after the public repository and DOI are real:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/OWNER/ArtifactGate-EDA \
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
  --repo OWNER/ArtifactGate-EDA \
  --tag v0.1.0 \
  --doi 10.xxxx/zenodo.xxxxxxx
```

This check is intentionally not part of `make preflight` because it should fail
until the public repository, live CI run, release tag, and DOI exist.

## Current Local Blockers

No local blocker is known after `make reproduce-all` and `make package-release`.
No local blocker is known after `make preflight`. Public repository, CI run
evidence, GitHub release, and Zenodo DOI remain external authorization
blockers.

## GitHub Connector Status

The available GitHub connector can operate on existing repositories: read
metadata and files, create blobs/trees/commits/refs, create files, and inspect
workflow runs. It does not expose a repository-creation tool in this session.
The next release step therefore requires either an existing empty
`owner/name` repository or explicit authorization to use local `gh` CLI after
`gh auth login`.

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
