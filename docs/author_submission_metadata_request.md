# Author-Side Submission Metadata Request

This file lists the remaining values that cannot be inferred safely from the
repository. Fill these before final SoftwareX submission.

## Required Values

| Field | Needed value | Current status |
|---|---|---|
| Support email | Email address to put in SoftwareX metadata field C8. | Pending author confirmation |
| Funding statement | Exact funding text. If there was no funding, confirm the no-funding wording. | Pending author confirmation |
| Competing interests | Exact declaration. If none, confirm the no-conflict wording. | Pending author confirmation |
| CRediT roles | Contributor roles for Xinzhi Lei, using the CRediT taxonomy. | Pending author confirmation |

## Suggested Safe Options For Confirmation

These are not applied automatically. The author must confirm or replace them.

| Field | Possible text |
|---|---|
| Funding | This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. |
| Competing interests | The author declares no competing interests. |
| CRediT roles | Xinzhi Lei: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing - original draft, Writing - review and editing, Visualization. |

## Before Submission

1. Replace the pending support email in `paper/softwarex_manuscript.md` and
   `paper/softwarex_manuscript.tex`.
2. Replace the pending Funding, Competing Interests, and CRediT sections in
   `paper/declarations.md`.
3. Re-run:

```bash
make preflight
.venv/bin/python scripts/external_release_check.py \
  --repo KKKKJ687/ArtifactGate-EDA \
  --tag v0.1.2 \
  --doi 10.5281/zenodo.20789516
```
