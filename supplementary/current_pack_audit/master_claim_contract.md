# Paper 2 Claim Contract: Claim-Safe EDA Artifact Evaluation

Date: 2026-06-18

Working title:

```text
Claim-Safe Artifact Evaluation for Reproducible EDA Research
```

## Core Claims

| ID | Claim | Current status | Required evidence |
| --- | --- | --- | --- |
| P2-C1 | The framework classifies EDA claims into evidence statuses. | `PLANNED` | Claim schema and examples across CircuitFaultBench and Spec2DFX. |
| P2-C2 | It detects unsupported claims in SPICE/ngspice and HDL/Yosys case studies. | `PLANNED` | Unsupported ledger for both case studies. |
| P2-C3 | It produces replayable evidence packages for selected cases. | `PARTIAL_EVIDENCE` | Existing packages plus unified replay checks. |
| P2-C4 | It generalizes across at least SPICE and HDL/synthesis artifact types. | `PLANNED` | CircuitFaultBench case + Spec2DFX case in the same schema. |

## Case Studies

| Case | Project | Role |
| --- | --- | --- |
| Case 1 | CircuitFaultBench | Main SPICE/ngspice benchmark and reproducibility case. |
| Case 2 | Spec2DFX | HDL simulation, Yosys synthesis, RM interface, unsupported-ledger case. |
| Appendix | LA-DFX | Simulation artifact case only. |
| Future extension | ReconfigRT-I | DFX/hardware artifact extension, not Paper 2 core method. |

## Forbidden Wording

- The framework validates DFX hardware.
- The framework proves DDC/DEL technical superiority.
- The framework is a full OS or full automation platform.
- The framework proves LLM quality or workflow speed.

## Allowed Current Wording

```text
This line studies claim-safe evidence classification, replay packaging, and unsupported-claim blocking for EDA experiments, first through SPICE/ngspice and HDL/Yosys case studies.
```
