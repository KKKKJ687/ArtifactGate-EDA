# E8 Codex/MCP Assisted Execution Audit

## Objective

E8 records how Codex/MCP-style tooling was used during engineering execution
without making Codex or MCP part of the software contribution, algorithm, or
reviewer dependency.

## Boundary

Codex/MCP-style tooling was used only as an engineering automation aid for
local commands, file edits, release checks, browser verification, and packaging
checks. The reproducibility path does not depend on Codex or MCP. All core
experiments are executable through the Makefile and the `artifactgate` CLI.

## Verified Non-Dependency Path

| Check | Evidence | Status |
|---|---|---|
| CLI-driven local reproduction | `make preflight` runs lint, pytest, smoke, ingestion, replay, negative claims, corrupted cases, scalability, baseline, manuscript package, release capsules, supplementary package, dist build, and release preflight. | PASS |
| External release verification | `scripts/external_release_check.py --repo KKKKJ687/ArtifactGate-EDA --tag v0.1.2 --doi 10.5281/zenodo.20789516` checks GitHub, latest main CI, release tag, local DOI metadata, and public Zenodo record. | PASS |
| Browser verification | Browser tooling was used only to inspect public GitHub and Zenodo pages after release. | PASS |
| Reviewer dependency | No reviewer needs Codex or MCP to run `make preflight`, inspect reports, or cite the archived release. | PASS |

## Safe Manuscript Wording

Codex/MCP-style tooling was used as an engineering automation aid for local
commands, code generation, packaging checks, and public-page verification. The
reproducibility path does not depend on Codex or MCP; all local checks are
executable through Makefile targets and CLI commands.

## Excluded Wording

Do not describe Codex or MCP as the claim-safety method, software contribution,
algorithmic novelty, or required reviewer environment.
