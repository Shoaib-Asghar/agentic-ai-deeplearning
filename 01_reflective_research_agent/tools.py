"""
Retrieval tools for the Reflective Research Agent.

Provides clean, standardized interfaces for:
1. Wikipedia: Foundational knowledge, definitions, and domain overviews.
2. arXiv: Peer-reviewed and pre-print academic research papers.
3. Tavily: Real-time web search for recent industry updates and live documentation.

Each tool returns a concise, formatted text summary with citations (titles, dates, URLs),
ready for consumption by the downstream Research and Writer agents.
"""

import os
import arxiv
import wikipedia
from dotenv import load_dotenv

# Set custom User-Agent to satisfy Wikimedia API policy and prevent 403 blocks
wikipedia.set_user_agent("ReflectiveResearchAgent/1.0 (educational-agentic-ai-demo)")

load_dotenv()


def search_wikipedia(query: str, max_results: int = 2) -> str:
    """
    Search Wikipedia for foundational articles and return concise summaries.

    Args:
        query: Search keywords.
        max_results: Maximum number of related pages to summarize (default: 2).

    Returns:
        Formatted string containing page titles, URLs, and summaries.
    """
    try:
        page_titles = wikipedia.search(query, results=max_results)
        if not page_titles:
            return f"Wikipedia Search: No articles found matching '{query}'."

        results = []
        for title in page_titles:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                summary = wikipedia.summary(title, sentences=4, auto_suggest=False)
                results.append(
                    f"### [Wikipedia] {page.title}\n"
                    f"- URL: {page.url}\n"
                    f"- Summary: {summary}\n"
                )
            except wikipedia.DisambiguationError as e:
                # If ambiguous, try the first suggested option
                first_option = e.options[0] if e.options else None
                if first_option:
                    try:
                        summary = wikipedia.summary(first_option, sentences=3, auto_suggest=False)
                        results.append(
                            f"### [Wikipedia] {first_option} (disambiguated from '{title}')\n"
                            f"- Summary: {summary}\n"
                        )
                    except Exception:
                        continue
            except wikipedia.PageError:
                continue

        if not results:
            return f"Wikipedia Search: Found potential titles {page_titles}, but could not retrieve page details."

        return "\n".join(results)

    except Exception as e:
        return f"Wikipedia Search Error for '{query}': {type(e).__name__} - {str(e)}"


def search_arxiv(query: str, max_results: int = 3) -> str:
    """
    Search arXiv for academic papers, returning titles, authors, dates, and abstracts.

    Args:
        query: Academic search keywords.
        max_results: Number of papers to retrieve (default: 3).

    Returns:
        Formatted string containing paper titles, authors, published dates, URLs, and abstracts.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        papers = list(client.results(search))
        if not papers:
            return f"arXiv Search: No academic papers found matching '{query}'."

        results = []
        for paper in papers:
            authors = ", ".join(author.name for author in paper.authors[:3])
            if len(paper.authors) > 3:
                authors += " et al."

            pub_date = paper.published.strftime("%Y-%m-%d") if paper.published else "Unknown"

            # Truncate long abstracts to ~300 words to preserve context window
            abstract = " ".join(paper.summary.split())
            if len(abstract) > 600:
                abstract = abstract[:600] + "..."

            results.append(
                f"### [arXiv] {paper.title}\n"
                f"- Authors: {authors}\n"
                f"- Published: {pub_date}\n"
                f"- Paper URL: {paper.entry_id}\n"
                f"- PDF URL: {paper.pdf_url}\n"
                f"- Abstract: {abstract}\n"
            )

        return "\n".join(results)

    except Exception as e:
        return f"arXiv Search Error for '{query}': {type(e).__name__} - {str(e)}"


def search_tavily(query: str, max_results: int = 3) -> str:
    """
    Search the live web using Tavily API for recent news, industry docs, and benchmarks.

    Args:
        query: Search keywords.
        max_results: Number of search results to return (default: 3).

    Returns:
        Formatted string containing result titles, URLs, and content snippets.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "your_tavily_api_key_here":
        return (
            f"### [Tavily Web Search] Notice\n"
            f"- Query: '{query}'\n"
            f"- Status: TAVILY_API_KEY is not configured in .env. "
            f"Add a free Tavily API key to .env to enable real-time web search."
        )

    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
        )

        raw_results = response.get("results", [])
        if not raw_results:
            return f"Tavily Search: No web results found matching '{query}'."

        results = []
        for item in raw_results:
            title = item.get("title", "No Title")
            url = item.get("url", "")
            content = item.get("content", "").strip()
            if len(content) > 500:
                content = content[:500] + "..."

            results.append(
                f"### [Web Search] {title}\n"
                f"- Source: {url}\n"
                f"- Content: {content}\n"
            )

        return "\n".join(results)

    except Exception as e:
        return f"Tavily Search Error for '{query}': {type(e).__name__} - {str(e)}"


def execute_tool(tool_name: str, query: str) -> str:
    """
    Unified tool dispatcher: routes tool requests by name to the appropriate search function.

    Args:
        tool_name: One of 'wikipedia', 'arxiv', or 'tavily'.
        query: The search query string.

    Returns:
        The formatted tool result string.
    """
    normalized_tool = str(tool_name).lower().strip()

    if "wiki" in normalized_tool:
        return search_wikipedia(query)
    elif "arxiv" in normalized_tool:
        return search_arxiv(query)
    elif "tavily" in normalized_tool or "web" in normalized_tool:
        return search_tavily(query)
    else:
        return f"Tool Execution Error: Unknown tool '{tool_name}'. Available tools are: wikipedia, arxiv, tavily."


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Tool Integrations")
    print("=" * 60)

    # 1. Test Wikipedia
    print("\n--- 1. Testing Wikipedia Search ---")
    wiki_out = search_wikipedia("Function calling computer science", max_results=1)
    print(wiki_out)

    # 2. Test arXiv
    print("\n--- 2. Testing arXiv Search ---")
    arxiv_out = search_arxiv("LLM function calling tool use", max_results=1)
    print(arxiv_out)

    # 3. Test Tavily (with graceful key handling)
    print("\n--- 3. Testing Tavily Web Search ---")
    tavily_out = search_tavily("Model Context Protocol Anthropic 2025", max_results=1)
    print(tavily_out)

