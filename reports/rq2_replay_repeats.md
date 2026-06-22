# RQ2 Replay Repeatability

| case | adapter | completed_repeats | passed_repeats | unique_artifact_signatures | drift_detected | artifact_count | status |
|---|---|---:|---:|---:|---|---:|---|
| rq2_ngspice_minimal | ngspice | 10 | 10 | 1 | no | 79 | PASS |
| rq2_cfb_sample | ngspice | 10 | 10 | 1 | no | 4 | PASS |
| rq2_icarus | icarus | 10 | 10 | 1 | no | 90 | PASS |
| rq2_verilator | verilator | 10 | 10 | 1 | no | 78 | PASS |
| rq2_yosys | yosys | 10 | 10 | 1 | no | 132 | PASS |

## Docker And CI Status

| check | status | detail |
|---|---|---|
| local_docker_binary | NOT_RUN_ENVIRONMENT_MISSING | docker command not found on this machine |
| ci_workflow_present | PASS | .github/workflows/ci.yml |
| ci_replay_command_present | PASS | CI includes replay/reproduction command |

Docker availability is reported separately. A missing local Docker binary does not create a false Docker pass.
