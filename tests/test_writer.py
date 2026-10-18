
from agents.writer import write_report


if __name__ == "__main__":
    query = "Applications of agentic AI in healthcare"

    findings = """
    AI systems can help summarize medical literature
    and coordinate administrative workflows.
    Clinical applications require careful validation.
    """

    analysis = """
    Key insight: AI agents may reduce repetitive work.
    Limitation: The supplied findings contain no measured
    evidence of clinical outcomes or productivity gains.
    Recommendation: Evaluate systems in controlled workflows
    with human oversight.
    """

    report = write_report(query, findings, analysis)

    print("\n" + "=" * 60)
    print("FINAL RESEARCH REPORT")
    print("=" * 60)
    print(report)
