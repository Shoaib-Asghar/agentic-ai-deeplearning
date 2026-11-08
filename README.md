# Agentic AI — DeepLearning.AI

My workspace for DeepLearning.AI's **Agentic AI** course by Andrew Ng.

## Active Project: Reflective Research Agent
Located in [`01_reflective_research_agent/`](./01_reflective_research_agent/).

A multi-agent pipeline that plans, researches, writes, and self-edits a report:
1. **Planner Agent**: Decomposes a topic into targeted sub-questions and assigns appropriate research tools.
2. **Research Agent**: Queries external tools (Tavily web search, arXiv, Wikipedia) iteratively.
3. **Writer Agent**: Synthesizes findings into a cohesive initial draft.
4. **Editor Agent (Reflection)**: Critiques and revises the draft into a cited Markdown report.

---

## Environment & Setup

- **Python**: 3.12 (`.venv` managed with `uv`)
- **Primary LLM**: Google Gemini (`gemini-3.5-flash`) via the native `google-genai` SDK
- **Configuration**: API keys stored in `.env` (see `.env.example`)
