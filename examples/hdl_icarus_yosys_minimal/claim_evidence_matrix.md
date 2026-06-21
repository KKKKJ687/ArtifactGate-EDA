# Paper 2 Spec2DFX Claim-Evidence Matrix

Generated: 2026-06-19

| claim_id | paper2_claim | support_level | evidence_layer | evidence_artifacts | inference_needed | safe_paper_wording |
|---|---|---|---|---|---|---|
| S2D-C01 | Spec2DFX includes two RM-like HDL artifacts. | direct evidence | L1_CODE_EXISTS | S2D-A001; S2D-A007 | none | The case contains two RM-like HDL source artifacts. |
| S2D-C02 | Spec2DFX includes local testbench/reference-vector evidence. | direct evidence | L1/L2 | S2D-A002; S2D-A003; S2D-A008; S2D-A009 | finite vectors only | The case includes self-checking testbench and finite reference-vector artifacts. |
| S2D-C03 | Spec2DFX has local HDL simulation evidence. | direct evidence | L3_SIMULATION_EVIDENCE | S2D-A004; S2D-A010; S2D-A023 | local simulator scope | The case records local HDL simulation evidence for the two RM candidates. |
| S2D-C04 | Spec2DFX has standalone Yosys synthesis evidence. | direct evidence | L4_SYNTHESIS_EVIDENCE | S2D-A005; S2D-A006; S2D-A011; S2D-A012; S2D-A015; S2D-A024 | Yosys is not Vivado | The case records standalone open-source Yosys synthesis evidence. |
| S2D-C05 | Spec2DFX records RM interface compatibility evidence. | direct evidence | L2_INTERFACE_EVIDENCE | S2D-A013; S2D-A014; S2D-A025 | static source-level only | The case includes a static source-level interface contract and compatibility report. |
| S2D-C06 | Spec2DFX separates supported and unsupported evidence layers. | direct evidence | BOUNDARY_ARTIFACT | S2D-A016; S2D-A017; S2D-A018; S2D-A021; S2D-A022 | none | The case includes explicit boundary artifacts for unsupported hardware claims. |
| S2D-C07 | Spec2DFX can feed artifact-ingestion workflows. | direct evidence for interface only | L0/L1_SCHEMA | S2D-A019; S2D-A020; DDC nodes/edges | not proof of real artifact ingestion | The case exports schema and DDC-style graph inputs for future artifact ingestion. |

## Paper 2 Wording

Use:

```text
Spec2DFX serves as the HDL/Yosys case for evaluating whether an artifact package can separate HDL implementation, simulation evidence, synthesis evidence, and unsupported DFX/board claims.
```

Do not use:

```text
Spec2DFX includes an unsupported DFX automation claim candidate.
Spec2DFX validates partial reconfiguration on FPGA.
```

