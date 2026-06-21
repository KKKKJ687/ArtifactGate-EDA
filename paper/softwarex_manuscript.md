# ArtifactGate-EDA: An Adapter-Based Claim-Safe Artifact Evaluation Framework for Software-Only EDA Experiments

## Highlights

- Claim-safe artifact packaging for software-only EDA experiments.
- Adapter-based ingestion for ngspice, HDL simulation, and Yosys evidence.
- Negative claim tests block hardware, bitstream, and board-level overclaim.

## Metadata

| Nr | Code metadata description | Metadata |
|---|---|---|
| C1 | Current code version | 0.1.1 |
| C2 | Permanent link to code/repository used for this code version | https://github.com/KKKKJ687/ArtifactGate-EDA |
| C3 | Legal code license | Apache-2.0 |
| C4 | Code versioning system used | git |
| C5 | Software code languages, tools and services used | Python, Makefile, GitHub Actions, ngspice-style artifacts, Icarus/VVP-style artifacts, Yosys-style artifacts |
| C6 | Compilation requirements, operating environments and dependencies | Python >=3.10; dependencies listed in `pyproject.toml`; core replay does not require commercial EDA software |
| C7 | Developer documentation/manual | `README.md` and `docs/` in the repository |
| C8 | Support email for questions | Pending author-side release metadata |

## Motivation And Significance

EDA artifact packages often mix source files, simulator logs, synthesis reports,
metadata, replay commands, and paper claims. ArtifactGate-EDA provides a
software layer for indexing these artifacts, assigning evidence levels, checking
claim support, and generating reviewer-readable reports.

## Software Description

![Architecture](figures/architecture.png)

The package provides command-line tools for ingestion, validation, replay,
claim checking, reporting, packaging, and drift comparison.

![Workflow](figures/workflow.png)

## Illustrative Examples

The repository includes bounded examples for ngspice-style SPICE artifacts,
HDL/Icarus simulation artifacts, Yosys synthesis artifacts, Verilator logs,
PLECS metadata-only artifacts, and Logisim metadata-only artifacts. The
corrupted artifact and negative claim examples exercise the failure modes that
reviewers are expected to inspect.

![Evidence levels](figures/evidence_levels.png)

## Impact

ArtifactGate-EDA complements generic reproducibility tooling by adding
EDA-specific evidence levels, unsupported-claim ledgers, and reviewer-facing
artifact reports. Its intended impact is narrower and safer than proving design
correctness: it makes software-level evidence boundaries explicit.

![Experiment matrix](figures/experiment_matrix.png)

## Conclusions

ArtifactGate-EDA packages heterogeneous software-only EDA artifacts into
hash-recorded, replay-checkable, and claim-auditable bundles. Local evaluation
covers installation, smoke tests, multi-adapter ingestion, replay summaries,
negative claim injection, corrupted artifact detection, scalability summaries,
and artifact-management baseline comparison.

## Limitations

ArtifactGate-EDA does not validate hardware, Vivado timing, DFX deployment,
bitstreams, or board-level behavior. It prevents unsupported escalation from
software, simulation, and synthesis artifacts to stronger claims.

## Availability

Repository: https://github.com/KKKKJ687/ArtifactGate-EDA. The archived Zenodo
DOI will be added before SoftwareX submission.
