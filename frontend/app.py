import os
import tempfile
import uuid
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from backend.orchestrator.graph import build_graph
from backend.pdf_exporter import export_report
from backend.rag.rag_engine import store_pdf_in_database
from backend.rag.chat_engine import ask_question
from backend.database import (
    create_tables,
    save_message,
    load_messages,
    clear_messages,
    save_research,
    load_recent_research,
)

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResearchAI | Multi-Agent Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. DATABASE INITIALIZATION
# =========================================================

create_tables()


# =========================================================
# 3. SESSION STATE
# =========================================================

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

if "researchai_session_id" not in st.session_state:
    query_session_id = st.query_params.get("chat")

    if query_session_id:
        st.session_state.researchai_session_id = query_session_id
    else:
        new_session_id = uuid.uuid4().hex
        st.query_params["chat"] = new_session_id
        st.session_state.researchai_session_id = new_session_id

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_messages(
        st.session_state.researchai_session_id
    )


# =========================================================
# 4. PROFESSIONAL DARK THEME
# =========================================================

st.markdown(
    """
    <style>

    /* MAIN APPLICATION */

    .stApp {
        background-color: #090E17;
        color: #E5E7EB;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background: #101722;
        border-right: 1px solid #253244;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #DCE5F0;
    }

    /* HERO SECTION */

    .hero {
        background: linear-gradient(
            120deg,
            #142B32 0%,
            #142337 55%,
            #17213A 100%
        );

        border: 1px solid #28505A;
        border-radius: 20px;
        padding: 34px;
        margin-bottom: 28px;
    }

    .hero h1 {
        color: #F8FAFC;
        font-size: 38px;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .hero p {
        color: #A9BAC9;
        font-size: 16px;
    }

    /* SECTION HEADINGS */

    h1, h2, h3 {
        color: #F1F5F9;
    }

    /* FEATURE CARDS */

    .feature-card {
        background: #131E2B;
        border: 1px solid #29394B;
        border-radius: 16px;
        padding: 22px;
        min-height: 155px;
        margin-bottom: 15px;
    }

    .feature-icon {
        font-size: 28px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: #F1F5F9;
        font-size: 18px;
        font-weight: 700;
    }

    .feature-description {
        color: #9BAABD;
        font-size: 14px;
        margin-top: 8px;
        line-height: 1.6;
    }

    /* AGENT CARDS */

    .agent-card {
        background: #131E2B;
        border: 1px solid #29394B;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        min-height: 105px;
    }

    .agent-name {
        color: #F1F5F9;
        font-size: 16px;
        font-weight: 650;
    }

    .agent-status {
        color: #91A4B8;
        font-size: 13px;
        margin-top: 9px;
    }

    /* METRIC CARDS */

    [data-testid="stMetric"] {
        background: #131E2B;
        border: 1px solid #29394B;
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #A7B6C7;
    }

    [data-testid="stMetricValue"] {
        color: #F1F5F9;
    }

    /* BUTTONS */

    div.stButton > button {
        background: #0F766E;
        color: white;
        border: 1px solid #168B80;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 650;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background: #115E59;
        border-color: #2DD4BF;
        color: white;
    }

    /* INPUTS */

    .stTextInput input,
    .stTextArea textarea {
        background: #111B29;
        color: #F1F5F9;
        border: 1px solid #34465A;
        border-radius: 10px;
    }

    /* DIVIDERS */

    hr {
        border-color: #263548;
    }

    /* FILE UPLOAD */

    [data-testid="stFileUploader"] {
        background: #111B29;
        border: 1px dashed #3A5968;
        border-radius: 12px;
        padding: 12px;
    }

    /* CHAT */

    [data-testid="stChatMessage"] {
        background: #131E2B;
        border-radius: 12px;
        border: 1px solid #29394B;
        padding: 12px;
    }

    /* LINKS */

    a {
        color: #5EEAD4;
    }
     
    
/* =========================================
   RESEARCHAI PREMIUM FUTURISTIC UPGRADE
========================================= */

/* MAIN BACKGROUND */
.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, rgba(13, 148, 136, 0.12), transparent 35%),
        radial-gradient(ellipse at 90% 10%, rgba(37, 99, 235, 0.10), transparent 35%),
        #080D16;
}

/* MAIN CONTENT */
.block-container {
    max-width: 1550px;
    padding-top: 2.5rem;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1724, #090F19);
    border-right: 1px solid rgba(45, 212, 191, 0.22);
}

[data-testid="stSidebar"] p {
    color: #C2D0DF;
}

/* HERO */
.hero {
    background:
        radial-gradient(circle at 85% 50%, rgba(20, 184, 166, 0.18), transparent 35%),
        linear-gradient(115deg, #102B35, #101B31 65%, #111A2B);
    border: 1px solid rgba(45, 212, 191, 0.35);
    border-radius: 22px;
    padding: 42px 36px;
    box-shadow: 0 12px 45px rgba(0, 0, 0, 0.22);
}

/* METRICS */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #142538, #101A29);
    border: 1px solid rgba(94, 234, 212, 0.22);
    border-radius: 17px;
    padding: 22px;
    transition: all 0.25s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #2DD4BF;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(20, 184, 166, 0.10);
}

/* FEATURE CARDS */
.feature-card {
    background: linear-gradient(145deg, #152538, #101A29);
    border: 1px solid #29445A;
    border-radius: 18px;
    padding: 25px;
    transition: all 0.25s ease;
}

.feature-card:hover {
    border-color: #2DD4BF;
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(20, 184, 166, 0.10);
}

/* AGENT CARDS */
.agent-card {
    background: linear-gradient(145deg, #152538, #101A29);
    border: 1px solid #29445A;
    border-radius: 17px;
    transition: all 0.25s ease;
}

.agent-card:hover {
    border-color: #38BDF8;
    transform: translateY(-3px);
}

/* BUTTONS */
div.stButton > button {
    border-radius: 11px;
    font-weight: 700;
    transition: all 0.2s ease;
    min-height: 44px;
}

div.stButton > button:hover {
    box-shadow: 0 0 18px rgba(45, 212, 191, 0.22);
    transform: translateY(-2px);
}

/* INPUT FIELDS */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #2DD4BF;
    box-shadow: 0 0 0 1px #2DD4BF;
}

/* DIVIDERS */
hr {
    border-color: rgba(148, 163, 184, 0.16);
}

/* SMOOTH PAGE */
[data-testid="stAppViewContainer"] {
    scroll-behavior: smooth;
}


    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 5. AGENT INFORMATION
# =========================================================

agent_names = {
    "researcher": "Research Agent",
    "web_researcher": "Web Research Agent",
    "document_reader": "Document Agent",
    "data_analyzer": "Data Agent",
    "analyst": "Analyst Agent",
    "reporter": "Report Agent",
}

agent_icons = {
    "researcher": "🔎",
    "web_researcher": "🌐",
    "document_reader": "📄",
    "data_analyzer": "📊",
    "analyst": "🧠",
    "reporter": "📝",
}


# =========================================================
# 6. SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown(
    """
    <div style="padding: 12px 0 20px 0;">
        <h2 style="color:#5EEAD4; margin-bottom:0;">
            🧠 ResearchAI
        </h2>
        <p style="color:#91A4B8; font-size:13px;">
            Multi-Agent Research Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.divider()

def navigate_to(destination):
    st.session_state.main_navigation = destination

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "New Research",
        "PDF Chatbot",
        "About ResearchAI",
    ],
    key="main_navigation",
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="
        background:#131E2B;
        border:1px solid #29394B;
        border-radius:12px;
        padding:14px;
    ">
        <p style="color:#5EEAD4;font-weight:650;">
            SYSTEM STATUS
        </p>
        <p style="color:#A7B6C7;font-size:13px;">
            ● ResearchAI Workspace
        </p>
        <p style="color:#A7B6C7;font-size:12px;">
            Powered by LangGraph, Gemini and ChromaDB
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
# =========================================================
# 7. DASHBOARD PAGE
# =========================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to ResearchAI 👋</h1>
            <p>
                Your intelligent multi-agent research workspace.
                Discover information, analyze documents and
                generate professional research reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Workspace Overview")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            label="AI Research Agents",
            value="06",
            delta="Multi-Agent System",
        )

    with metric2:
        st.metric(
            label="Uploaded Documents",
            value=len(st.session_state.uploaded_documents),
            delta="Current session",
        )

   
    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            label="AI Research Agents",
            value="06",
            delta="Multi-Agent System",
        )

    with metric2:
        st.metric(
            label="Uploaded Documents",
            value=len(st.session_state.uploaded_documents),
            delta="Current session",
        )

    with metric3:
        st.metric(
            label="Chat Messages",
            value=len(st.session_state.chat_history),
            delta="PDF Chatbot",
        )

    with metric4:
        st.metric(
            label="Research Platform",
            value="Ready",
            delta="System Active",
        )


    st.divider()

    # -----------------------------------------------------
    # QUICK ACTIONS
    # -----------------------------------------------------

    st.markdown("## Quick Actions")

    action1, action2 = st.columns(2)

    with action1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">Start New Research</div>
                <div class="feature-description">
                    Research any topic using six specialized
                    AI agents and generate a detailed report.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Start New Research →",
            key="dashboard_research",
            use_container_width=True,
            on_click=navigate_to,
            args=("New Research",),
        ):
            pass
    with action2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">Explore PDF Chatbot</div>
                <div class="feature-description">
                    Upload your research PDFs and ask questions
                    using Retrieval Augmented Generation.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Open PDF Chatbot →",
            key="dashboard_chatbot",
            use_container_width=True,
            on_click=navigate_to,
            args=("PDF Chatbot",),
        ):
            pass

    st.divider()

    # =====================================================
    # RECENT RESEARCH ACTIVITY
    # =====================================================

    st.markdown("## Recent Research Activity")

    recent_research = load_recent_research(5)

    if recent_research:

        for topic, created_at in recent_research:

            with st.container(border=True):

                st.markdown(f"**{topic}**")

                st.caption(f"Completed: {created_at}")

    else:

        st.info(
            "No research activity yet. "
            "Start your first research to see it here."
        )

    st.divider()

    # -----------------------------------------------------
    # SIX AI AGENTS
    # -----------------------------------------------------

    st.markdown("## Meet Your AI Research Team")

    st.caption(
        "Each agent performs a specialized task in the research workflow."
    )

    agent_descriptions = {
        "researcher": (
            "Breaks down the research topic and gathers core information."
        ),
        "web_researcher": (
            "Collects additional web research and relevant sources."
        ),
        "document_reader": (
            "Reads and extracts useful information from PDF documents."
        ),
        "data_analyzer": (
            "Analyzes uploaded CSV datasets and identifies patterns."
        ),
        "analyst": (
            "Combines findings and develops meaningful insights."
        ),
        "reporter": (
            "Creates the final structured research report."
        ),
    }

    agent_columns = st.columns(3)

    for index, (key, name) in enumerate(agent_names.items()):

        with agent_columns[index % 3]:

            st.markdown(
                f"""
                <div class="agent-card">
                    <div style="font-size:26px;">
                        {agent_icons[key]}
                    </div>

                    <div class="agent-name">
                        {name}
                    </div>

                    <div class="agent-status">
                        {agent_descriptions[key]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # -----------------------------------------------------
    # HOW IT WORKS
    # -----------------------------------------------------

    st.markdown("## How ResearchAI Works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📥</div>
                <div class="feature-title">01. Input</div>
                <div class="feature-description">
                    Enter a research topic and optionally
                    upload PDF or CSV files.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⚙️</div>
                <div class="feature-title">02. Processing</div>
                <div class="feature-description">
                    Specialized AI agents research,
                    analyze and combine information.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📑</div>
                <div class="feature-title">03. Final Report</div>
                <div class="feature-description">
                    Receive a structured research report
                    and download it as a PDF.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption(
        "ResearchAI | Intelligent Multi-Agent Research Platform"
    )


# =========================================================
# 8. ABOUT RESEARCHAI PAGE
# =========================================================

elif page == "About ResearchAI":
    agent_descriptions = {
        "researcher": "Breaks down the research topic and gathers core information.",
        "web_researcher": "Collects additional web research and relevant sources.",
        "document_reader": "Reads and extracts useful information from PDF documents.",
        "data_analyzer": "Analyzes uploaded CSV datasets and identifies patterns.",
        "analyst": "Combines findings and develops meaningful insights.",
        "reporter": "Creates the final structured research report.",
    }

    st.markdown(
        """
        <div class="hero">
            <h1>About ResearchAI 🧠</h1>
            <p>
                An intelligent research assistant built
                with a collaborative multi-agent architecture.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Project Overview")

    st.write(
        """
        ResearchAI is a multi-agent AI research platform designed
        to simplify information gathering, document understanding,
        dataset analysis and research report generation.

        It uses specialized AI agents coordinated through LangGraph.
        Each agent performs a particular task, and the orchestrator
        manages the overall workflow.
        """
    )

    st.divider()

    st.markdown("## Technology Stack")

    tech1, tech2, tech3 = st.columns(3)

    with tech1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🐍</div>
                <div class="feature-title">Python</div>
                <div class="feature-description">
                    Main programming language.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tech2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">LangGraph + Gemini</div>
                <div class="feature-description">
                    AI agent orchestration and language model.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tech3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🗄️</div>
                <div class="feature-title">ChromaDB + SQLite</div>
                <div class="feature-description">
                    Document retrieval and chat persistence.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("## AI Agent Architecture")

    for key, name in agent_names.items():

        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-name">
                    {agent_icons[key]} {name}
                </div>
                <div class="agent-status">
                    {agent_descriptions[key]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(
        "ResearchAI | Built with Python, Streamlit and LangGraph"
    )
    
# =========================================================
# 9. NEW RESEARCH PAGE
# =========================================================

elif page == "New Research":

    st.markdown(
        """
        <div class="hero">
            <h1>🚀 New Research Workspace</h1>
            <p>
                Start an intelligent research task using
                six specialized AI agents.
            </p>
            <p>
                Upload documents, analyze datasets and
                generate professional research reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Research Configuration")

    topic = st.text_input(
        "Research Topic",
        placeholder="Example: Artificial Intelligence in Healthcare",
        key="research_topic",
    )

    st.markdown("### Upload Research Files")

    pdf_col, csv_col = st.columns(2)

    with pdf_col:
        st.markdown("#### 📄 Research Document")

        pdf_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            key="research_pdf",
            help="Upload a PDF document for the Document Agent.",
        )

    with csv_col:
        st.markdown("#### 📊 Dataset")

        csv_file = st.file_uploader(
            "Upload CSV",
            type=["csv"],
            key="research_csv",
            help="Upload a CSV dataset for the Data Agent.",
        )

    st.divider()

    st.markdown("## Your AI Research Team")

    agent_columns = st.columns(3)

    for index, (key, name) in enumerate(agent_names.items()):

        with agent_columns[index % 3]:

            st.markdown(
                f"""
                <div class="agent-card">
                    <div style="font-size:25px;">
                        {agent_icons[key]}
                    </div>
                    <div class="agent-name">{name}</div>
                    <div class="agent-status">Ready for research</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    if st.button(
        "🚀 Start AI Research",
        type="primary",
        use_container_width=True,
        key="start_research",
    ):

        if not topic.strip():

            st.warning("Please enter a research topic.")

        else:

            pdf_path = ""
            csv_path = ""

            try:

                if pdf_file:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf",
                    ) as temp_pdf:

                        temp_pdf.write(pdf_file.getvalue())
                        pdf_path = temp_pdf.name

                if csv_file:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".csv",
                    ) as temp_csv:

                        temp_csv.write(csv_file.getvalue())
                        csv_path = temp_csv.name

                initial_state = {
                    "topic": topic.strip(),
                    "pdf_path": pdf_path,
                    "csv_path": csv_path,
                    "research": "",
                    "web_research": "",
                    "document_analysis": "",
                    "data_analysis": "",
                    "source_results": [],
                    "analysis": "",
                    "report": "",
                }

                st.markdown("## ⚙️ Live Agent Workflow")

                progress_bar = st.progress(0)

                progress_text = st.empty()

                status_placeholders = {}

                status_columns = st.columns(3)

                for index, (key, name) in enumerate(agent_names.items()):

                    with status_columns[index % 3]:

                        status_placeholders[key] = st.empty()

                        status_placeholders[key].markdown(
                            f"""
                            <div class="agent-card">
                                <div class="agent-name">
                                    {agent_icons[key]} {name}
                                </div>
                                <div class="agent-status">
                                    ⏳ Waiting
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                app = build_graph()

                completed = 0
                total = len(agent_names)
                result = None

                for event in app.stream(
                    initial_state,
                    stream_mode="updates",
                ):

                    for node_name, node_output in event.items():

                        if node_name in agent_names:

                            completed += 1

                            status_placeholders[node_name].markdown(
                                f"""
                                <div class="agent-card">
                                    <div class="agent-name">
                                        {agent_icons[node_name]}
                                        {agent_names[node_name]}
                                    </div>
                                    <div class="agent-status">
                                        ✅ Completed
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            progress_bar.progress(
                                min(completed / total, 1.0)
                            )

                            progress_text.write(
                                f"{completed} of {total} agents completed"
                            )

                        if node_name == "reporter":
                            result = node_output

                if not isinstance(result, dict) or "report" not in result:

                    raise RuntimeError(
                        "The research workflow finished, "
                        "but the final report was not generated."
                    )

                report = result["report"]

                if not report:

                    raise RuntimeError(
                        "The generated research report is empty."
                    )

                save_research(initial_state["topic"], report)

                progress_bar.progress(1.0)
                progress_bar.progress(1.0)

                progress_text.success(
                    "All research agents completed successfully!"
                )

                st.success("🎉 Research completed successfully!")

                st.divider()

                st.markdown("## 📑 Final Research Report")

                st.markdown(report)

                pdf_output = export_report(report)

                with open(pdf_output, "rb") as report_file:

                    pdf_data = report_file.read()

                st.download_button(
                    label="📥 Download Research Report (PDF)",
                    data=pdf_data,
                    file_name="ResearchAI_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

            except Exception as error:

                st.error("Something went wrong during research.")

                st.exception(error)

            finally:

                for file_path in [pdf_path, csv_path]:

                    if file_path and os.path.exists(file_path):

                        os.remove(file_path)

    st.divider()

    st.caption(
        "ResearchAI | Multi-Agent AI Research Workspace"
    )
    
# =========================================================
# 10. PDF CHATBOT PAGE
# =========================================================

elif page == "PDF Chatbot":

    st.markdown(
        """
        <div class="hero">
            <h1>📚 ResearchAI Document Assistant</h1>
            <p>
                Chat with your research documents.
                Ask questions and get answers grounded
                in your uploaded PDFs.
            </p>
            <p>
                Powered by RAG, Gemini Embeddings and ChromaDB.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # DOCUMENT UPLOAD
    # -----------------------------------------------------

    st.markdown("## 📥 Upload Research Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="knowledge_base_pdfs",
        help="Upload one or more PDF documents.",
    )

    if st.button(
        "📥 Add PDFs to Knowledge Base",
        type="primary",
        use_container_width=True,
    ):

        if not uploaded_files:

            st.warning("Please upload at least one PDF.")

        else:

            upload_folder = Path("data/uploads")
            upload_folder.mkdir(parents=True, exist_ok=True)

            for uploaded_file in uploaded_files:

                try:

                    document_key = (
                        uploaded_file.name,
                        uploaded_file.size,
                    )

                    already_uploaded = any(
                        doc["key"] == document_key
                        for doc in st.session_state.uploaded_documents
                    )

                    if already_uploaded:

                        st.info(
                            f"{uploaded_file.name} is already uploaded "
                            "in this session."
                        )

                        continue

                    safe_filename = (
                        f"{uuid.uuid4().hex}_"
                        f"{Path(uploaded_file.name).name}"
                    )

                    pdf_path = upload_folder / safe_filename

                    pdf_path.write_bytes(
                        uploaded_file.getvalue()
                    )

                    with st.spinner(
                        f"Processing {uploaded_file.name}..."
                    ):

                        document_id = store_pdf_in_database(
                            str(pdf_path)
                        )

                    st.session_state.uploaded_documents.append(
                        {
                            "key": document_key,
                            "name": uploaded_file.name,
                            "path": str(pdf_path),
                            "document_id": document_id,
                        }
                    )

                    st.success(
                        f"Successfully added: {uploaded_file.name}"
                    )

                except Exception as error:

                    st.error(
                        f"Could not process {uploaded_file.name}"
                    )

                    st.exception(error)

    st.divider()

    # -----------------------------------------------------
    # KNOWLEDGE BASE
    # -----------------------------------------------------

    st.markdown("## 🗂️ Your Knowledge Base")

    documents = st.session_state.uploaded_documents

    selected_document_id = None

    if not documents:

        st.info(
            "No PDFs uploaded yet. Upload a PDF above to get started."
        )

    else:

        st.success(
            f"{len(documents)} PDF document(s) available."
        )

        document_options = {
            "All uploaded PDFs": None
        }

        for index, document in enumerate(documents):

            label = (
                f"{document['name']} ({index + 1})"
            )

            document_options[label] = document["document_id"]

        selected_document = st.selectbox(
            "Choose which documents the chatbot should search:",
            list(document_options.keys()),
        )

        selected_document_id = document_options[
            selected_document
        ]

        with st.expander("View uploaded documents"):

            for document in documents:

                st.write(f"📄 {document['name']}")

    st.divider()

    # -----------------------------------------------------
    # CHAT HEADER AND CONTROLS
    # -----------------------------------------------------

    chat_col, clear_col = st.columns([4, 1])

    with chat_col:

        st.markdown("## 💬 Chat with Your Documents")

        st.caption(
            "Ask questions about the content of your uploaded PDFs."
        )

    with clear_col:

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):

            clear_messages(
                st.session_state.researchai_session_id
            )

            st.session_state.chat_history = []

            st.rerun()

    # -----------------------------------------------------
    # CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):

                with st.expander("📚 View Sources"):

                    for source in message["sources"]:

                        st.write(f"📄 {source}")

    # -----------------------------------------------------
    # ASK QUESTION
    # -----------------------------------------------------

    question = st.chat_input(
        "Ask something about your uploaded PDFs..."
    )

    if question:

        save_message(
            st.session_state.researchai_session_id,
            "user",
            question,
        )

        user_message = {
            "role": "user",
            "content": question,
            "sources": [],
        }

        st.session_state.chat_history.append(
            user_message
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "ResearchAI is searching your documents..."
            ):

                try:

                    result = ask_question(
                        question,
                        document_id=selected_document_id,
                    )

                    answer = result["answer"]

                    sources = result.get("sources", [])

                    st.markdown(answer)

                    if sources:

                        with st.expander("📚 View Sources"):

                            for source in sources:

                                st.write(f"📄 {source}")

                    save_message(
                        st.session_state.researchai_session_id,
                        "assistant",
                        answer,
                        sources,
                    )

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                except Exception as error:

                    st.error(
                        "Something went wrong while answering."
                    )

                    st.exception(error)

    st.divider()

    st.caption(
        "ResearchAI PDF Chatbot | Retrieval Augmented Generation"
    )