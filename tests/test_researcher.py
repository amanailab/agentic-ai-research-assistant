
from agents.researcher import research_topic


if __name__ == "__main__":
    query = "Latest applications of agentic AI in healthcare"

    result = research_topic(query)

    print("\n" + "=" * 60)
    print("RESEARCH QUESTION")
    print("=" * 60)
    print(result["query"])

    print("\n" + "=" * 60)
    print("RESEARCH FINDINGS")
    print("=" * 60)
    print(result["findings"])

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in result["sources"]:
        print(f"- {source['title']}")
        print(f"  {source['url']}")
