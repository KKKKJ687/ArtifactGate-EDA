# Master Research Boundary

Date: 2026-06-18

## Unified Identity

```text
Evidence-gated runtime assurance and reproducible artifact evaluation for reconfigurable FPGA and EDA systems.
```

Chinese:

```text
面向可重构 FPGA 和 EDA 实验的证据门控、运行时保障、artifact consistency 与可复现实验体系。
```

## Main Lines

| Line | Main output | What it proves | What it must not claim yet |
| --- | --- | --- | --- |
| Paper 1: ReconfigRT-I | DFX runtime assurance paper | DDC + DEL can represent and block unsafe DFX runtime decisions under artifact drift. | Unsupported hardware-level system claims, physical acceleration claims, physical power claims, and production-use claims. |
| Paper 2: EDA Evidence Framework | Claim-safe artifact evaluation paper | EDA claims can be mapped to evidence layers, replay packages, and unsupported-claim blocking reports. | DDC/DEL technical superiority or hardware-level DFX validation. |

## Current Evidence Boundary

Current safe claims:

- software-level DFX scheduling simulation exists;
- HDL simulation and Yosys synthesis evidence exists for Spec2DFX;
- SPICE/ngspice benchmark and reproducibility evidence exists for CircuitFaultBench and original EEE-Agent-OS;
- ReconfigRT-I has software scaffold, DDC/DEL concepts, tests, and ResearchClaimOS governance.

Current blocked claims:

- completed Vivado DFX implementation;
- partial bitstream generation evidence;
- board-level DFX validation;
- ILA/serial log validated runtime behavior;
- hardware repeatability package;
- physical acceleration, power-saving, or production edge-AI deployment claims.

## Evidence Status Vocabulary

| Status | Meaning |
| --- | --- |
| `DIRECT_EVIDENCE` | Direct local artifact, command output, verified report, or dataset supports the claim. |
| `PARTIAL_EVIDENCE` | Some evidence exists, but a key layer is missing. |
| `INFERENCE` | Reasonable interpretation from evidence, not directly proven. |
| `PLANNED` | Planned work, no output yet. |
| `BLOCKED` | Blocked by hardware, toolchain, literature access, or human gate. |
| `UNSUPPORTED` | Must not be stated as fact. |

## Rule

Every new experiment, report, README update, paper draft, or application bullet must declare the target line and evidence status.
