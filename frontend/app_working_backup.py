import os
import tempfile
import uuid
from pathlib import Path

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
)


# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="ResearchAI",
    page_icon="🧠",
    layout="wide",
)

# Create the SQLite table before the pages are displayed.
create_tables()


# ---------- SESSION STATE AND CHAT DATABASE ----------
if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

# Keep a chat identifier in the browser URL so the same browser can
# reopen its own conversation. This is a simple local-app approach,
# not a user-authentication or multi-user security system.
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


# ---------- CUSTOM DESIGN ----------
st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #e5e7eb;
    }
    [data-testid="stSidebar"] {
        background: #111827;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #312e81);
        border: 1px solid #3730a3;
        margin-bottom: 25px;
    }
    .hero h1 {
        color: white;
        font-size: 38px;
    }
    .hero p {
        color: #c7d2fe;
        font-size: 16px;
    }
    .agent-card {
        background: #151e32;
        border: 1px solid #29364f;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .agent-name {
        font-size: 16px;
        font-weight: 600;
        color: #f1f5f9;
    }
    .agent-status {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 7px;
    }
    div.stButton > button {
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 9px;
        padding: 10px 22px;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: #6366f1;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- SIDEBAR ----------
st.sidebar.title("🧠 ResearchAI")
st.sidebar.caption("Multi-Agent Research Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["New Research", "PDF Chatbot", "About ResearchAI"],
)

st.sidebar.divider()
st.sidebar.caption("Powered by LangGraph + Gemini + ChromaDB")


# ---------- AGENT INFORMATION ----------
agent_names = {
    "researcher": "Research Agent",
    "web_researcher": "Web Research Agent",
    "document_reader": "Document Agent",
    "data_analyzer": "Data Agent",
    "analyst": "Analyst Agent",
    "reporter": "Report Agent",
}

agent_icons = {
    "researcher": "🔍",
    "web_researcher": "🌐",
    "document_reader": "📄",
    "data_analyzer": "📊",
    "analyst": "🧠",
    "reporter": "📝",
}


# ---------- ABOUT PAGE ----------
if page == "About ResearchAI":
    st.title("About ResearchAI")
    st.write(
        "ResearchAI is a multi-agent AI research platform "
        "that uses six specialized AI agents."
    )

    for key, name in agent_names.items():
        st.markdown(f"### {agent_icons[key]} {name}")

    st.info(
        "The LangGraph orchestrator manages the workflow "
        "and passes information between agents."
    )


# ---------- PDF CHATBOT PAGE ----------
elif page == "PDF Chatbot":
    st.markdown(
        """
        <div class="hero">
            <h1>📚 ResearchAI PDF Chatbot</h1>
            <p>Upload your research documents and ask questions.</p>
            <p>Powered by RAG, Gemini Embeddings and ChromaDB.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header("1. Upload Research Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="knowledge_base_pdfs",
    )

    if st.button("📥 Add PDFs to Knowledge Base"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            upload_folder = Path("data/uploads")
            upload_folder.mkdir(parents=True, exist_ok=True)

            for uploaded_file in uploaded_files:
                try:
                    document_key = (uploaded_file.name, uploaded_file.size)

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
                        f"{uuid.uuid4().hex}_{Path(uploaded_file.name).name}"
                    )
                    pdf_path = upload_folder / safe_filename
                    pdf_path.write_bytes(uploaded_file.getvalue())

                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        document_id = store_pdf_in_database(str(pdf_path))

                    st.session_state.uploaded_documents.append(
                        {
                            "key": document_key,
                            "name": uploaded_file.name,
                            "path": str(pdf_path),
                            "document_id": document_id,
                        }
                    )
                    st.success(f"Successfully added: {uploaded_file.name}")

                except Exception as error:
                    st.error(f"Could not process {uploaded_file.name}")
                    st.exception(error)

    st.divider()
    st.header("2. Your Knowledge Base")

    documents = st.session_state.uploaded_documents

    if not documents:
        st.info(
            "No PDFs uploaded yet. Upload a PDF above to get started."
        )
        selected_document_id = None
    else:
        st.success(f"{len(documents)} PDF document(s) available.")

        for document in documents:
            st.write(f"📄 {document['name']}")

        document_options = {"All uploaded PDFs": None}
        for index, document in enumerate(documents):
            label = f"{document['name']} ({index + 1})"
            document_options[label] = document["document_id"]

        selected_document = st.selectbox(
            "Choose which documents the chatbot should search:",
            list(document_options.keys()),
        )
        selected_document_id = document_options[selected_document]

    st.divider()
    st.header("3. Ask Your Documents")

    if st.button("🗑️ Clear Chat History"):
        clear_messages(st.session_state.researchai_session_id)
        st.session_state.chat_history = []
        st.rerun()

    # Display messages loaded from SQLite.
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.write(f"📄 {source}")

    question = st.chat_input(
        "Ask something about your uploaded PDFs..."
    )

    if question:
        # Save and display the user's question.
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
        st.session_state.chat_history.append(user_message)

        with st.chat_message("user"):
            st.markdown(question)

        # Ask the RAG engine and save the answer and its sources.
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
                        with st.expander("📚 Sources"):
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
                    st.error("Something went wrong while answering.")
                    st.exception(error)

    st.divider()
    st.caption(
        "ResearchAI PDF Chatbot | Retrieval Augmented Generation"
    )


# ---------- NEW RESEARCH PAGE ----------
else:
    st.markdown(
        """
        <div class="hero">
            <h1>🧠 ResearchAI</h1>
            <p>Your intelligent multi-agent research workspace.</p>
            <p>Research topics, analyze documents, understand datasets
            and generate professional reports.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header("Start New Research")

    topic = st.text_input(
        "Research Topic",
        placeholder="Example: Artificial Intelligence in Healthcare",
    )

    col1, col2 = st.columns(2)

    with col1:
        pdf_file = st.file_uploader(
            "📄 Upload PDF Document",
            type=["pdf"],
            key="research_pdf",
        )

    with col2:
        csv_file = st.file_uploader(
            "📊 Upload CSV Dataset",
            type=["csv"],
            key="research_csv",
        )

    st.divider()

    if st.button("🚀 Start Research", type="primary"):
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
                    "topic": topic,
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

                st.header("🤖 AI Agent Workflow")
                progress_bar = st.progress(0)
                progress_text = st.empty()
                status_placeholders = {}
                cols = st.columns(3)

                for index, (key, name) in enumerate(agent_names.items()):
                    with cols[index % 3]:
                        status_placeholders[key] = st.empty()
                        status_placeholders[key].markdown(
                            f"""
                            <div class="agent-card">
                                <div class="agent-name">
                                    {agent_icons[key]} {name}
                                </div>
                                <div class="agent-status">⏳ Waiting</div>
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
                            progress_bar.progress(completed / total)
                            progress_text.write(
                                f"{completed} of {total} agents completed"
                            )

                        if node_name == "reporter":
                            result = node_output

                if result is None or "report" not in result:
                    raise RuntimeError("Report was not generated.")

                report = result["report"]
                st.success("🎉 Research completed successfully!")
                st.divider()
                st.header("📑 Final Research Report")
                st.markdown(report)

                pdf_output = export_report(report)
                with open(pdf_output, "rb") as report_file:
                    pdf_data = report_file.read()

                st.download_button(
                    label="📥 Download Research Report (PDF)",
                    data=pdf_data,
                    file_name="ResearchAI_Report.pdf",
                    mime="application/pdf",
                )

            except Exception as error:
                st.error("Something went wrong.")
                st.exception(error)

            finally:
                for file_path in [pdf_path, csv_path]:
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)

    st.divider()
    st.caption("ResearchAI | Multi-Agent AI Research Platform")