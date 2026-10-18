
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def write_report(
    query: str,
    findings: str,
    analysis: str,
) -> str:
    """Generate a structured report from research and analysis."""

    if not query.strip():
        raise ValueError("Research query cannot be empty.")

    if not findings.strip():
        raise ValueError("Research findings cannot be empty.")

    if not analysis.strip():
        raise ValueError("Research analysis cannot be empty.")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        api_key=api_key,
        temperature=0.3,
    )

    prompt = f"""
You are the Writer Agent in a multi-agent research system.

Create a professional research report using the supplied inputs.

RESEARCH QUESTION:
{query}

RESEARCH FINDINGS:
{findings}

ANALYST'S EVALUATION:
{analysis}

Use this report structure:

# Research Report
## 1. Executive Summary
## 2. Key Findings
## 3. Analysis and Trends
## 4. Limitations and Uncertainties
## 5. Recommendations
## 6. Sources

Rules:
- Preserve important limitations identified by the Analyst.
- Never invent statistics, facts, or source URLs.
- Keep conclusions consistent with the supplied evidence.
- Write clearly, professionally, and concisely.
- Include only source URLs present in the research findings.
"""

    response = model.invoke(prompt)

    return response.content
