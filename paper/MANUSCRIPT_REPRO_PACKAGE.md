# Manuscript Reproducibility Package

## Rebuild Commands

```bash
make install
make reproduce-all
make package-release
```

## Artifact Map

| file | role | sha256 | rebuild_command |
|---|---|---|---|
| paper/softwarex_manuscript.md | manuscript_source | `6bca6218bccafc26ea0694f24c6957f7f35a56165205683f0465b1b72a469a68` | `manual edit, then make manuscript-package` |
| paper/softwarex_manuscript.tex | manuscript_source | `101054ea29a93993a903003cbff728ca3e7f958cc9c795d31223ad2599ced297` | `manual edit, then make manuscript-package` |
| paper/figures/architecture.png | generated_figure | `6b508a854d3b895cdd8d82fdcce2ca2e7e93a94a5a4e5553ad781dd909673aec` | `make figures` |
| paper/figures/evidence_levels.png | generated_figure | `9551b12cf1bd545c8cdd115143595b79935b0d965088162fe41a512f0913c640` | `make figures` |
| paper/figures/experiment_matrix.png | generated_figure | `ce2b3debb0c72b965322f74c03baef1866abcff3157bccc5a63627061dc04a5a` | `make figures` |
| paper/figures/workflow.png | generated_figure | `f48012d93ef2dc6e6f167a90c0607d15c9187f30e8732dde7809deca31263315` | `make figures` |
| reports/e1_multi_adapter_summary.csv | generated_report | `ac2d2a591c55f6b3d331c48928d51d97308a20cb467bfaa748b1ccb8730ebdc6` | `make reproduce-all` |
| reports/e2_replay_summary.csv | generated_report | `5091c125f0c92bbb9aa7d871e3aa1ce9713f668caa4dcfa699e13b81ebc4d59c` | `make reproduce-all` |
| reports/e3_negative_claim_detection_summary.csv | generated_report | `42f8c9c64aa8d7850e5fdd5367bec1042881879b76dd39addd0e07486b2f271e` | `make reproduce-all` |
| reports/e5_scalability_memory.csv | generated_report | `426e4c2b6d2dfb1e45b24ec189147510f43baadd59bb5e3cb12a045db0b64214` | `make reproduce-all` |
| reports/e5_scalability_runtime.csv | generated_report | `08ea5855d59ff2d579c604d863bf9b40bf689a3fe40b48c04688dcec820e2a92` | `make reproduce-all` |
| reports/e6_baseline_comparison.csv | generated_report | `0cd5b35717cd31e414fff169e43e1760ce3bbd865044fbe09b0c4c572977d098` | `make reproduce-all` |
| reports/e2_replay_acceptance_report.md | generated_report | `5fa8c2906de12c5af35efa79711cbf39551d21cef58d380cc0c02a31f6de46a9` | `make reproduce-all` |
| reports/e5_scalability_summary.md | generated_report | `9e2520f2a46e88bba9b404badb20871df305f83da8979bb0c4b9f0ce9cc46f3b` | `make reproduce-all` |
| reports/e6_baseline_comparison.md | generated_report | `393229f6a516b2a88f549c4b4a3cd7e0de523da660769cb10f76db6d2249e9c3` | `make reproduce-all` |

## Claim-Evidence Boundary

The manuscript package is limited to software-only artifact evidence. Reports under `reports/` are generated from local CLI/Makefile commands and do not provide hardware, vendor implementation, bitstream, or board-measurement evidence.
