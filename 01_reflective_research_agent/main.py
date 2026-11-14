"""
Main entry point and orchestrator for the Reflective Research Agent.

Coordinates the complete 4-stage agentic workflow:
1. Planner Agent: Decomposes a research topic into structured steps.
2. Research Agent: Queries Wikipedia, arXiv, and Tavily to build an evidence dossier.
3. Writer Agent: Drafts a comprehensive technical report in Markdown.
4. Editor Agent (Reflection): Critiques and refines the draft into a publication-ready report.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Ensure module directory is in sys.path for direct imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from schemas import ResearchPlan, ResearchDossier, EditorialReview
from planner import generate_research_plan
from researcher import conduct_research
from writer import write_research_report
from editor import edit_and_reflect

load_dotenv()


def run_reflective_research_pipeline(
    topic: str,
    output_path: str | Path | None = None,
    model: str = "gemini-3.5-flash",
) -> tuple[str, EditorialReview]:
    """
    Execute the end-to-end multi-agent research workflow.

    Args:
        topic: The user's research topic or prompt.
        output_path: Optional path to save the final markdown report.
        model: The Gemini model to use for all agents (default: gemini-3.5-flash).

    Returns:
        A tuple of (final_markdown_report, editorial_review_object).
    """
    client = genai.Client()

    print("\n" + "=" * 75)
    print(" 🚀 STARTING REFLECTIVE RESEARCH AGENT WORKFLOW")
    print("=" * 75)
    print(f"Topic: \"{topic}\"\nModel: {model}\n")

    # -------------------------------------------------------------------------
    # STAGE 1: PLANNER AGENT
    # -------------------------------------------------------------------------
    print("=" * 75)
    print(" [STAGE 1/4] 🧠 PLANNER AGENT: Decomposing topic into research blueprint...")
    print("=" * 75)
    plan: ResearchPlan = generate_research_plan(topic, model=model, client=client)

    print(f"\nStrategy: {plan.strategy_overview}\n")
    print(f"Generated {len(plan.steps)} sequential research steps:")
    for step in plan.steps:
        print(f"  [{step.step_number}] {step.tool.value.upper()}: \"{step.search_query}\"")
        print(f"      Question: {step.question}")

    # -------------------------------------------------------------------------
    # STAGE 2: RESEARCH AGENT & TOOL EXECUTION
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 2/4] 🔍 RESEARCH AGENT: Executing tool queries and synthesizing data...")
    print("=" * 75)
    dossier: ResearchDossier = conduct_research(plan, model=model, client=client)

    total_citations = sum(len(f.citations) for f in dossier.findings)
    print(f"\nResearch Complete: Gathered evidence across {len(dossier.findings)} steps ({total_citations} total citations).")

    # -------------------------------------------------------------------------
    # STAGE 3: WRITER AGENT
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 3/4] ✍️  WRITER AGENT: Synthesizing dossier into initial draft...")
    print("=" * 75)
    draft: str = write_research_report(dossier, model=model, client=client)
    print(f"\nInitial Draft Generated ({len(draft)} characters, ~{len(draft.split())} words).")

    # -------------------------------------------------------------------------
    # STAGE 4: EDITOR AGENT (REFLECTION PATTERN)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 4/4] 🧐 EDITOR AGENT (REFLECTION): Critiquing and refining draft...")
    print("=" * 75)
    review: EditorialReview = edit_and_reflect(draft, dossier, model=model, client=client)

    print("\n--- Editorial Critique Highlights ---")
    print(f"Clarity:    {review.critique_clarity[:150]}...")
    print(f"Grounding:  {review.critique_grounding[:150]}...")
    print(f"Citations:  {review.critique_citations[:150]}...")
    print("\nKey Improvements Applied:")
    for imp in review.improvements_made:
        print(f"  ✓ {imp}")

    final_report = review.final_report

    # -------------------------------------------------------------------------
    # SAVE ARTIFACT
    # -------------------------------------------------------------------------
    if output_path is None:
        # Default filename based on topic or fallback
        output_path = Path("research_report.md")
    else:
        output_path = Path(output_path)

    output_path.write_text(final_report, encoding="utf-8")
    print("\n" + "=" * 75)
    print(f" ✅ FINAL REPORT SAVED TO: {output_path.resolve()}")
    print("=" * 75)

    return final_report, review


def main():
    parser = argparse.ArgumentParser(
        description="Reflective Research Agent - Multi-Agent Research System"
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="The research topic. If not provided, you will be prompted interactively.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="01_reflective_research_agent/final_report.md",
        help="Path where the final Markdown report should be saved.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3.5-flash",
        help="Gemini model to use for inference (default: gemini-3.5-flash).",
    )

    args = parser.parse_args()

    topic = args.topic
    if not topic:
        print("=" * 70)
        print(" DeepLearning.AI: Reflective Research Agent")
        print("=" * 70)
        print("Sample topics to try:")
        print("  1. Recent advances in LLM tool-calling and function calling (2024-2026)")
        print("  2. How do vector databases work, and how are they used in RAG systems?")
        print("-" * 70)
        topic = input("\nEnter research topic: ").strip()

    if not topic:
        print("No topic provided. Exiting.")
        sys.exit(1)

    run_reflective_research_pipeline(
        topic=topic,
        output_path=args.output,
        model=args.model,
    )


if __name__ == "__main__":
    main()

