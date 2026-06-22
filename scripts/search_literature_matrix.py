#!/usr/bin/env python3
"""Generate the IST literature mapping seed matrix and gap map."""

from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from pathlib import Path

FIELDS = [
    "id",
    "title",
    "year",
    "venue",
    "type",
    "category",
    "tool_or_method",
    "solves_packaging",
    "solves_replay",
    "solves_provenance",
    "solves_eda_flow",
    "solves_claim_evidence",
    "solves_hardware_overclaim",
    "domain",
    "overlap_risk",
    "gap_for_artifactgate",
    "url",
]


def source(
    source_id: str,
    title: str,
    year: str,
    venue: str,
    source_type: str,
    category: str,
    tool_or_method: str,
    solves_packaging: str,
    solves_replay: str,
    solves_provenance: str,
    solves_eda_flow: str,
    solves_claim_evidence: str,
    solves_hardware_overclaim: str,
    domain: str,
    overlap_risk: str,
    gap_for_artifactgate: str,
    url: str,
) -> dict[str, str]:
    return {
        "id": source_id,
        "title": title,
        "year": year,
        "venue": venue,
        "type": source_type,
        "category": category,
        "tool_or_method": tool_or_method,
        "solves_packaging": solves_packaging,
        "solves_replay": solves_replay,
        "solves_provenance": solves_provenance,
        "solves_eda_flow": solves_eda_flow,
        "solves_claim_evidence": solves_claim_evidence,
        "solves_hardware_overclaim": solves_hardware_overclaim,
        "domain": domain,
        "overlap_risk": overlap_risk,
        "gap_for_artifactgate": gap_for_artifactgate,
        "url": url,
    }


SOURCES = [
    source("S01", "Information and Software Technology aims and scope", "2026", "Elsevier", "journal_scope", "empirical_se_methodology", "IST venue scope", "no", "no", "no", "no", "no", "no", "software engineering", "low", "Venue fit only; not an artifact tool.", "https://shop.elsevier.com/journals/subjects/physical-sciences-and-engineering/computer-science/software/software-general"),
    source("S02", "ACM Artifact Review and Badging policy", "2020", "ACM", "policy", "artifact_evaluation_badging", "ACM artifact badges", "partial", "partial", "partial", "no", "manual", "no", "research artifacts", "medium", "Defines artifact quality and badges but does not automate EDA evidence levels.", "https://www.acm.org/publications/policies/artifact-review-and-badging-current"),
    source("S03", "ACM SIGSOFT Artifact Evaluation guidance", "2026", "ACM SIGSOFT", "guidance", "artifact_evaluation_badging", "SIGSOFT AE", "partial", "partial", "no", "no", "manual", "no", "software engineering artifacts", "medium", "Requires claim support descriptions but leaves binding manual.", "https://github.com/acmsigsoft/artifact-evaluation"),
    source("S04", "ReproZip: Computational reproducibility with captured dependencies", "2016", "SIGMOD", "paper", "computational_reproducibility_packaging", "ReproZip", "yes", "yes", "yes", "no", "no", "no", "computational experiments", "medium", "Packages and replays experiments but does not model EDA claim sufficiency.", "https://dl.acm.org/doi/10.1145/2882903.2899401"),
    source("S05", "ReproZip project documentation", "2026", "ReproZip", "official_docs", "computational_reproducibility_packaging", "ReproZip", "yes", "yes", "yes", "no", "no", "no", "computational experiments", "medium", "Captures command dependencies rather than paper claim boundaries.", "https://www.reprozip.org/about.html"),
    source("S06", "RO-Crate Metadata Specification 1.1", "2023", "Research Object", "specification", "computational_reproducibility_packaging", "RO-Crate", "yes", "partial", "metadata", "no", "no", "no", "research objects", "medium", "Metadata packaging does not provide EDA evidence-level policy.", "https://www.researchobject.org/ro-crate/specification/1.1/"),
    source("S07", "RO-Crate Metadata Specification 1.2.0", "2024", "Zenodo", "specification", "computational_reproducibility_packaging", "RO-Crate", "yes", "partial", "metadata", "no", "no", "no", "research objects", "medium", "Research-object aggregation without hardware-overclaim blocking.", "https://zenodo.org/records/13751027"),
    source("S08", "Code Ocean verification process for reproducibility and quality", "2026", "Code Ocean", "official_docs", "computational_reproducibility_packaging", "Code Ocean", "yes", "yes", "yes", "no", "no", "no", "compute capsules", "medium", "Compute capsule verification is domain-general and not EDA claim aware.", "https://docs.codeocean.com/osl-guide/publishing-on-code-ocean/the-verification-process/code-oceans-verification-process-for-computational-reproducibility-and-quality"),
    source("S09", "DVC documentation and user guide", "2026", "DVC", "official_docs", "computational_reproducibility_packaging", "DVC", "data_ml", "pipeline", "partial", "no", "no", "no", "data science and ML", "low", "Data and pipeline versioning does not classify EDA evidence levels.", "https://dvc.org/doc/user-guide"),
    source("S10", "Whole Tale reproducible research platform", "2026", "Whole Tale", "platform_docs", "computational_reproducibility_packaging", "Whole Tale", "yes", "yes", "yes", "no", "no", "no", "computational research", "medium", "Research-object environment packaging without EDA claim policing.", "https://wholetale.org/"),
    source("S11", "Implementing computational reproducibility in the Whole Tale environment", "2017", "Science Gateways", "paper", "computational_reproducibility_packaging", "Whole Tale", "yes", "yes", "yes", "no", "no", "no", "computational research", "medium", "Environment packaging complements but does not replace claim-evidence checking.", "https://www.stodden.net/papers/p17-chard.pdf"),
    source("S12", "Binder project documentation", "2026", "Binder", "official_docs", "computational_reproducibility_packaging", "Binder", "partial", "yes", "partial", "no", "no", "no", "notebook environments", "low", "Launches executable environments; no EDA artifact evidence lattice.", "https://mybinder.readthedocs.io/"),
    source("S13", "repo2docker documentation", "2026", "Jupyter", "official_docs", "computational_reproducibility_packaging", "repo2docker", "partial", "yes", "partial", "no", "no", "no", "computational environments", "low", "Builds environments from repositories without claim-boundary analysis.", "https://repo2docker.readthedocs.io/"),
    source("S14", "MLCAD artifact evaluation", "2026", "MLCAD", "artifact_evaluation", "eda_fpga_artifact_practice", "MLCAD AE", "partial", "partial", "no", "domain-general", "manual", "no", "ML for EDA", "medium", "Provides EDA-community AE practice but not automated evidence sufficiency.", "https://mlcad.org/symposium/2026/call-for-artifact-evaluation/"),
    source("S15", "FPGA artifact evaluation", "2026", "ISFPGA", "artifact_evaluation", "eda_fpga_artifact_practice", "FPGA AE", "partial", "partial", "no", "yes", "manual", "no", "FPGA research artifacts", "medium", "Community AE process is manual and can include hardware artifacts outside this scope.", "https://www.isfpga.org/artifact-evaluation/"),
    source("S16", "FuseSoC user overview", "2026", "FuseSoC", "official_docs", "eda_workflow_build_tools", "FuseSoC", "package", "tool_run", "partial", "yes", "no", "no", "HDL build", "high", "HDL package/build manager; ArtifactGate is complementary claim-safety layer.", "https://fusesoc.readthedocs.io/en/stable/user/overview.html"),
    source("S17", "Edalize documentation", "2026", "Edalize", "official_docs", "eda_workflow_build_tools", "Edalize", "no", "tool_run", "partial", "yes", "no", "no", "EDA tool interfacing", "high", "Tool abstraction does not judge paper claim sufficiency.", "https://edalize.readthedocs.io/"),
    source("S18", "Edalize repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "Edalize", "no", "tool_run", "partial", "yes", "no", "no", "EDA tool interfacing", "high", "Interface library; not a reviewer-ready claim ledger.", "https://github.com/olofk/edalize"),
    source("S19", "OpenROAD Flow Scripts tutorial", "2026", "OpenROAD", "official_docs", "eda_workflow_build_tools", "OpenROAD Flow Scripts", "partial", "yes", "logs", "yes", "no", "no", "RTL-to-GDS flow", "high", "EDA flow execution is outside ArtifactGate's claim-safety purpose.", "https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/FlowTutorial.html"),
    source("S20", "OpenROAD Flow Scripts repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "OpenROAD Flow Scripts", "partial", "yes", "logs", "yes", "no", "no", "RTL-to-GDS flow", "high", "Flow automation rather than manuscript evidence boundary checking.", "https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts"),
    source("S21", "OpenLane repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "OpenLane", "partial", "yes", "logs", "yes", "no", "no", "RTL-to-GDS flow", "high", "Physical implementation flow; ArtifactGate must not claim to replace it.", "https://github.com/The-OpenROAD-Project/openlane"),
    source("S22", "mflowgen documentation", "2026", "mflowgen", "official_docs", "eda_workflow_build_tools", "mflowgen", "partial", "tool_run", "partial", "yes", "no", "no", "ASIC/FPGA flow generation", "high", "Modular flow generator, not claim-overreach detector.", "https://mflowgen.readthedocs.io/"),
    source("S23", "Enabling reusable physical design flows with modular flow generators", "2021", "arXiv", "paper", "eda_workflow_build_tools", "mflowgen", "partial", "tool_run", "partial", "yes", "no", "no", "physical design flows", "high", "Reusable flow concern differs from software-only claim sufficiency.", "https://arxiv.org/abs/2111.14535"),
    source("S24", "SiliconCompiler documentation", "2026", "SiliconCompiler", "official_docs", "eda_workflow_build_tools", "SiliconCompiler", "partial", "tool_run", "manifest", "yes", "no", "no", "silicon compilation", "high", "Build-system manifests do not block unsupported manuscript claims.", "https://docs.siliconcompiler.com/"),
    source("S25", "SiliconCompiler repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "SiliconCompiler", "partial", "tool_run", "manifest", "yes", "no", "no", "silicon compilation", "high", "Flow automation and results tracking are complementary.", "https://github.com/siliconcompiler/siliconcompiler"),
    source("S26", "Hammer VLSI flow overview", "2026", "Hammer", "official_docs", "eda_workflow_build_tools", "Hammer", "no", "tool_run", "partial", "yes", "no", "no", "VLSI flow APIs", "high", "VLSI flow backend, not software-only artifact claim checker.", "https://docs.hammer-eda.org/en/latest/Hammer-Basics/Hammer-Overview.html"),
    source("S27", "Hammer project website", "2026", "Hammer", "project_site", "eda_workflow_build_tools", "Hammer", "no", "tool_run", "partial", "yes", "no", "no", "VLSI flow APIs", "high", "Targets physical design tasks beyond ArtifactGate's evidence ceiling.", "https://www.hammer-eda.org/"),
    source("S28", "CIRCT project", "2026", "LLVM", "project_site", "eda_workflow_build_tools", "CIRCT", "no", "tool_run", "partial", "yes", "no", "no", "hardware compiler infrastructure", "medium", "Compiler infrastructure does not address artifact-package claim boundaries.", "https://circt.llvm.org/"),
    source("S29", "CIRCT repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "CIRCT", "no", "tool_run", "partial", "yes", "no", "no", "hardware compiler infrastructure", "medium", "Reusable compiler infrastructure, not artifact review ledger.", "https://github.com/llvm/circt"),
    source("S30", "ngspice official site", "2026", "ngspice", "tool_docs", "eda_workflow_build_tools", "ngspice", "no", "yes", "logs", "yes", "no", "no", "SPICE simulation", "low", "Core backend source; not an artifact packaging framework.", "https://ngspice.sourceforge.io/"),
    source("S31", "Yosys official site", "2026", "YosysHQ", "tool_docs", "eda_workflow_build_tools", "Yosys", "no", "tool_run", "logs", "yes", "no", "no", "RTL synthesis", "low", "Open-source synthesis evidence provider; not a claim-safety layer.", "https://yosyshq.net/yosys/"),
    source("S32", "Yosys repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "Yosys", "no", "tool_run", "logs", "yes", "no", "no", "RTL synthesis", "low", "Provides L4 evidence type but no manuscript claim policy.", "https://github.com/YosysHQ/yosys"),
    source("S33", "Icarus Verilog repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "Icarus Verilog", "no", "tool_run", "logs", "yes", "no", "no", "Verilog simulation", "low", "Simulation backend source; no claim-evidence matrix.", "https://github.com/steveicarus/iverilog"),
    source("S34", "Verilator repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "Verilator", "no", "tool_run", "logs", "yes", "no", "no", "SystemVerilog simulation and lint", "low", "Backend source; no hardware-overclaim blocking.", "https://github.com/verilator/verilator"),
    source("S35", "SLSA provenance specification", "2026", "SLSA", "specification", "provenance_policy_traceability", "SLSA provenance", "no", "no", "yes", "no", "no", "no", "software supply chain", "medium", "Supply-chain provenance differs from scientific claim sufficiency.", "https://slsa.dev/provenance"),
    source("S36", "in-toto project", "2026", "in-toto", "project_site", "provenance_policy_traceability", "in-toto", "no", "no", "yes", "no", "no", "no", "software supply chain", "medium", "Attestation framework does not model EDA evidence levels.", "https://in-toto.io/"),
    source("S37", "in-toto and SLSA", "2023", "SLSA", "technical_article", "provenance_policy_traceability", "in-toto/SLSA attestation", "no", "no", "yes", "no", "no", "no", "software supply chain", "medium", "Attestation context complements but does not replace claim audits.", "https://slsa.dev/blog/2023/05/in-toto-and-slsa"),
    source("S38", "W3C PROV-O ontology", "2013", "W3C", "standard", "provenance_policy_traceability", "PROV-O", "no", "no", "yes", "no", "no", "no", "provenance", "medium", "General provenance model lacks EDA-specific claim-boundary semantics.", "https://www.w3.org/TR/prov-o/"),
    source("S39", "Goal Question Metric approach", "1989", "University of Maryland", "technical_report", "empirical_se_methodology", "GQM", "no", "no", "no", "no", "manual", "no", "software engineering measurement", "low", "Measurement framing supports evaluation design but not artifact tooling.", "https://www.cs.umd.edu/~basili/publications/technical/T89.pdf"),
    source("S40", "Experimentation in Software Engineering", "2024", "Springer", "book", "empirical_se_methodology", "Software engineering experimentation", "no", "no", "no", "no", "manual", "no", "empirical software engineering", "low", "Study-design guidance supports statistics and threats to validity.", "https://portal.research.lu.se/en/publications/experimentation-in-software-engineering-2024-edition/"),
    source("S41", "Guidelines for conducting and reporting case study research in software engineering", "2009", "Empirical Software Engineering", "paper", "empirical_se_methodology", "Case study guidelines", "no", "no", "no", "no", "manual", "no", "empirical software engineering", "low", "Reporting guidance, not a claim-safety tool.", "https://doi.org/10.1007/s10664-008-9102-8"),
    source("S42", "Guidelines for performing systematic literature reviews in software engineering", "2007", "Keele University", "technical_report", "empirical_se_methodology", "Kitchenham and Charters SLR", "no", "no", "no", "no", "manual", "no", "software engineering reviews", "low", "Methodological basis for mapping; no EDA artifact checking.", "https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf"),
    source("S43", "Systematic mapping studies in software engineering", "2008", "EASE", "paper", "empirical_se_methodology", "Systematic mapping", "no", "no", "no", "no", "manual", "no", "software engineering reviews", "low", "Supports gap-map method but not ArtifactGate functionality.", "https://doi.org/10.14236/ewic/EASE2008.8"),
    source("S44", "PLECS product page", "2026", "Plexim", "tool_docs", "eda_workflow_build_tools", "PLECS", "no", "tool_run", "logs", "yes", "no", "no", "power electronics simulation", "low", "Optional metadata/backend source only; not core reproducibility dependency.", "https://www.plexim.com/products/plecs"),
    source("S45", "Logisim-evolution repository", "2026", "GitHub", "repository", "eda_workflow_build_tools", "Logisim-evolution", "no", "tool_run", "partial", "yes", "no", "no", "digital logic simulation", "low", "Optional educational metadata case, not claim-sufficiency framework.", "https://github.com/logisim-evolution/logisim-evolution"),
    source("S46", "LTspice official page", "2026", "Analog Devices", "tool_docs", "eda_workflow_build_tools", "LTspice", "no", "tool_run", "logs", "yes", "no", "no", "SPICE simulation", "low", "Optional local metadata/backend source; not open-source core dependency.", "https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html"),
]

EXTRA_SOURCES = [
    source("S47", "Artifact Evaluations for Stronger Research Results", "2025", "ACM", "paper", "artifact_evaluation_badging", "Artifact evaluation tutorial", "partial", "partial", "no", "domain-general", "manual", "no", "computer science artifacts", "medium", "AE practice guidance; does not automate EDA evidence-level checking.", "https://dl.acm.org/doi/10.1145/3696630.3728623"),
    source("S48", "Lessons Learned from Five Years of Artifact Evaluations at EuroSys", "2025", "ACM", "paper", "artifact_evaluation_badging", "EuroSys AE study", "partial", "partial", "no", "domain-general", "manual", "no", "systems artifacts", "medium", "Highlights claim-to-artifact connection needs but remains process-level.", "https://dl.acm.org/doi/10.1145/3736731.3746152"),
    source("S49", "Community expectations for research artifacts and evaluation processes", "2020", "ACM", "paper", "artifact_evaluation_badging", "AE expectations study", "partial", "partial", "no", "domain-general", "manual", "no", "software artifacts", "medium", "Survey evidence for AE expectations, not EDA-specific policy automation.", "https://dl.acm.org/doi/10.1145/3368089.3409767"),
    source("S50", "Artifact Evaluation in the FPGA Community and in ACM TRETS", "2026", "ACM TRETS", "paper", "eda_fpga_artifact_practice", "FPGA/TRETS AE", "partial", "partial", "no", "yes", "manual", "no", "FPGA artifacts", "medium", "Direct FPGA AE context; still process/manual rather than automated claim blocking.", "https://dl.acm.org/doi/10.1145/3802561"),
    source("S51", "Understanding and improving artifact sharing in software engineering research", "2021", "Empirical Software Engineering", "paper", "artifact_evaluation_badging", "Artifact sharing study", "partial", "partial", "no", "no", "manual", "no", "software engineering artifacts", "medium", "Discusses artifact support for claims but not EDA evidence-level sufficiency.", "https://doi.org/10.1007/s10664-021-09973-5"),
    source("S52", "Preparing Reproducible Scientific Artifacts using Docker", "2023", "arXiv", "paper", "computational_reproducibility_packaging", "Docker artifact method", "yes", "yes", "partial", "no", "no", "no", "empirical computer science", "medium", "Reproducible artifact preparation method, not claim-evidence policing.", "https://arxiv.org/abs/2308.14122"),
    source("S53", "Rethinking Artifact Evaluation for Software Engineering in the Age of Generative AI", "2026", "arXiv", "paper", "artifact_evaluation_badging", "SE artifact evaluation position", "partial", "partial", "no", "no", "manual", "no", "software engineering artifacts", "medium", "Argues AE should focus on substance and evidence; not an EDA-specific tool.", "https://arxiv.org/abs/2604.16306"),
    source("S54", "Empirical Research Methods in Software Engineering", "2003", "Springer", "book_chapter", "empirical_se_methodology", "Empirical SE methods", "no", "no", "no", "no", "manual", "no", "empirical software engineering", "low", "Method selection guidance supports study design and threat framing.", "https://link.springer.com/chapter/10.1007/978-3-540-45143-3_2"),
    source("S55", "Preliminary guidelines for empirical research in software engineering", "2002", "IEEE Transactions on Software Engineering", "paper", "empirical_se_methodology", "Empirical SE guidelines", "no", "no", "no", "no", "manual", "no", "empirical software engineering", "low", "Guidelines for empirical research quality; not an artifact tool.", "https://ieeexplore.ieee.org/document/1027796"),
    source("S56", "Sjoberg et al. survey of controlled experiments in software engineering", "2005", "IEEE Transactions on Software Engineering", "paper", "empirical_se_methodology", "Controlled experiment survey", "no", "no", "no", "no", "manual", "no", "empirical software engineering", "low", "Supports controlled-experiment validity discussion.", "https://doi.org/10.1109/TSE.2005.97"),
    source("S57", "AutoBench: Automatic Testbench Generation and Evaluation Using LLMs for HDL Design", "2024", "ACM/IEEE MLCAD", "paper", "eda_fpga_artifact_practice", "AutoBench", "partial", "yes", "artifact_doi", "yes", "manual", "no", "HDL simulation/testbench artifacts", "medium", "EDA artifact with public artifact DOI and code, but it evaluates testbench generation rather than claim-evidence sufficiency.", "https://ieeexplore.ieee.org/document/10740250/"),
]

ALL_SOURCES = SOURCES + EXTRA_SOURCES

SEARCH_LOG_ROWS = [
    {
        "database": "ACM Digital Library",
        "query": "artifact evaluation reproducibility software engineering badging claims artifact support",
        "search_interface": "web search scoped to dl.acm.org plus ACM DOI pages",
        "date": "2026-06-22",
        "returned_count": ">=8",
        "screened_count": "8",
        "included_count": "5",
        "included_ids": "S02;S03;S47;S48;S49",
        "notes": "Included artifact policy/guidance and recent AE studies with public DOI metadata.",
    },
    {
        "database": "IEEE Xplore",
        "query": "EDA artifact evaluation reproducibility MLCAD; AutoBench Artifact DOI; empirical software engineering guidelines",
        "search_interface": "web search scoped to ieeexplore.ieee.org",
        "date": "2026-06-22",
        "returned_count": ">=4",
        "screened_count": "4",
        "included_count": "2",
        "included_ids": "S55;S57",
        "notes": "Included empirical-SE guideline plus ACM/IEEE MLCAD AutoBench, whose IEEE metadata and open preprint record an artifact DOI.",
    },
    {
        "database": "ScienceDirect",
        "query": "Information and Software Technology empirical software engineering artifact reproducibility",
        "search_interface": "web search / public pages",
        "date": "2026-06-22",
        "returned_count": "blocked",
        "screened_count": "0",
        "included_count": "1",
        "included_ids": "S01",
        "notes": "Direct ScienceDirect search was blocked by robots; IST public scope page retained as venue evidence.",
    },
    {
        "database": "SpringerLink",
        "query": "empirical software engineering experimentation case study systematic review",
        "search_interface": "web search scoped to link.springer.com",
        "date": "2026-06-22",
        "returned_count": ">=8",
        "screened_count": "8",
        "included_count": "3",
        "included_ids": "S40;S41;S54",
        "notes": "Included empirical-method and experimentation sources.",
    },
    {
        "database": "arXiv",
        "query": "artifact evaluation reproducibility software engineering; EDA reproducibility artifact",
        "search_interface": "arXiv MCP search",
        "date": "2026-06-22",
        "returned_count": "10",
        "screened_count": "10",
        "included_count": "3",
        "included_ids": "S23;S52;S53",
        "notes": "Included mflowgen, reproducible Docker artifacts, and current SE artifact-evaluation position paper.",
    },
    {
        "database": "Google Scholar / citation network",
        "query": "Artifact evaluation reproducibility EDA claim evidence; seed-paper citation expansion",
        "search_interface": "Google Scholar public web unavailable; OpenAlex public API and publisher metadata used as reproducible substitute",
        "date": "2026-06-22",
        "returned_count": "Google Scholar not_available; OpenAlex >=38 for AutoBench title query",
        "screened_count": "8",
        "included_count": "4",
        "included_ids": "S50;S51;S53;S57",
        "notes": "Direct Google Scholar querying was not machine-accessible; citation-network follow-up was closed with OpenAlex/DOI/public metadata, so the output remains a lightweight mapping rather than a PRISMA-complete review.",
    },
    {
        "database": "GitHub / official docs",
        "query": "ReproZip RO-Crate DVC FuseSoC Edalize OpenROAD OpenLane mflowgen SiliconCompiler Hammer CIRCT SLSA in-toto official docs",
        "search_interface": "official documentation and repository pages",
        "date": "2026-06-22",
        "returned_count": ">=30",
        "screened_count": "30",
        "included_count": "30",
        "included_ids": "S05;S06;S07;S08;S09;S10;S12;S13;S16;S17;S18;S19;S20;S21;S22;S24;S25;S26;S27;S28;S29;S30;S31;S32;S33;S34;S35;S36;S37;S38",
        "notes": "Official docs/repositories used for tool capability and overlap boundaries.",
    },
]


def write_matrix(out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ALL_SOURCES)


def write_protocol(path: Path) -> None:
    now = datetime.now(UTC).date().isoformat()
    categories = sorted({row["category"] for row in ALL_SOURCES})
    lines = [
        "# Literature Search Protocol",
        "",
        f"Generated: {now}",
        "",
        "This file records the reproducible protocol for the IST literature map. "
        "The matrix combines primary official documentation, standards, named papers "
        "identified in the stronger optimization plan, web-verified primary sources, logged "
        "database/search passes, and machine-verifiable citation-network follow-up. Google Scholar "
        "and some ScienceDirect content remain limited by machine-access constraints; citation "
        "expansion is therefore verified through OpenAlex/DOI/public metadata and the output remains "
        "a systematic mapping support artifact rather than a PRISMA-complete systematic review.",
        "",
        "## Databases And Sources",
        "",
        "| Source | Current status |",
        "|---|---|",
        "| ACM Digital Library | seed papers and policies mapped where public metadata/DOI is available |",
        "| IEEE Xplore | empirical-SE guideline plus ACM/IEEE MLCAD EDA artifact row mapped |",
        "| ScienceDirect | IST scope and software-engineering context mapped from public pages |",
        "| SpringerLink | empirical SE methodology mapped through public book/DOI metadata |",
        "| arXiv | mflowgen and related open EDA flow paper mapped |",
        "| Google Scholar / citation network | direct Scholar unavailable; OpenAlex/DOI/public metadata used for reproducible citation expansion |",
        "| GitHub / official docs | official tool and policy pages mapped directly |",
        "",
        "## Search Strings",
        "",
        "- computational reproducibility package capsule environment provenance",
        "- artifact evaluation badging reproducibility software engineering",
        "- EDA workflow manager reproducibility FuseSoC Edalize OpenROAD OpenLane Hammer mflowgen SiliconCompiler",
        "- software provenance attestation SLSA in-toto policy as code artifact integrity",
        "- Goal Question Metric empirical software engineering experimentation case study systematic mapping",
        "- FPGA EDA artifact evaluation reproducibility MLCAD",
        "",
        "## Inclusion Criteria",
        "",
        "- I1: computational reproducibility or artifact packaging",
        "- I2: artifact evaluation, artifact review, or badging",
        "- I3: EDA workflow, build, simulation, synthesis, or tool interfacing",
        "- I4: provenance, attestation, policy, or traceability",
        "- I5: empirical software engineering research design",
        "- I6: EDA/FPGA/MLCAD artifact evaluation practice",
        "",
        "## Exclusion Criteria",
        "",
        "- E1: hardware implementation only, without software artifact relevance",
        "- E2: EDA algorithm performance only, without artifact or reproducibility concern",
        "- E3: generic writing advice without SE/AE/reproducibility relevance",
        "- E4: no accessible abstract, method, specification, or official documentation",
        "- E5: unrelated to software-only EDA artifacts",
        "",
        "## Mapped Categories",
        "",
    ]
    lines.extend(f"- {category}" for category in categories)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_exclusion_log(path: Path) -> None:
    rows = [
        {
            "id": "X01",
            "candidate": "hardware-only FPGA implementation papers without artifact review scope",
            "reason": "E1",
            "decision": "exclude until software artifact relevance is shown",
        },
        {
            "id": "X02",
            "candidate": "EDA algorithm performance papers without packaging/replay/provenance focus",
            "reason": "E2",
            "decision": "exclude from claim-safety related work table",
        },
        {
            "id": "X03",
            "candidate": "generic academic writing or reproducibility opinion posts",
            "reason": "E3",
            "decision": "exclude unless tied to artifact evaluation or empirical SE method",
        },
        {
            "id": "X04",
            "candidate": "Google Scholar-only hits without accessible metadata",
            "reason": "E4",
            "decision": "exclude unless OpenAlex, DOI, publisher, DBLP, or official metadata can verify the candidate",
        },
        {
            "id": "X05",
            "candidate": "IEEE Xplore AI-driven IC design survey results",
            "reason": "E2",
            "decision": "exclude because the hit is algorithm/survey oriented, not artifact reproducibility oriented",
        },
        {
            "id": "X06",
            "candidate": "IEEE Xplore netlist extraction from image result",
            "reason": "E2",
            "decision": "exclude because it studies extraction accuracy, not artifact packaging or claim evidence",
        },
        {
            "id": "X07",
            "candidate": "OpenLane tutorial videos and secondary blog posts",
            "reason": "E4",
            "decision": "exclude in favor of official documentation/repository rows",
        },
        {
            "id": "X08",
            "candidate": "ResearchGate mirrors of EDA flow papers",
            "reason": "E4",
            "decision": "exclude in favor of publisher, arXiv, or official project pages",
        },
        {
            "id": "X09",
            "candidate": "Hardware-only RTL-to-GDSII implementation papers without AE focus",
            "reason": "E1",
            "decision": "exclude unless the source discusses reproducible software artifacts",
        },
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "candidate", "reason", "decision"])
        writer.writeheader()
        writer.writerows(rows)


def write_gap_map(path: Path) -> None:
    categories = {}
    for row in ALL_SOURCES:
        categories.setdefault(row["category"], []).append(row)
    lines = [
        "# Related Work Gap Map",
        "",
        f"Mapped sources: {len(ALL_SOURCES)}",
        "",
        "ArtifactGate-EDA should be positioned as complementary to existing packaging, artifact "
        "evaluation, provenance, and EDA workflow systems. The recurring gap is G5-G8 from the "
        "stronger plan: EDA-specific evidence levels, claim-evidence binding, unsupported "
        "hardware-overclaim blocking, and reviewer-ready ledgers.",
        "",
    ]
    for category, rows in sorted(categories.items()):
        lines.extend([f"## {category}", "", "| ID | Tool / Method | Gap For ArtifactGate |", "|---|---|---|"])
        for row in rows:
            lines.append(f"| {row['id']} | {row['tool_or_method']} | {row['gap_for_artifactgate']} |")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_gap_table(path: Path) -> None:
    rows = [
        ["System/process", "Packaging", "Replay", "Provenance", "EDA-aware", "Evidence-level model", "Claim-evidence binding", "Hardware-overclaim blocking"],
        ["ReproZip", "yes", "yes", "yes", "no", "no", "no", "no"],
        ["RO-Crate", "yes", "partial", "metadata", "no", "no", "no", "no"],
        ["Code Ocean", "yes", "yes", "yes", "no", "no", "no", "no"],
        ["DVC", "data/ML", "pipeline", "partial", "no", "no", "no", "no"],
        ["ACM/SIGSOFT AE", "process", "partial", "no", "domain-general", "no", "manual", "no"],
        ["FuseSoC", "HDL build", "tool run", "partial", "yes", "no", "no", "no"],
        ["Edalize", "no", "tool run", "partial", "yes", "no", "no", "no"],
        ["OpenROAD/OpenLane", "flow", "yes", "logs", "yes", "no", "no", "no"],
        ["mflowgen/SiliconCompiler/Hammer", "flow", "tool run", "manifest/logs", "yes", "no", "no", "no"],
        ["AutoBench / MLCAD artifact", "artifact", "yes", "artifact DOI", "yes", "no", "manual", "no"],
        ["SLSA/in-toto", "no", "no", "yes", "no", "no", "no", "no"],
        ["ArtifactGate-EDA", "yes", "yes", "yes", "yes", "yes", "yes/automated", "yes"],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def write_search_log(path: Path) -> None:
    fieldnames = [
        "database",
        "query",
        "search_interface",
        "date",
        "returned_count",
        "screened_count",
        "included_count",
        "included_ids",
        "notes",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(SEARCH_LOG_ROWS)


def write_source_quality_audit(path: Path) -> None:
    scholarly_types = {"paper", "book", "book_chapter", "technical_report", "standard", "specification"}
    rows = []
    for row in ALL_SOURCES:
        source_class = "scholarly_or_standard" if row["type"] in scholarly_types else "tool_policy_or_repository"
        rows.append(
            {
                "id": row["id"],
                "type": row["type"],
                "category": row["category"],
                "source_class": source_class,
                "use_in_manuscript": "cite_for_gap" if source_class == "scholarly_or_standard" else "cite_for_tool_scope",
                "quality_note": row["gap_for_artifactgate"],
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "type", "category", "source_class", "use_in_manuscript", "quality_note"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_citation_expansion_log(path: Path) -> None:
    rows = [
        {
            "seed_id": "S04",
            "seed_title": "ReproZip",
            "expansion_type": "tool_lineage",
            "candidate_ids": "S05;S06;S08;S10;S12;S13;S52",
            "status": "mapped",
            "note": "Expanded from computational reproducibility packaging to research-object and container approaches.",
        },
        {
            "seed_id": "S02",
            "seed_title": "ACM Artifact Review and Badging",
            "expansion_type": "artifact_evaluation_practice",
            "candidate_ids": "S03;S14;S15;S47;S48;S49;S50;S51;S53",
            "status": "mapped",
            "note": "Expanded from policy to software engineering, systems, FPGA, and MLCAD artifact-evaluation practice.",
        },
        {
            "seed_id": "S16",
            "seed_title": "FuseSoC",
            "expansion_type": "eda_tool_lineage",
            "candidate_ids": "S17;S18;S19;S20;S21;S22;S23;S24;S25;S26;S27;S28;S29",
            "status": "mapped",
            "note": "Expanded from HDL build tooling to EDA flow/build-system tools.",
        },
        {
            "seed_id": "S39",
            "seed_title": "GQM",
            "expansion_type": "empirical_se_method",
            "candidate_ids": "S40;S41;S42;S43;S54;S55;S56",
            "status": "mapped",
            "note": "Expanded from measurement framing to empirical SE methods, experiments, cases, and mapping studies.",
        },
        {
            "seed_id": "S35",
            "seed_title": "SLSA provenance",
            "expansion_type": "provenance_attestation",
            "candidate_ids": "S36;S37;S38",
            "status": "mapped",
            "note": "Expanded from supply-chain provenance to attestation and general provenance vocabulary.",
        },
        {
            "seed_id": "openalex_citation_network",
            "seed_title": "Google Scholar-compatible citation-network follow-up",
            "expansion_type": "forward_backward_citation",
            "candidate_ids": "S47;S48;S49;S50;S51;S53;S57",
            "status": "mapped_with_accessible_metadata",
            "note": "Direct Google Scholar querying was not machine-accessible; OpenAlex/DOI/publisher metadata closed the forward-backward expansion check.",
        },
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["seed_id", "seed_title", "expansion_type", "candidate_ids", "status", "note"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_citation_network_verification(path: Path) -> None:
    rows = [
        {
            "query_id": "CN01",
            "seed_or_query": "AutoBench Automatic Testbench Generation Evaluation LLMs HDL Design",
            "source": "OpenAlex public API plus IEEE/ACM/arXiv metadata",
            "returned_count": "38",
            "screened_count": "3",
            "selected_ids": "S57",
            "status": "verified",
            "note": "OpenAlex returned IEEE DOI 10.1109/MLCAD62225.2024.10740250 and ACM/arXiv records; publisher/preprint metadata records the artifact DOI.",
        },
        {
            "query_id": "CN02",
            "seed_or_query": "artifact evaluation FPGA community ACM TRETS",
            "source": "OpenAlex public API plus ACM DOI metadata",
            "returned_count": "16",
            "screened_count": "3",
            "selected_ids": "S50",
            "status": "verified",
            "note": "Used to confirm FPGA/TRETS artifact-evaluation context without adding unsupported hardware-validation claims.",
        },
        {
            "query_id": "CN03",
            "seed_or_query": "artifact evaluation software engineering generative AI",
            "source": "arXiv metadata and DOI/public metadata",
            "returned_count": "10",
            "screened_count": "3",
            "selected_ids": "S53",
            "status": "verified",
            "note": "Used as current SE artifact-evaluation position evidence, not as a core ArtifactGate dependency.",
        },
        {
            "query_id": "CN04",
            "seed_or_query": "Understanding and improving artifact sharing in software engineering research",
            "source": "Springer DOI metadata and OpenAlex title search",
            "returned_count": ">=3",
            "screened_count": "3",
            "selected_ids": "S51",
            "status": "verified",
            "note": "Used to connect artifact-sharing concerns to empirical software-engineering literature.",
        },
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "query_id",
                "seed_or_query",
                "source",
                "returned_count",
                "screened_count",
                "selected_ids",
                "status",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_crosswalk(path: Path) -> None:
    table_rows = {
        "ReproZip": "S04;S05",
        "RO-Crate": "S06;S07",
        "Code Ocean": "S08",
        "DVC": "S09",
        "ACM/SIGSOFT AE": "S02;S03;S47;S48;S49;S51;S53",
        "FuseSoC": "S16",
        "Edalize": "S17;S18",
        "OpenROAD/OpenLane": "S19;S20;S21",
        "mflowgen/SiliconCompiler/Hammer": "S22;S23;S24;S25;S26;S27",
        "AutoBench / MLCAD artifacts": "S57",
        "SLSA/in-toto": "S35;S36;S37",
        "ArtifactGate-EDA": "local contribution row; not counted as external literature",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["paper_table_row", "matrix_source_ids"])
        writer.writeheader()
        for paper_row, ids in table_rows.items():
            writer.writerow({"paper_table_row": paper_row, "matrix_source_ids": ids})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="literature/literature_matrix.csv")
    args = parser.parse_args()
    out = Path(args.out)
    write_matrix(out)
    write_protocol(out.with_name("search_protocol.md"))
    write_search_log(out.with_name("search_log.csv"))
    write_exclusion_log(out.with_name("exclusion_log.csv"))
    write_gap_map(out.with_name("related_work_gap_map.md"))
    write_gap_map(out.with_name("gap_map.md"))
    write_source_quality_audit(out.with_name("source_quality_audit.csv"))
    write_citation_expansion_log(out.with_name("citation_expansion_log.csv"))
    write_citation_network_verification(out.with_name("citation_network_verification.csv"))
    write_crosswalk(out.with_name("matrix_to_gap_table_crosswalk.csv"))
    write_gap_table(Path("paper/tables/related_work_gap_table.csv"))
    print(f"mapped {len(ALL_SOURCES)} literature/source rows -> {out}")
    return 0 if len(ALL_SOURCES) >= 40 else 1


if __name__ == "__main__":
    raise SystemExit(main())
