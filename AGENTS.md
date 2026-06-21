# ArtifactGate-EDA Codex Rules

These rules apply to this repository unless a closer `AGENTS.md` overrides them.

## Project Boundary

ArtifactGate-EDA is a SoftwareX-oriented Python software package for claim-safe
artifact evaluation in software-only EDA experiments. It is not a hardware
validation, Vivado timing, DFX deployment, bitstream, or board-validation
project.

## Start Of Every Task

- Read this file, `README.md`, `TODO.md`, and relevant files under `docs/`.
- Run `git status --short --branch` before making claims or edits.
- Preserve source evidence under `examples/` and `supplementary/`.
- Keep all paths portable. Do not write private absolute paths into generated
  artifacts.

## Claim Boundary

Allowed positive evidence ceiling in the SoftwareX core: `L4_SYNTHESIS`.

Unsupported unless real artifacts are added and audited:

- hardware validation
- Vivado timing or implementation evidence
- full or partial bitstreams
- DFX deployment or runtime DFX validation
- board-level behavior
- real FPGA speedup or energy saving

## Git Safety

- Do not commit unless the user explicitly asks.
- Do not push or create a GitHub repository unless the user explicitly asks and
  authentication is verified.
- Do not run destructive rollback or cleanup commands such as `git reset --hard`
  or `git clean -fd` unless the user explicitly approves the exact command.

## Verification

Run the narrowest meaningful check after each work packet:

- `python -m pip install -e ".[dev]"`
- `artifactgate --help`
- `pytest`
- `make smoke`
- `make negative-claims`
- `make corrupted-tests`

