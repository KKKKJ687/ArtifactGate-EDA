# SoftwareX Submission Checklist

This checklist is based on the SoftwareX Original Software Publication template
downloaded from Elsevier on 2026-06-22 and the public SoftwareX GitHub
organization.

## Template Requirements

| Requirement | Local Status | Evidence |
|---|---|---|
| Use the SoftwareX Original Software Publication structure | Local pass with author metadata pending | `paper/softwarex_manuscript.md`, `paper/softwarex_manuscript.tex` |
| Public GitHub repository in metadata table | External pass | https://github.com/KKKKJ687/ArtifactGate-EDA |
| Well documented README | Local pass | `README.md`, `docs/` |
| Licence.txt file | Local pass | `Licence.txt`, `LICENSE` |
| Main body focused on software | Local pass | `paper/softwarex_manuscript.md` |
| 4000-word body limit | Local pass | Manuscript is below this limit |
| Maximum six figures | Local pass | 4 generated figures under `paper/figures/` |
| Five main templated sections | Local pass | Motivation, Software description, Illustrative examples, Impact, Conclusions |
| Metadata table C1-C8 | Pass with author-side fields pending | `paper/softwarex_manuscript.md` |
| Repository archive and DOI | Pending external v0.1.2 DOI | GitHub release target: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.2; Zenodo DOI pending for v0.1.2 |

## Verified External State

- Public repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Public CI: verified by `scripts/external_release_check.py`
- GitHub release: pending v0.1.2 publication
- Zenodo DOI: pending for v0.1.2

## External Sources Checked

- Elsevier SoftwareX OSP template: https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.docx
- Public SoftwareX GitHub organization: https://github.com/ElsevierSoftwareX

## Remaining Submission Blockers

1. Author-side support email, funding, competing interest, and CRediT metadata.

The remaining author-side values are listed in
`docs/author_submission_metadata_request.md`. The final external release check
must be rerun after the v0.1.2 Zenodo DOI is public.
