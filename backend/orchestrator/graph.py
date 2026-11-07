
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from backend.agents.research_agent import ResearchAgent
from backend.agents.web_research_agent import WebResearchAgent
from backend.agents.document_agent import DocumentAgent
from backend.agents.data_agent import DataAgent
from backend.agents.analyst_agent import AnalystAgent
from backend.agents.report_agent import ReportAgent


class ResearchState(TypedDict):
    topic: str
    pdf_path: str
    csv_path: str
    research: str
    web_research: str
    document_analysis: str
    data_analysis: str
    source_results: list
    analysis: str
    report: str


def research_node(state: ResearchState):
    print("\n[1/6] Research Agent is working...")
    result = ResearchAgent().research(state["topic"])
    return {"research": result}


def web_research_node(state: ResearchState):
    print("\n[2/6] Web Research Agent is searching and reading...")
    results = WebResearchAgent().research(state["topic"], max_results=5)

    formatted_results = []

    for index, item in enumerate(results, start=1):
        formatted_results.append(f"""
Source {index}

Title: {item.get("title", "No title")}
URL: {item.get("url", "")}

Search Description:
{item.get("description", "No description")}

Extracted Webpage Content:
{item.get("content", "No content extracted")}
""")

    return {
        "web_research": "\n".join(formatted_results),
        "source_results": results
    }


def document_node(state: ResearchState):
    pdf_path = state.get("pdf_path", "").strip()

    if not pdf_path:
        print("\n[3/6] No PDF provided. Skipping Document Agent.")
        return {"document_analysis": ""}

    print("\n[3/6] Document Agent is reading your PDF...")
    result = DocumentAgent().analyze_pdf(pdf_path)
    return {"document_analysis": str(result)}


def data_node(state: ResearchState):
    csv_path = state.get("csv_path", "").strip()

    if not csv_path:
        print("\n[4/6] No CSV provided. Skipping Data Agent.")
        return {"data_analysis": ""}

    print("\n[4/6] Data Agent is analyzing your CSV...")
    result = DataAgent().analyze_csv(csv_path)

    if isinstance(result, list):
        result = "\n".join(
            item.get("text", "")
            for item in result
            if isinstance(item, dict)
        )

    return {"data_analysis": str(result)}


def analyst_node(state: ResearchState):
    print("\n[5/6] Analyst Agent is analyzing all research...")

    combined_research = (
        state["research"]
        + "\n\nWEB RESEARCH:\n" + state["web_research"]
        + "\n\nPDF DOCUMENT ANALYSIS:\n" + state["document_analysis"]
        + "\n\nCSV DATA ANALYSIS:\n" + state["data_analysis"]
    )

    result = AnalystAgent().analyze(combined_research)
    return {"analysis": result}


def report_node(state: ResearchState):
    print("\n[6/6] Report Agent is generating the report...")

    findings = (
        state["research"]
        + "\n\nWEB RESEARCH:\n" + state["web_research"]
        + "\n\nPDF DOCUMENT ANALYSIS:\n" + state["document_analysis"]
        + "\n\nCSV DATA ANALYSIS:\n" + state["data_analysis"]
        + "\n\nANALYSIS:\n" + state["analysis"]
    )

    result = ReportAgent().generate_report(state["topic"], findings)

    sources_section = "\n\n---\n\n## Sources\n\n"
    sources = state.get("source_results", [])

    if sources:
        for index, item in enumerate(sources, start=1):
            title = item.get("title", "Untitled source")
            url = item.get("url", "")
            sources_section += f"{index}. **{title}**\n"

            if url:
                sources_section += f"   URL: {url}\n\n"
    else:
        sources_section += "No web sources were found.\n"

    return {"report": result + sources_section}


def build_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("researcher", research_node)
    workflow.add_node("web_researcher", web_research_node)
    workflow.add_node("document_reader", document_node)
    workflow.add_node("data_analyzer", data_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("reporter", report_node)

    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "web_researcher")
    workflow.add_edge("web_researcher", "document_reader")
    workflow.add_edge("document_reader", "data_analyzer")
    workflow.add_edge("data_analyzer", "analyst")
    workflow.add_edge("analyst", "reporter")
    workflow.add_edge("reporter", END)

    return workflow.compile()
