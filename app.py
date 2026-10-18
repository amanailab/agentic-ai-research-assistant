
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "amanai-agentic-research-assistant",
)

LANGSMITH_URL = "https://smith.langchain.com/"

# --------------------------------------------------
# Streamlit page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Agentic AI Research Assistant",
    page_icon="🔬",
    layout="wide",
)

# --------------------------------------------------
# Application header
# --------------------------------------------------

st.title("🔬 Agentic AI Research Assistant")

st.caption(
    "Research the web, analyze findings, and generate "
    "a structured report using multiple AI agents."
)

st.markdown(
    """
    **Powered by:** LangGraph · Groq · FastAPI · LangSmith

    Enter a research question below to start the
    multi-agent research workflow.
    """
)

# --------------------------------------------------
# Research form
# --------------------------------------------------

with st.form("research_form"):
    query = st.text_area(
        "What would you like to research?",
        placeholder=(
            "Example: How are AI agents transforming "
            "software development?"
        ),
        height=120,
        max_chars=500,
    )

    submitted = st.form_submit_button(
        "🔍 Research Topic",
        type="primary",
        use_container_width=True,
    )

# --------------------------------------------------
# Execute research workflow through FastAPI
# --------------------------------------------------

if submitted:
    if not query.strip():
        st.warning("Please enter a research question.")

    elif len(query.strip()) < 3:
        st.warning(
            "Please enter a research question "
            "containing at least 3 characters."
        )

    else:
        try:
            with st.spinner(
                "AI agents are researching, analyzing, "
                "and preparing your report..."
            ):
                response = requests.post(
                    f"{API_BASE_URL.rstrip('/')}/research",
                    json={"query": query.strip()},
                    timeout=300,
                )

            if response.ok:
                result = response.json()

                st.success("Research completed successfully!")

                # Display report sections.
                tab1, tab2, tab3, tab4 = st.tabs(
                    [
                        "📄 Final Report",
                        "🔎 Research Findings",
                        "📊 Analysis",
                        "🔗 Sources",
                    ]
                )

                with tab1:
                    st.markdown(
                        result.get(
                            "report",
                            "No report was returned.",
                        )
                    )

                    st.download_button(
                        label="Download Report",
                        data=result.get("report", ""),
                        file_name="research_report.md",
                        mime="text/markdown",
                    )

                with tab2:
                    st.markdown(
                        result.get(
                            "findings",
                            "No research findings returned.",
                        )
                    )

                with tab3:
                    st.markdown(
                        result.get(
                            "analysis",
                            "No analysis returned.",
                        )
                    )

                with tab4:
                    sources = result.get("sources", [])

                    if not sources:
                        st.info("No sources were returned.")

                    for source in sources:
                        title = source.get("title", "Source")
                        url = source.get("url", "")
                        snippet = source.get("snippet", "")

                        if url.startswith(("https://", "http://")):
                            st.markdown(f"- [{title}]({url})")
                        else:
                            st.write(title)

                        if snippet:
                            st.caption(snippet)

                st.caption(
                    "Research pipeline: Research Agent → "
                    "Analyst Agent → Writer Agent"
                )

            elif response.status_code == 422:
                st.error(
                    "The API rejected the request. "
                    "Check the research question and try again."
                )

            else:
                st.error(
                    f"API request failed "
                    f"(HTTP {response.status_code})."
                )

                with st.expander("Technical details"):
                    st.code(response.text)

        except requests.exceptions.Timeout:
            st.error(
                "The research request timed out. "
                "Check the backend logs and try again."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Make sure the backend is running and "
                "API_BASE_URL is configured correctly."
            )

        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")

        except ValueError:
            st.error(
                "The backend returned an invalid response. "
                "Check the FastAPI logs."
            )

# --------------------------------------------------
# LangSmith observability section
# --------------------------------------------------

st.divider()

st.subheader("🔭 Workflow Observability")

st.write(
    "Use LangSmith to inspect supported workflow traces, "
    "LLM calls, latency, and errors."
)

st.link_button(
    "Open LangSmith Dashboard ↗",
    LANGSMITH_URL,
    use_container_width=True,
)

st.caption(f"Configured LangSmith project: {LANGSMITH_PROJECT}")

st.info(
    "Traces appear only when LangSmith tracing is enabled, "
    "the API key is valid, and the backend workflow has run. "
    "The dashboard link does not guarantee that traces exist."
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "AmanAI Lab | Agentic AI Research Assistant | "
    "Built with Python, LangGraph, Groq, FastAPI, "
    "Streamlit, and LangSmith"
)
