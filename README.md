# Agentic AI — DeepLearning.AI

Hands-on workspace for DeepLearning.AI's **Agentic AI** course taught by Andrew Ng.

We build each agent system from first principles in minimal, understandable iterations.

## Active Project: Reflective Research Agent
Located in [`01_reflective_research_agent/`](./01_reflective_research_agent/).

A multi-agent pipeline that plans, researches, writes, and self-edits a report:
1. **Planner Agent**: Decomposes a topic into targeted sub-questions and assigns appropriate research tools.
2. **Research Agent**: Queries external tools (Tavily web search, arXiv, Wikipedia) iteratively.
3. **Writer Agent**: Synthesizes findings into a cohesive initial draft.
4. **Editor Agent (Reflection)**: Critiques and revises the draft into a cited Markdown report.

---

## Modern `uv` Workflow

The repository uses modern `uv` project standards (`pyproject.toml`, `uv.lock`, `.python-version`):

### 1. Synchronize Virtual Environment
```bash
uv sync
```
*Installs and locks dependencies deterministically in `.venv`.*

### 2. Run the Research Agent
```bash
# Interactive mode (prompts for a topic)
uv run python 01_reflective_research_agent/main.py

# CLI mode with custom topic and output file
uv run python 01_reflective_research_agent/main.py --topic "How do vector databases work in RAG systems?" --output my_report.md
```

### 3. Run Diagnostics & Tests
```bash
uv run python tests/test_connection.py
```
