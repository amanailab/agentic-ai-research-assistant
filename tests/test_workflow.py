
from workflow import run_research


if __name__ == "__main__":
    query = "How are AI agents being used in software development?"

    result = run_research(query)

    print("\n" + "=" * 60)
    print("RESEARCH QUESTION")
    print("=" * 60)
    print(result["query"])

    print("\n" + "=" * 60)
    print("RESEARCH FINDINGS")
    print("=" * 60)
    print(result["findings"])

    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)
    print(result["analysis"])

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result["report"])

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in result.get("sources", []):
        print(f"- {source['title']}: {source['url']}")
