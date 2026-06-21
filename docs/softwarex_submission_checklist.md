# SoftwareX Submission Checklist

This checklist is based on the SoftwareX Original Software Publication template
downloaded from Elsevier on 2026-06-22 and the public SoftwareX GitHub
organization.

## Template Requirements

| Requirement | Local Status | Evidence |
|---|---|---|
| Use the SoftwareX Original Software Publication structure | Partial local pass | `paper/softwarex_manuscript.md`, `paper/softwarex_manuscript.tex` |
| Public GitHub repository in metadata table | External pass | https://github.com/KKKKJ687/ArtifactGate-EDA |
| Well documented README | Local pass | `README.md`, `docs/` |
| Licence.txt file | Local pass | `Licence.txt`, `LICENSE` |
| Main body focused on software | Local pass | `paper/softwarex_manuscript.md` |
| 4000-word body limit | Local pass skeleton | Manuscript is currently below this limit |
| Maximum six figures | Local pass | 4 generated figures under `paper/figures/` |
| Five main templated sections | Local pass skeleton | Motivation, Software description, Illustrative examples, Impact, Conclusions |
| Metadata table C1-C8 | Local pass with blockers marked | `paper/softwarex_manuscript.md` |
| Repository archive and DOI | Partial external pass | GitHub release exists at https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.1; Zenodo DOI remains pending |

## Verified External State

- Public repository: https://github.com/KKKKJ687/ArtifactGate-EDA
- Passing CI run: https://github.com/KKKKJ687/ArtifactGate-EDA/actions/runs/27919622621
- GitHub release: https://github.com/KKKKJ687/ArtifactGate-EDA/releases/tag/v0.1.1

## External Sources Checked

- Elsevier SoftwareX OSP template: https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.docx
- Public SoftwareX GitHub organization: https://github.com/ElsevierSoftwareX

## Remaining Submission Blockers

1. Zenodo DOI.
2. Author-side support email, funding, competing interest, and CRediT metadata.
3. Final manuscript polish against the released repository URL and DOI.
4. Final external release check with the real DOI.

Zenodo account-side steps and local DOI metadata commands are documented in
`docs/zenodo_doi_finalization.md`.
