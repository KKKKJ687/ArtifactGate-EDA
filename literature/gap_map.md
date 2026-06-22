# Related Work Gap Map

Mapped sources: 57

ArtifactGate-EDA should be positioned as complementary to existing packaging, artifact evaluation, provenance, and EDA workflow systems. The recurring gap is G5-G8 from the stronger plan: EDA-specific evidence levels, claim-evidence binding, unsupported hardware-overclaim blocking, and reviewer-ready ledgers.

## artifact_evaluation_badging

| ID | Tool / Method | Gap For ArtifactGate |
|---|---|---|
| S02 | ACM artifact badges | Defines artifact quality and badges but does not automate EDA evidence levels. |
| S03 | SIGSOFT AE | Requires claim support descriptions but leaves binding manual. |
| S47 | Artifact evaluation tutorial | AE practice guidance; does not automate EDA evidence-level checking. |
| S48 | EuroSys AE study | Highlights claim-to-artifact connection needs but remains process-level. |
| S49 | AE expectations study | Survey evidence for AE expectations, not EDA-specific policy automation. |
| S51 | Artifact sharing study | Discusses artifact support for claims but not EDA evidence-level sufficiency. |
| S53 | SE artifact evaluation position | Argues AE should focus on substance and evidence; not an EDA-specific tool. |

## computational_reproducibility_packaging

| ID | Tool / Method | Gap For ArtifactGate |
|---|---|---|
| S04 | ReproZip | Packages and replays experiments but does not model EDA claim sufficiency. |
| S05 | ReproZip | Captures command dependencies rather than paper claim boundaries. |
| S06 | RO-Crate | Metadata packaging does not provide EDA evidence-level policy. |
| S07 | RO-Crate | Research-object aggregation without hardware-overclaim blocking. |
| S08 | Code Ocean | Compute capsule verification is domain-general and not EDA claim aware. |
| S09 | DVC | Data and pipeline versioning does not classify EDA evidence levels. |
| S10 | Whole Tale | Research-object environment packaging without EDA claim policing. |
| S11 | Whole Tale | Environment packaging complements but does not replace claim-evidence checking. |
| S12 | Binder | Launches executable environments; no EDA artifact evidence lattice. |
| S13 | repo2docker | Builds environments from repositories without claim-boundary analysis. |
| S52 | Docker artifact method | Reproducible artifact preparation method, not claim-evidence policing. |

## eda_fpga_artifact_practice

| ID | Tool / Method | Gap For ArtifactGate |
|---|---|---|
| S14 | MLCAD AE | Provides EDA-community AE practice but not automated evidence sufficiency. |
| S15 | FPGA AE | Community AE process is manual and can include hardware artifacts outside this scope. |
| S50 | FPGA/TRETS AE | Direct FPGA AE context; still process/manual rather than automated claim blocking. |
| S57 | AutoBench | EDA artifact with public artifact DOI and code, but it evaluates testbench generation rather than claim-evidence sufficiency. |

## eda_workflow_build_tools

| ID | Tool / Method | Gap For ArtifactGate |
|---|---|---|
| S16 | FuseSoC | HDL package/build manager; ArtifactGate is complementary claim-safety layer. |
| S17 | Edalize | Tool abstraction does not judge paper claim sufficiency. |
| S18 | Edalize | Interface library; not a reviewer-ready claim ledger. |
| S19 | OpenROAD Flow Scripts | EDA flow execution is outside ArtifactGate's claim-safety purpose. |
| S20 | OpenROAD Flow Scripts | Flow automation rather than manuscript evidence boundary checking. |
| S21 | OpenLane | Physical implementation flow; ArtifactGate must not claim to replace it. |
| S22 | mflowgen | Modular flow generator, not claim-overreach detector. |
| S23 | mflowgen | Reusable flow concern differs from software-only claim sufficiency. |
| S24 | SiliconCompiler | Build-system manifests do not block unsupported manuscript claims. |
| S25 | SiliconCompiler | Flow automation and results tracking are complementary. |
| S26 | Hammer | VLSI flow backend, not software-only artifact claim checker. |
| S27 | Hammer | Targets physical design tasks beyond ArtifactGate's evidence ceiling. |
| S28 | CIRCT | Compiler infrastructure does not address artifact-package claim boundaries. |
| S29 | CIRCT | Reusable compiler infrastructure, not artifact review ledger. |
| S30 | ngspice | Core backend source; not an artifact packaging framework. |
| S31 | Yosys | Open-source synthesis evidence provider; not a claim-safety layer. |
| S32 | Yosys | Provides L4 evidence type but no manuscript claim policy. |
| S33 | Icarus Verilog | Simulation backend source; no claim-evidence matrix. |
| S34 | Verilator | Backend source; no hardware-overclaim blocking. |
| S44 | PLECS | Optional metadata/backend source only; not core reproducibility dependency. |
| S45 | Logisim-evolution | Optional educational metadata case, not claim-sufficiency framework. |
| S46 | LTspice | Optional local metadata/backend source; not open-source core dependency. |

## empirical_se_methodology

| ID | Tool / Method | Gap For ArtifactGate |
|---|---|---|
| S01 | IST venue scope | Venue fit only; not an artifact tool. |
| S39 | GQM | Measurement framing supports evaluation design but not artifact tooling. |
| S40 | Software engineering experimentation | Study-design guidance supports statistics and threats to validity. |
| S41 | Case study guidelines | Reporting guidance, not a claim-safety tool. |
| S42 | Kitchenham and Charters SLR | Methodological basis for mapping; no EDA artifact checking. |
| S43 | Systematic mapping | Supports gap-map method but not ArtifactGate functionality. |
| S54 | Empirical SE methods | Method selection guidance supports study design and threat framing. |
| S55 | Empirical SE guidelines | Guidelines for empirical research quality; not an artifact tool. |
| S56 | Controlled experiment survey | Supports controlled-experiment validity discussion. |

## provenance_policy_traceability

| ID | Tool / Method | Gap For ArtifactGate |
|---|---|---|
| S35 | SLSA provenance | Supply-chain provenance differs from scientific claim sufficiency. |
| S36 | in-toto | Attestation framework does not model EDA evidence levels. |
| S37 | in-toto/SLSA attestation | Attestation context complements but does not replace claim audits. |
| S38 | PROV-O | General provenance model lacks EDA-specific claim-boundary semantics. |
