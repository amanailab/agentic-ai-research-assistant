
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def analyze_research(query: str, findings: str) -> str:
    """Analyze research findings and identify useful insights."""

    if not query.strip():
        raise ValueError("Research query cannot be empty.")

    if not findings.strip():
        raise ValueError("Research findings cannot be empty.")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        api_key=api_key,
        temperature=0.2,
    )

    prompt = f"""
You are an analytical AI agent in a multi-agent research system.

Research question:
{query}

Research findings:
{findings}

Analyze the supplied findings and produce the following sections:

1. KEY INSIGHTS
Identify the most important findings.

2. PATTERNS AND TRENDS
Explain any patterns supported by the findings.

3. EVIDENCE AND LIMITATIONS
Identify what the evidence supports and what remains uncertain.

4. RECOMMENDATIONS
Provide practical recommendations relevant to the question.

Rules:
- Do not invent facts, statistics, or sources.
- Clearly identify unsupported conclusions.
- Distinguish evidence from interpretation.
- If information is insufficient, say so.
"""

    response = model.invoke(prompt)

    return response.content
