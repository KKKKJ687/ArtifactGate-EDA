# Paper 2 Spec2DFX Unsupported Ledger

Generated: 2026-06-19

| claim_id | unsupported_claim | blocked_by_missing_artifact | current_status | paper2_safe_wording | upgrade_condition |
|---|---|---|---|---|---|
| S2D-U01 | Vivado timing closure validated | real Vivado timing summary with WNS/TNS/clock/XDC/tool version/report hash | UNSUPPORTED | Vivado timing is not evaluated in this Stage 1 case. | Ingest real Vivado timing reports with hashes and provenance. |
| S2D-U02 | Vivado utilization evidence exists | real Vivado utilization report with device/tool/run provenance | UNSUPPORTED | Yosys utilization is recorded, but Vivado utilization is absent. | Ingest real Vivado utilization reports with hashes and provenance. |
| S2D-U03 | DFX partition implementation completed | real partition implementation report and constraints | UNSUPPORTED | DFX partition implementation is outside the current evidence layer. | Add real DFX partition reports and constraints. |
| S2D-U04 | Full bitstream generated and verified | full bitstream path/hash and generation log | UNSUPPORTED | Full bitstream generation is not claimed. | Add full bitstream, generation log, and hash manifest. |
| S2D-U05 | Partial bitstream generated and verified | partial bitstream path/hash and DFX report | UNSUPPORTED | Partial bitstream generation is not claimed. | Add partial bitstream, DFX report, and hash manifest. |
| S2D-U06 | Board-level DFX behavior validated | serial log, ILA/XRT capture, RM behavior-change evidence, partial loading record | UNSUPPORTED | Board validation is not claimed. | Add board logs and repeatable validation procedure. |
| S2D-U07 | Real FPGA speedup, energy benefit, or XC7Z010 DFX benefit proven | real measured static-vs-DFX comparison with reconfiguration overhead and repeatability | UNSUPPORTED | Real FPGA benefit is not claimed. | Replace synthetic rows with audited hardware measurements and repeatability evidence. |

