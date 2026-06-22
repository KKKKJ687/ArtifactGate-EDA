# Literature Search Protocol

Generated: 2026-06-22

This file records the reproducible protocol for the IST literature map. The matrix combines primary official documentation, standards, named papers identified in the stronger optimization plan, web-verified primary sources, logged database/search passes, and machine-verifiable citation-network follow-up. Google Scholar and some ScienceDirect content remain limited by machine-access constraints; citation expansion is therefore verified through OpenAlex/DOI/public metadata and the output remains a systematic mapping support artifact rather than a PRISMA-complete systematic review.

## Databases And Sources

| Source | Current status |
|---|---|
| ACM Digital Library | seed papers and policies mapped where public metadata/DOI is available |
| IEEE Xplore | empirical-SE guideline plus ACM/IEEE MLCAD EDA artifact row mapped |
| ScienceDirect | IST scope and software-engineering context mapped from public pages |
| SpringerLink | empirical SE methodology mapped through public book/DOI metadata |
| arXiv | mflowgen and related open EDA flow paper mapped |
| Google Scholar / citation network | direct Scholar unavailable; OpenAlex/DOI/public metadata used for reproducible citation expansion |
| GitHub / official docs | official tool and policy pages mapped directly |

## Search Strings

- computational reproducibility package capsule environment provenance
- artifact evaluation badging reproducibility software engineering
- EDA workflow manager reproducibility FuseSoC Edalize OpenROAD OpenLane Hammer mflowgen SiliconCompiler
- software provenance attestation SLSA in-toto policy as code artifact integrity
- Goal Question Metric empirical software engineering experimentation case study systematic mapping
- FPGA EDA artifact evaluation reproducibility MLCAD

## Inclusion Criteria

- I1: computational reproducibility or artifact packaging
- I2: artifact evaluation, artifact review, or badging
- I3: EDA workflow, build, simulation, synthesis, or tool interfacing
- I4: provenance, attestation, policy, or traceability
- I5: empirical software engineering research design
- I6: EDA/FPGA/MLCAD artifact evaluation practice

## Exclusion Criteria

- E1: hardware implementation only, without software artifact relevance
- E2: EDA algorithm performance only, without artifact or reproducibility concern
- E3: generic writing advice without SE/AE/reproducibility relevance
- E4: no accessible abstract, method, specification, or official documentation
- E5: unrelated to software-only EDA artifacts

## Mapped Categories

- artifact_evaluation_badging
- computational_reproducibility_packaging
- eda_fpga_artifact_practice
- eda_workflow_build_tools
- empirical_se_methodology
- provenance_policy_traceability
