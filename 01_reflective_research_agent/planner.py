"""
Planner Agent for the Reflective Research Agent pipeline.

The Planner is responsible for Task Decomposition: breaking a high-level research
topic into 3 to 5 sequential steps and selecting the appropriate retrieval tool
(Wikipedia, arXiv, or Tavily) for each step.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Allow running as a standalone script or as an imported module
try:
    from .schemas import ResearchPlan
except ImportError:
    from schemas import ResearchPlan

load_dotenv()

PLANNER_SYSTEM_INSTRUCTION = """\
You are an expert Research Planner. Your job is to analyze a user's research topic \
and decompose it into a structured, step-by-step investigation plan.

Guidelines for creating the plan:
1. Deconstruct the topic into 3 to 5 distinct, sequential research steps.
2. Select the optimal tool for each step:
   - 'wikipedia': Use for foundational definitions, core domain concepts, and historical background.
   - 'arxiv': Use for academic research papers, formal mathematical/algorithmic formulations, and benchmark evaluations.
   - 'tavily': Use for the latest industry developments, live web documentation, open-source libraries, and current year (2024-2026) trends.
3. Formulate precise, focused keyword search queries for each tool (avoid long conversational questions in search_query).
4. Order the steps logically: foundational concepts first, technical/academic deep dive next, followed by modern state-of-the-art developments.
"""


def generate_research_plan(
    topic: str,
    model: str = "gemini-3.5-flash",
    client: genai.Client | None = None,
) -> ResearchPlan:
    """
    Generate a validated ResearchPlan for a given topic using Gemini structured output.

    Args:
        topic: The user's research topic or prompt.
        model: The Gemini model to use (default: gemini-3.5-flash).
        client: Optional pre-configured genai.Client instance.

    Returns:
        A validated ResearchPlan instance containing sequential steps.
    """
    if client is None:
        client = genai.Client()

    config = types.GenerateContentConfig(
        system_instruction=PLANNER_SYSTEM_INSTRUCTION,
        temperature=0.2,  # Low temperature for deterministic, structured planning
        response_mime_type="application/json",
        response_schema=ResearchPlan,
    )

    prompt = f"Please create a comprehensive research plan for the following topic:\n\n\"{topic}\""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    # Validate and parse the structured JSON directly into our Pydantic model
    plan = ResearchPlan.model_validate_json(response.text)
    return plan


if __name__ == "__main__":
    # Test topic from the course curriculum
    sample_topic = "Recent advances in LLM tool-calling and function calling (2024-2026)"

    print("=" * 70)
    print(f"Generating Research Plan for:\n'{sample_topic}'")
    print("=" * 70)

    try:
        plan = generate_research_plan(sample_topic)

        print(f"\n[Topic]: {plan.topic}")
        print(f"[Strategy Overview]:\n{plan.strategy_overview}\n")
        print("-" * 70)
        print("Generated Research Steps:")
        print("-" * 70)

        for step in plan.steps:
            print(f"Step {step.step_number}: [{step.tool.value.upper()}]")
            print(f"  Question: {step.question}")
            print(f"  Search Query: '{step.search_query}'")
            print(f"  Rationale: {step.rationale}")
            print()

    except Exception as e:
        print(f"Error generating research plan: {type(e).__name__} - {e}")

