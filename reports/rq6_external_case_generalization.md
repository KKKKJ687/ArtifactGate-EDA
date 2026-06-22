# RQ6 External Case Generalization

This benchmark uses public, software-only EDA artifacts. Replayable cases are processed through ArtifactGate replay-packaging and validation using ngspice, Yosys, or Verilator artifact adapters. Logisim cases are metadata-only.

The benchmark does not execute external EDA simulators or synthesis tools. No case is treated as hardware validation, Vivado timing closure, bitstream, DFX deployment, or board-level evidence.

## Summary

| metric | value | target | status |
| --- | ---: | --- | --- |
| external_cases | 10 | >=10 | PASS |
| open_source_replayable_cases | 8 | >=6 | PASS |
| case_success_rate | 1 | >=0.95 | PASS |
| adapter_success_rate | 1 | >=0.95 | PASS |
| manual_adapter_fix_rate | 0 | <=0.10 | PASS |
| hardware_dependency_count | 0 | 0 | PASS |
| commercial_dependency_count | 0 | 0 | PASS |
| open_source_artifactgate_replay_package_success_rate | 1 | >=0.95 | PASS |
| metadata_only_success_rate | 1 | >=0.95 | PASS |

## Cases

| case_id | expected_adapter | detected_adapter | replayable_open_source | metadata_only | artifact_count | observed_manual_fix | observed_hardware_dependency | status |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| logisim_combinational_circuit | logisim | logisim | no | yes | 1 | no | no | PASS |
| logisim_example_1 | logisim | logisim | no | yes | 1 | no | no | PASS |
| ngspice_gain_stage | ngspice | ngspice | yes | no | 1 | no | no | PASS |
| ngspice_param_sweep | ngspice | ngspice | yes | no | 1 | no | no | PASS |
| ngspice_rc_meas_ac | ngspice | ngspice | yes | no | 1 | no | no | PASS |
| verilator_make_hello_c | verilator | verilator | yes | no | 1 | no | no | PASS |
| verilator_make_tracing_c | verilator | verilator | yes | no | 2 | no | no | PASS |
| yosys_cmos_counter | yosys | yosys | yes | no | 3 | no | no | PASS |
| yosys_osu035_example | yosys | yosys | yes | no | 2 | no | no | PASS |
| yosys_smtbmc_demo1 | yosys | yosys | yes | no | 1 | no | no | PASS |
