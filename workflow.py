
import os
from typing import TypedDict

from dotenv import load_dotenv

# Load configuration before initializing the workflow.
load_dotenv()

from langgraph.graph import END, START, StateGraph

from agents.researcher import research_topic
from agents.analyst import analyze_research
from agents.writer import write_report


class ResearchState(TypedDict, total=False):
    query: str
    findings: str
    analysis: str
    sources: list[dict]
    report: str


def research_node(state: ResearchState) -> dict:
    result = research_topic(state["query"])
    return {
        "findings": result["findings"],
        "sources": result["sources"],
    }


def analyst_node(state: ResearchState) -> dict:
    analysis = analyze_research(
        query=state["query"],
        findings=state["findings"],
    )
    return {"analysis": analysis}


def writer_node(state: ResearchState) -> dict:
    report = write_report(
        query=state["query"],
        findings=state["findings"],
        analysis=state["analysis"],
    )
    return {"report": report}


builder = StateGraph(ResearchState)

builder.add_node("researcher", research_node)
builder.add_node("analyst", analyst_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, "researcher")
builder.add_edge("researcher", "analyst")
builder.add_edge("analyst", "writer")
builder.add_edge("writer", END)

research_graph = builder.compile()


def run_research(query: str) -> ResearchState:
    if not query.strip():
        raise ValueError("Research query cannot be empty.")

    return research_graph.invoke({"query": query})
