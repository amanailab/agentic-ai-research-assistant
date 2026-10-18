
from agents.analyst import analyze_research


if __name__ == "__main__":
    query = "Applications of agentic AI in healthcare"

    findings = """
    Research finding 1:
    AI agents can help summarize medical literature.

    Research finding 2:
    Agentic systems can coordinate multi-step administrative workflows.

    Research finding 3:
    Clinical deployment requires careful validation,
    privacy safeguards, and human oversight.
    """

    analysis = analyze_research(query, findings)

    print("\n" + "=" * 60)
    print("ANALYST AGENT OUTPUT")
    print("=" * 60)
    print(analysis)
