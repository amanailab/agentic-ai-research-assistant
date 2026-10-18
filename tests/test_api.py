
from fastapi.testclient import TestClient

import api


client = TestClient(api.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_research_endpoint(monkeypatch):
    def fake_research(query: str):
        return {
            "query": query,
            "findings": "Three relevant findings.",
            "analysis": "The evidence has some limitations.",
            "report": "# Research Report\nTest report.",
            "sources": [
                {
                    "title": "Example Source",
                    "url": "https://example.com",
                    "snippet": "Example snippet",
                }
            ],
        }

    monkeypatch.setattr(api, "run_research", fake_research)

    response = client.post(
        "/research",
        json={"query": "Agentic AI applications"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "Agentic AI applications"
    assert "Research Report" in data["report"]
    assert len(data["sources"]) == 1


def test_research_rejects_short_query():
    response = client.post(
        "/research",
        json={"query": "AI"},
    )

    assert response.status_code == 422


def test_research_handles_workflow_error(monkeypatch):
    def fake_research(query: str):
        raise RuntimeError("Simulated failure")

    monkeypatch.setattr(api, "run_research", fake_research)

    response = client.post(
        "/research",
        json={"query": "Agentic AI applications"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Research workflow failed. Please try again."
    )
