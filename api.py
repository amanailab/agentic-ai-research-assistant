
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from workflow import run_research

app = FastAPI(
    title="Agentic AI Research Assistant API",
    description="Multi-agent research powered by LangGraph and Groq",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=500,
        description="Topic or question to research",
    )


class ResearchResponse(BaseModel):
    query: str
    findings: str
    analysis: str
    report: str
    sources: list[dict]


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    try:
        result = run_research(request.query)

        return ResearchResponse(
            query=result["query"],
            findings=result["findings"],
            analysis=result["analysis"],
            report=result["report"],
            sources=result.get("sources", []),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail=str(exc)
        ) from exc

    except Exception as exc:
        # Log the exception in production; avoid exposing internals.
        raise HTTPException(
            status_code=500,
            detail="Research workflow failed. Please try again.",
        ) from exc
