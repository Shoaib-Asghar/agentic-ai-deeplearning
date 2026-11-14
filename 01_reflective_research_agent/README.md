# Project 1: Reflective Research Agent

A 4-stage multi-agent pipeline that plans, researches, writes, and self-edits a comprehensive research report on any topic from first principles.

Built with Python 3.12, `uv`, Pydantic v2, and Google Gemini (`gemini-3.5-flash`) via the native `google-genai` SDK.

---

## Architecture & Data Flow

```text
User Topic
    │
    ▼
[Planner Agent] (planner.py)
    │  - Decomposes topic into 3-5 sub-questions
    │  - Maps each step to optimal tool (Wikipedia, arXiv, Tavily)
    │  - Emits: ResearchPlan (Pydantic)
    ▼
[Research Agent & Tools] (researcher.py & tools.py)
    │  - Queries Wikipedia API, arXiv API, and Tavily Web Search
    │  - Low-temperature (0.1) extraction of facts & citation URLs
    │  - Emits: ResearchDossier (Pydantic)
    ▼
[Writer Agent] (writer.py)
    │  - Thematic synthesis (not a step-by-step log)
    │  - Drafts Executive Summary, Deep-Dive, & References
    │  - Emits: Markdown Draft
    ▼
[Editor Agent / Reflection] (editor.py)
    │  - Actor-Critic / Evaluator-Optimizer loop
    │  - Evaluates draft against Clarity, Grounding, & Citation rubrics
    │  - Emits: EditorialReview with final polished report
    ▼
[Output Artifact] (final_report.md)
```

---

## File Structure & Responsibilities

| File | Core Role | Design Pattern / Technique |
|---|---|---|
| [`schemas.py`](./schemas.py) | Data contracts | Pydantic models for structured output (`ResearchPlan`, `StepFinding`, `ResearchDossier`, `EditorialReview`). |
| [`tools.py`](./tools.py) | Retrieval adapters | Standardized wrapper functions for Wikipedia, arXiv, and Tavily with custom User-Agent and error handling. |
| [`planner.py`](./planner.py) | Task decomposition | **Planning Pattern**: Translates broad user topics into structured, sequential research steps. |
| [`researcher.py`](./researcher.py) | Fact extraction & search | **Tool Use Pattern**: Executes tool queries and extracts verified facts and direct links at low entropy (`temp=0.1`). |
| [`writer.py`](./writer.py) | Synthesis | Weaves the research dossier into an authoritative, multi-section Markdown report. |
| [`editor.py`](./editor.py) | Fact-checking & polish | **Reflection Pattern**: Self-critiques the draft for flow, grounding, and citation completeness before rewriting. |
| [`main.py`](./main.py) | Orchestrator & CLI | Chained workflow orchestrator with interactive CLI and file export. |

---

## Running the Pipeline

### Interactive Mode
```bash
uv run python 01_reflective_research_agent/main.py
```
*Prompts you to enter any research topic in the terminal.*

### CLI Mode (Custom Topic & Output)
```bash
uv run python 01_reflective_research_agent/main.py \
  --topic "How do vector databases work, and how are they used in RAG systems?" \
  --output 01_reflective_research_agent/final_report.md
```

### Running Individual Agents Standalone
Each module includes a `__main__` test block so you can inspect individual agent behaviors:

```bash
# Test the Planner on a topic
uv run python 01_reflective_research_agent/planner.py

# Test the Tools (Wikipedia, arXiv, Tavily)
uv run python 01_reflective_research_agent/tools.py

# Test the Researcher synthesis on a single step
uv run python 01_reflective_research_agent/researcher.py

# Test the Writer draft synthesis
uv run python 01_reflective_research_agent/writer.py

# Test the Editor reflection & critique loop
uv run python 01_reflective_research_agent/editor.py
```
