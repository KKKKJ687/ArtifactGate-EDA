# Zenodo DOI Finalization

This note records the external DOI finalization for the SoftwareX release gate.
It is separate from local preflight because Zenodo publication creates
account-side external state.

## Current Verified State

- Public repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- GitHub release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.2
- Public CI: passing on `main`
- Local release preflight: passing
- Zenodo record: https://zenodo.org/records/20789516
- Zenodo DOI: 10.5281/zenodo.20789516

Public Zenodo version lookup confirms two versions under concept DOI
10.5281/zenodo.20789287:

- v0.1.2: 10.5281/zenodo.20789516
- v0.1.1: 10.5281/zenodo.20789288

The exact API checks used were:

```bash
curl -fsS https://zenodo.org/api/records/20789288/versions/latest

curl -fsS https://zenodo.org/api/records/20789288/versions

curl -fsS https://zenodo.org/api/records/20789516
```

Browser verification also confirmed the public record page title, version
`v0.1.2`, file `KKKKJ687/ArtifactGate-EDA-v0.1.2.zip`, and citation DOI.

## Account-Side Zenodo Steps Completed

Use the official Zenodo GitHub integration pages:

- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

Required account-side actions were:

1. Log in to Zenodo with the GitHub account that can access
   `KKKKJ687/ArtifactGate-EDA`.
2. Open the Zenodo GitHub integration page.
3. Sync GitHub repositories if `ArtifactGate-EDA` is not visible.
4. Enable the repository toggle for `KKKKJ687/ArtifactGate-EDA`.
5. Select the repository in Zenodo and process the `v0.1.2` GitHub release.
6. Wait for Zenodo to finish processing the release.
7. Copy the v0.1.2 version DOI: 10.5281/zenodo.20789516.
8. Confirm the Zenodo record links back to the GitHub repository.

Do not move or rewrite existing Git tags after Zenodo has archived them. If a
DOI-bearing source snapshot is required after metadata is committed, create a
follow-up patch release instead of mutating an archived tag.

## Local Finalization After DOI

The v0.1.2 DOI metadata was applied with:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA \
  --doi 10.5281/zenodo.20789516 \
  --release-date 2026-06-22 \
  --apply

make preflight

.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.2 \
  --doi 10.5281/zenodo.20789516
```

Expected final checker result:

```text
external release check: PASS
```

Inspect and commit only the DOI metadata updates:

```bash
git status --short --branch
git diff -- CITATION.cff codemeta.json .zenodo.json README.md paper/softwarex_manuscript.md paper/softwarex_manuscript.tex paper/declarations.md
```

## Completion Rule

The external release and DOI portion is complete when:

1. The Zenodo DOI exists and is publicly accessible.
2. DOI metadata is present in the repository and manuscript files.
3. `make preflight` passes after DOI metadata application.
4. `scripts/external_release_check.py --doi <real DOI>` passes, including the
   public Zenodo record check.
5. The final SoftwareX submission checklist has no unresolved external DOI
   blocker.
