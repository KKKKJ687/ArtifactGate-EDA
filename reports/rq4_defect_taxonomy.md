# RQ4 Extended Defect Taxonomy

| defect_id | category | defect | expected_error_code | severity | critical |
| --- | --- | --- | --- | --- | --- |
| D01 | Structural | missing artifact | MISSING_ARTIFACT | 5 | true |
| D02 | Structural | extra unindexed artifact | UNINDEXED_ARTIFACT | 3 | false |
| D03 | Structural | invalid schema | SCHEMA_INVALID | 5 | true |
| D04 | Structural | broken relative path | BROKEN_PATH | 5 | true |
| D05 | Integrity | hash mismatch | HASH_MISMATCH | 5 | true |
| D06 | Integrity | stale checksum | STALE_CHECKSUM | 4 | true |
| D07 | Integrity | duplicated artifact id | DUPLICATE_ARTIFACT_ID | 5 | true |
| D08 | Provenance | missing tool version | MISSING_TOOL_VERSION | 4 | true |
| D09 | Provenance | tool version drift | TOOL_VERSION_DRIFT | 3 | false |
| D10 | Provenance | missing command | MISSING_COMMAND | 4 | true |
| D11 | Provenance | missing seed | REPLAY_UNSAFE | 3 | false |
| D12 | Replay | incomplete manifest | INCOMPLETE_MANIFEST | 5 | true |
| D13 | Replay | output directory drift | PACKAGE_STRUCTURE_DRIFT | 3 | false |
| D14 | Replay | non-deterministic output | NONDETERMINISTIC_OUTPUT | 4 | true |
| D15 | Replay | missing expected output | MISSING_EXPECTED_OUTPUT | 5 | true |
| D16 | Policy | unsupported hardware claim | UNSUPPORTED_CLAIM | 5 | true |
| D17 | Policy | simulation-to-hardware escalation | EVIDENCE_LEVEL_ESCALATION | 5 | true |
| D18 | Policy | Yosys-to-Vivado escalation | EVIDENCE_LEVEL_ESCALATION | 5 | true |
| D19 | Policy | allowed limitation misclassified | CONTEXT_FALSE_POSITIVE | 4 | true |
| D20 | Evidence | missing evidence level | MISSING_EVIDENCE_LEVEL | 4 | true |
| D21 | Evidence | wrong evidence level | EVIDENCE_LEVEL_MISMATCH | 4 | true |
| D22 | Evidence | broken claim reference | BROKEN_CLAIM_REFERENCE | 5 | true |
| D23 | Evidence | claim without artifact | UNBOUND_CLAIM | 5 | true |
| D24 | Portability | absolute user path | NON_PORTABLE_PATH | 5 | true |
| D25 | Portability | OS-specific separator | NON_PORTABLE_PATH | 3 | false |
| D26 | Portability | symlink to external path | NON_PORTABLE_PATH | 5 | true |
| D27 | Package | missing README | PACKAGE_MISSING_README | 3 | false |
| D28 | Package | missing license | PACKAGE_MISSING_LICENSE | 4 | true |
| D29 | Package | missing citation metadata | PACKAGE_MISSING_CITATION | 3 | false |
| D30 | Package | release contains cache/venv/git | RELEASE_CONTAMINATION | 5 | true |
