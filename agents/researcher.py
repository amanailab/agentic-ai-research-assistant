
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from tools.web_search import search_web

load_dotenv()


def research_topic(query: str) -> dict:
    """Research a topic using web search and an LLM."""

    if not query.strip():
        raise ValueError("Research query cannot be empty.")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        api_key=api_key,
        temperature=0.2,
    )

    results = search_web(query, max_results=5)

    if not results:
        raise RuntimeError(
            "No search results found. Try another research query."
        )

    sources = "\n\n".join(
        f"Title: {item['title']}\n"
        f"URL: {item['url']}\n"
        f"Content: {item['snippet']}"
        for item in results
    )

    prompt = f"""
You are a research agent.

Research question: {query}

Use only the supplied search results as evidence.
Summarize the key findings clearly.
Distinguish supported facts from uncertainty.
Do not invent facts or citations.
Include the URLs of relevant sources.

Search results:
{sources}
"""

    response = model.invoke(prompt)

    return {
        "query": query,
        "findings": response.content,
        "sources": results,
    }
