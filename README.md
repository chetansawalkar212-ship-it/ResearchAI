# ResearchAI — Multi-Agent AI Research Assistant

ResearchAI is an AI-powered research assistant built using Python, LangGraph, LangChain, and Google Gemini. It uses multiple specialized AI agents to research topics, analyze web sources, read PDF documents, process CSV datasets, and generate structured research reports.

## 🚀 Features

- **Multi-Agent Research:** Six specialized AI agents work together through a LangGraph workflow.
- **Web Research:** Searches for relevant online information and collects source details.
- **PDF Analysis:** Upload PDF documents for document analysis.
- **CSV Analysis:** Analyze uploaded CSV datasets.
- **AI Research Reports:** Generate structured reports from combined research findings.
- **Source References:** Include source titles and URLs in generated reports.
- **PDF Export:** Export research reports as PDF files.
- **PDF Chatbot (RAG):** Upload PDFs and ask questions about their content.
- **Chat History:** Store and retrieve chat messages.
- **Research History:** Keep track of recent research activity.
- **Streamlit Interface:** Interactive dashboard and application pages.

## 🧠 Six AI Agents

ResearchAI uses six specialized agents connected through LangGraph.

| Agent | Responsibility |
|---|---|
| Research Agent | Performs initial topic research |
| Web Research Agent | Searches and collects online sources |
| Document Agent | Analyzes uploaded PDF documents |
| Data Agent | Analyzes uploaded CSV files |
| Analyst Agent | Combines and analyzes research findings |
| Report Agent | Generates the final research report |

### Workflow

1. User enters a research topic.
2. Research Agent performs initial research.
3. Web Research Agent gathers online information.
4. Document Agent analyzes an uploaded PDF, if provided.
5. Data Agent analyzes an uploaded CSV, if provided.
6. Analyst Agent combines the available findings.
7. Report Agent generates the final report with source references.

The workflow is orchestrated using LangGraph's StateGraph.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | LLM integration |
| LangGraph | Multi-agent orchestration |
| Google Gemini | AI language model |
| Streamlit | User interface |
| ChromaDB | Vector database |
| Pandas | CSV data analysis |
| PyPDF | PDF processing |
| DuckDuckGo Search | Web research |
| SQLite | Chat and research history |
| Python Dotenv | Environment variable management |

## 🤖 AI Model Configuration

ResearchAI currently uses:

- **Provider:** Google Gemini
- **Model:** `gemini-3.5-flash-lite`
- **Temperature:** `0.3`
- **Integration:** `langchain-google-genai`

The Google API key is loaded securely from the `.env` file.

## 📂 Project Structure

```text
ResearchAI/
│
├── backend/
│   ├── agents/
│   │   ├── analyst_agent.py
│   │   ├── data_agent.py
│   │   ├── document_agent.py
│   │   ├── report_agent.py
│   │   ├── research_agent.py
│   │   └── web_research_agent.py
│   │
│   ├── orchestrator/
│   │   └── graph.py
│   │
│   ├── rag/
│   │   ├── chat_engine.py
│   │   ├── document_processor.py
│   │   ├── embedding_engine.py
│   │   ├── rag_engine.py
│   │   ├── retriever.py
│   │   ├── text_chunker.py
│   │   └── vector_store.py
│   │
│   ├── database.py
│   ├── llm.py
│   └── pdf_exporter.py
│
├── frontend/
│   └── app.py
│
├── data/
│
├── .gitignore
├── requirements.txt
└── README.md
```

The `data/` directory stores local application data and is excluded from Git tracking.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ResearchAI
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure the Google Gemini API key

Create a `.env` file in the project root directory.

Add the following:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace the placeholder with your own Google Gemini API key.

**Important:** Never upload your actual `.env` file or API key to GitHub.

## ▶️ Run ResearchAI

From the project root directory, execute:

```powershell
python -m streamlit run frontend/app.py
```

Streamlit will start the application and provide a local URL in the terminal.

Open that URL in your browser to access ResearchAI.

## 🖥️ Application Pages

### Dashboard

Provides an overview of ResearchAI, quick actions, agent information, and recent research activity.

### About ResearchAI

Provides information about the project and its purpose.

### New Research

Allows users to enter research topics, provide optional PDF and CSV files, and generate AI-powered research reports.

### PDF Chatbot

Allows users to upload PDF documents and ask questions using the Retrieval-Augmented Generation (RAG) pipeline.

## 🔍 Retrieval-Augmented Generation (RAG)

The PDF Chatbot uses a RAG pipeline to answer questions based on uploaded documents.

The pipeline includes:

1. PDF document processing.
2. Text extraction and chunking.
3. Text embeddings.
4. Vector storage using ChromaDB.
5. Relevant document retrieval.
6. AI-generated answers using the retrieved context.

## 🔐 Security

- API credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- Virtual environments and local data are excluded from Git tracking.
- API keys should never be committed to a public repository.

## 🚧 Future Improvements

- Improve research accuracy and source verification.
- Add support for more document and data formats.
- Enhance report customization.
- Improve the user interface and user experience.
- Prepare the application for cloud deployment.
- Add additional research and analysis capabilities.

## 👨‍💻 Project

**ResearchAI — Multi-Agent AI Research Assistant**

Built using Python, LangGraph, LangChain, Google Gemini, Streamlit, and ChromaDB.

---

*An intelligent research assistant designed to simplify research, document analysis, data analysis, and report generation.*