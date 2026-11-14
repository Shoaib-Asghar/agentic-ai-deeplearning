# Agentic AI — DeepLearning.AI

My workspace for DeepLearning.AI's **Agentic AI** course taught by Andrew Ng.

---

## Completed Projects

### 1. Reflective Research Agent ([Documentation](./01_reflective_research_agent/README.md))
Located in [`01_reflective_research_agent/`](./01_reflective_research_agent/).

A 4-stage multi-agent pipeline implementing the core Agentic Design Patterns:
* **Planner Agent (`planner.py`)**: Task decomposition into sequential sub-questions mapped to tools (**Planning Pattern**).
* **Research Agent & Tools (`researcher.py`, `tools.py`)**: Grounded fact extraction with citations from Wikipedia, arXiv, and Tavily (**Tool Use Pattern**).
* **Writer Agent (`writer.py`)**: Multi-section thematic synthesis of evidence into a technical Markdown draft.
* **Editor Agent (`editor.py`)**: Rubric-driven self-critique (Clarity, Grounding, Citations) and publication polish (**Reflection Pattern**).

---

## Quickstart & Environment Setup

### 1. Prerequisites & Installation
This repository uses modern `uv` project management (PEP 621):

```bash
# Clone the repository and sync virtual environment
uv sync
```

### 2. Configure API Keys
Copy the example environment file and add your Google Gemini API key:
```bash
cp .env.example .env
```
*(Add your `GEMINI_API_KEY` from Google AI Studio. `TAVILY_API_KEY` is optional for live web search).*

---

## Usage

### Run the Research Agent
```bash
# Interactive mode (prompts for a topic in terminal)
uv run python 01_reflective_research_agent/main.py

# CLI mode with custom topic and output file
uv run python 01_reflective_research_agent/main.py \
  --topic "How do vector databases work, and how are they used in RAG systems?" \
  --output 01_reflective_research_agent/final_report.md
```

### Run Type Checking & Diagnostics
```bash
# Run full repository static type check (Pyright engine)
uv run pyright

# Verify Gemini API connectivity & structured outputs
uv run python tests/test_connection.py
```
