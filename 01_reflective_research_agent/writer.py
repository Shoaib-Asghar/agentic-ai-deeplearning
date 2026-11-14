"""
Writer Agent for the Reflective Research Agent pipeline.

Responsible for synthesizing the compiled ResearchDossier into a comprehensive,
well-structured initial draft of the research report in Markdown format.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Ensure module directory is in sys.path for direct imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from schemas import ResearchDossier, StepFinding

load_dotenv()

WRITER_SYSTEM_INSTRUCTION = """\
You are an expert Technical Writer and Research Synthesis Specialist. \
Your job is to transform a structured Research Dossier into an authoritative, \
comprehensive, and well-structured research report in GitHub-flavored Markdown.

Report Structure Guidelines:
1. # Title: Clear, professional title capturing the essence of the research topic.
2. ## Executive Summary: A high-level overview (2-3 paragraphs) summarizing the core findings, current state, and significance.
3. ## Thematic Sections: Synthesize the findings into 2-4 logical thematic deep-dive sections. \
Do NOT simply list "Step 1, Step 2"; instead, weave the evidence into cohesive technical narratives with subheadings, explanations, and bullet points where helpful.
4. ## Strategic Implications & Future Outlook: Synthesize what these findings mean for practitioners and researchers moving forward.
5. ## References & Sources: A dedicated section cataloging all cited papers, documentation, and articles using clickable Markdown links ([Source Title](URL)).

Writing Standards:
- Grounded: Rely strictly on the evidence, dates, authors, and insights present in the dossier.
- Professional: Objective, clear, and analytical tone.
- Well-cited: Attribute claims to the specific sources, authors, and papers gathered in the research.
"""


def format_dossier_for_prompt(dossier: ResearchDossier) -> str:
    """Format the ResearchDossier into structured context text for the Writer prompt."""
    lines = [
        f"RESEARCH TOPIC: {dossier.topic}\n",
        "=" * 60,
        "COMPILED RESEARCH FINDINGS (DOSSIER):",
        "=" * 60,
    ]

    for finding in dossier.findings:
        lines.append(f"\n[Step {finding.step_number}] Investigated: {finding.question}")
        lines.append(f"Tool Used: {finding.tool_used.upper()}")
        lines.append(f"Synthesized Evidence:\n{finding.summary}")
        lines.append("Cited Sources:")
        if finding.citations:
            for cite in finding.citations:
                lines.append(f"  - {cite}")
        else:
            lines.append("  - (No external URLs recorded)")
        lines.append("-" * 40)

    return "\n".join(lines)


def write_research_report(
    dossier: ResearchDossier,
    model: str = "gemini-3.5-flash",
    client: genai.Client | None = None,
) -> str:
    """
    Generate a full-length Markdown research report from a compiled ResearchDossier.

    Args:
        dossier: The compiled ResearchDossier from the Research Agent.
        model: The Gemini model to use for drafting (default: gemini-3.5-flash).
        client: Optional pre-configured genai.Client.

    Returns:
        The complete research report as a Markdown string.
    """
    if client is None:
        client = genai.Client()

    dossier_text = format_dossier_for_prompt(dossier)

    prompt = (
        f"Please write a comprehensive, professional Markdown research report based on the following dossier:\n\n"
        f"{dossier_text}\n\n"
        f"Ensure every citation and URL from the dossier is accurately preserved in the References section."
    )

    config = types.GenerateContentConfig(
        system_instruction=WRITER_SYSTEM_INSTRUCTION,
        temperature=0.3,  # Balanced temperature: articulate prose, strictly grounded facts
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise ValueError("Writer agent received an empty response from Gemini.")

    return response.text.strip()


if __name__ == "__main__":
    print("=" * 70)
    print("Testing Writer Agent on a Mock Research Dossier")
    print("=" * 70)

    # Create a realistic 2-step mock dossier to test drafting
    mock_dossier = ResearchDossier(
        topic="Recent advances in LLM tool-calling and function calling (2024-2026)",
        findings=[
            StepFinding(
                step_number=1,
                question="What are the foundational principles of function calling?",
                tool_used="wikipedia",
                summary=(
                    "In computer science, a function is a callable unit of software logic with a well-formed "
                    "interface that enables problem decomposition into chunks with low cognitive load. In language "
                    "models, function calling bridges natural language prompts with external APIs by generating "
                    "structured arguments that invoke these callable units."
                ),
                citations=["https://en.wikipedia.org/wiki/Function_(computer_programming)"],
            ),
            StepFinding(
                step_number=2,
                question="What are modern architectures for function calling in LLMs?",
                tool_used="arxiv",
                summary=(
                    "Recent academic literature emphasizes protocol-agnostic tool management. ToolRegistry (Ding & Stevens, 2025) "
                    "formalizes tool calling as Remote Procedure Calls (RPCs), using a universal stub across native Python, "
                    "OpenAPI, and Model Context Protocol (MCP). Zhao et al. (2026) introduce an action-class-oriented diagnostic "
                    "framework showing that multi-turn tool failure is primarily driven by action-class miscalibration."
                ),
                citations=[
                    "http://arxiv.org/abs/2507.10593v3",
                    "https://arxiv.org/pdf/2507.10593v3",
                    "http://arxiv.org/abs/2609.00949v2",
                ],
            ),
        ],
    )

    print("Drafting research report from dossier...\n")
    try:
        report = write_research_report(mock_dossier)
        print("Generated Report Preview:\n")
        print("=" * 70)
        # Print the first 1000 characters of the report
        print(report[:1200] + "\n\n... [truncated preview] ...")
        print("=" * 70)
        print(f"\nTotal characters generated: {len(report)}")
    except Exception as e:
        print(f"Error during report drafting: {type(e).__name__} - {e}")

