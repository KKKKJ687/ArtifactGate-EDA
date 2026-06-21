# Zenodo DOI Finalization

This note is the final external handoff for the SoftwareX release gate. It is
separate from local preflight because Zenodo publication creates account-side
external state.

## Current Verified State

- Public repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- GitHub release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.2
- Public CI: passing on `main`
- Local release preflight: passing
- Zenodo DOI: pending for v0.1.2

Public Zenodo searches should find the v0.1.2 ArtifactGate-EDA record after
Zenodo processes the GitHub release.

- Record: pending
- DOI: pending

The exact searches used were:

```bash
curl -fsS --get \
  --data-urlencode 'q="ArtifactGate-EDA"' \
  --data-urlencode 'size=10' \
  https://zenodo.org/api/records

curl -fsS --get \
  --data-urlencode 'q="https://github.com/KKKKJ687/ArtifactGate-EDA"' \
  --data-urlencode 'size=10' \
  https://zenodo.org/api/records
```

The title search returned the public record. The repository URL search may not
match Zenodo metadata text directly, so the final checker validates the record
by DOI and title.

## Account-Side Zenodo Steps

Use the official Zenodo GitHub integration pages:

- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

Required account-side actions:

1. Log in to Zenodo with the GitHub account that can access
   `KKKKJ687/ArtifactGate-EDA`.
2. Open the Zenodo GitHub integration page.
3. Sync GitHub repositories if `ArtifactGate-EDA` is not visible.
4. Enable the repository toggle for `KKKKJ687/ArtifactGate-EDA`.
5. Select the repository in Zenodo and process the `v0.1.2` GitHub release.
6. Wait for Zenodo to finish processing the release.
7. Copy the v0.1.2 version DOI.
8. Confirm the Zenodo record links back to the GitHub release/repository.

Do not move or rewrite existing Git tags after Zenodo has archived them. If a
DOI-bearing source snapshot is required after metadata is committed, create a
follow-up patch release instead of mutating an archived tag.

## Local Finalization After DOI

After the v0.1.2 DOI exists, apply DOI metadata with:

```bash
.venv/bin/python scripts/prepare_release_metadata.py \
  --repo-url https://github.com/KKKKJ687/ArtifactGate-EDA \
  --doi <v0.1.2 DOI> \
  --release-date 2026-06-22 \
  --apply

make preflight

.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.2 \
  --doi <v0.1.2 DOI>
```

Expected final checker result:

```text
external release check: PASS
```

Then inspect and commit only the DOI metadata updates:

```bash
git status --short --branch
git diff -- CITATION.cff codemeta.json .zenodo.json README.md paper/softwarex_manuscript.md paper/softwarex_manuscript.tex paper/declarations.md
```

## Completion Rule

The original execution plan is not complete until:

1. The Zenodo DOI exists and is publicly accessible.
2. DOI metadata is present in the repository and manuscript files.
3. `make preflight` passes after DOI metadata application.
4. `scripts/external_release_check.py --doi <real DOI>` passes, including the
   public Zenodo record check.
5. The final SoftwareX submission checklist has no unresolved external DOI
   blocker.
