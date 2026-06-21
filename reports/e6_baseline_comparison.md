# Baseline Comparison

ArtifactGate-EDA complements generic reproducibility tools by adding EDA-specific evidence-level and unsupported-claim checks.

| method | hash_check | evidence_level_check | claim_check | replay_manifest | unsupported_ledger | softwarex_report | manual_steps |
|---|---|---|---|---|---|---|---|
| manual_zip | no | no | no | no | no | no | high |
| shell_script | partial | no | no | partial | no | no | medium |
| checksum_manifest | yes | no | no | no | no | no | medium |
| artifactgate | yes | yes | yes | yes | yes | yes | low |
