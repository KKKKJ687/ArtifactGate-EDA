# Unsupported Ledger

Generated: 2026-06-19T01:41:21

| id | claim | status | reason | unlock_evidence_required |
| --- | --- | --- | --- | --- |
| UNSUP-001 | FPGA/DFX/Vivado/partial-bitstream implementation evidence | UNSUPPORTED | No current CFB artifact contains FPGA, Vivado/Vitis, bitstream, timing, or board data. | Separate FPGA project with synthesis/implementation logs, constraints, bitstreams, and board traces. |
| UNSUP-002 | Board-level or hardware diagnostic validation | UNSUPPORTED | Phase6/8 manifests explicitly show hardware_required=false and only SPICE/ngspice simulation. | Board experiment protocol, hardware setup, captured traces, and acceptance report. |
| UNSUP-003 | Exact external benchmark reproduction completed | BLOCKED | Phase8 is proxy_aligned_not_exact; Phase9 is Gate 0/1 control readiness only. | Source-verified schematics, fault-mode crosswalk, exact reproduction runs, and acceptance report. |
| UNSUP-004 | SCI submission ready or journal accepted | UNSUPPORTED | Phase6 final acceptance states SCI SUBMISSION READINESS: NOT YET. | Advisor-approved manuscript, external benchmark closure, journal checklist, and submission package. |
| UNSUP-005 | Real-world diagnostic validity or exhaustive analog benchmark coverage | UNSUPPORTED | Current case is controlled SPICE/ngspice evidence, not field validation. | External datasets, broader circuit coverage, statistical validation, and real-world trace evidence. |
| UNSUP-006 | Paper1/ReconfigRT-I performance or hardware claim from CFB metrics | UNSUPPORTED | CFB metrics are analog-fault SPICE metrics, not runtime scheduling or FPGA metrics. | ReconfigRT-I-specific experiments, hardware/software traces, and claim contract. |
| UNSUP-007 | DFX runtime scheduling project | UNSUPPORTED | Current CFB artifacts are SPICE/ngspice evidence-gating artifacts, not DFX runtime artifacts. | ReconfigRT-I or LA-DFX runtime traces, scheduler logs, partial reconfiguration evidence, and claim contract. |
| UNSUP-008 | FPGA implementation evidence | UNSUPPORTED | No current CFB artifact contains an FPGA implementation, HDL integration, synthesis, implementation, timing, or bitstream record. | Vivado/Vitis project, HDL integration, synthesis/implementation logs, timing reports, bitstream, and acceptance report. |
| UNSUP-009 | hardware validation | UNSUPPORTED | No current CFB artifact contains board logs, ILA traces, serial logs, lab setup records, or physical repeatability data. | Board experiment protocol, setup photos/notes, captured traces, repeatability table, and hardware acceptance report. |
| UNSUP-010 | journal-ready benchmark quality | UNSUPPORTED | The current stage is a claim-safe software evidence package; it is not an externally reproduced, reviewer-complete benchmark package. | Exact external reproduction, broader benchmark coverage, reviewer-risk closure, manuscript figures, citations, and journal checklist. |
