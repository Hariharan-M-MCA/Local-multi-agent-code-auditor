🛡️ Privacy-Preserving Multi-Agent Code Auditor

An enterprise-grade, 100% local, and air-gapped repository vulnerability scanning engine. This system utilizes a Retrieval-Augmented Generation (RAG) architecture and an autonomous multi-agent framework to execute semantic code compliance audits safely on consumer hardware without data privacy risks.

🌟 The Core Problem & Value Proposition

In modern enterprise environments (finance, healthcare, defense), developers are strictly prohibited from uploading proprietary code repositories to public cloud APIs (like OpenAI or Anthropic) due to catastrophic data leak risks and compliance regulations.

This project solves that exact bottleneck by establishing a Zero-Cost, Air-Gapped, Local Inference System. It brings advanced agentic intelligence and abstract syntax code analysis directly into the private, disconnected development environment.

✨ Key Features

100% Data Privacy: Operates entirely locally. Zero code or telemetry is broadcasted over the internet.

Hardware Optimized: Engineered to run smoothly on standard consumer hardware (e.g., Intel i5, 16GB RAM) without requiring a dedicated NVIDIA GPU.

Agentic Orchestration: Replaces the traditional "single-prompt" chatbot with a dedicated team of AI personas (Security Auditor, Quality Architect, Lead Manager) that debate and verify findings to eliminate hallucinations.

AST-Aware Code Parsing: Uses Tree-Sitter to understand the actual structural hierarchy of the code (functions, classes) rather than just reading blind text.

Interactive Dashboard: Features a clean, reactive Streamlit web interface for executing scans and exporting compliance reports.

🏗️ System Architecture

[Local Filesystem: *.py] 
       │
       ▼
[LangChain LanguageParser (Python AST via Tree-Sitter)]
       │
       ▼
[RecursiveCharacterTextSplitter (Semantic Chunking)]
       │
       ▼
[Hugging Face all-MiniLM-L6-v2] ──► [In-Memory Chroma Vector DB]
                                                  │
                             (Semantic Proximity) ──┘
                          ┌─────────┴─────────┐
                          ▼                   ▼
            [Senior Security Auditor]   [Code Quality Architect]
                          │                   │
                          └─────────┬─────────┘
                                    ▼
                   [Lead Software Engineering Manager]
                                    │
                                    ▼
                         [Streamlit Web Dashboard]


🧠 Technology Stack

Orchestration Framework: CrewAI

Local Inference Engine: Ollama running qwen2.5-coder:1.5b (INT4 Quantized Small Language Model)

Vector Database (RAG): ChromaDB

Representation Learning: Hugging Face all-MiniLM-L6-v2 (Local Embeddings)

Data Pipeline & AST Parsing: LangChain + Tree-Sitter

Frontend UI: Streamlit

🚀 Installation & Setup

1. Prerequisite: Local AI Engine

Download and install Ollama. Once installed, open your terminal and pull down the highly-optimized coding model:

ollama run qwen2.5-coder:1.5b


(Once the model loads, you can type /bye to exit. Keep the Ollama service running in the background).

2. Clone & Configure Environment

It is highly recommended to use Python 3.12 for ultimate stability.

git clone [https://github.com/YOUR_USERNAME/local-multi-agent-code-auditor.git](https://github.com/YOUR_USERNAME/local-multi-agent-code-auditor.git)
cd local-multi-agent-code-auditor

# Create and activate a virtual environment
python -m venv venv

# Windows Activation:
venv\Scripts\activate
# Mac/Linux Activation:
# source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Launch the Dashboard

streamlit run app_ui.py


The web browser will automatically open the dashboard interface at http://localhost:8501.

📖 Usage Guide

Target Repository: Enter the absolute path of the local directory you wish to audit into the Streamlit interface.

Execute Scan: Click Start Multi-Agent Security Audit.

Monitor Agents: Watch the real-time execution logs as the pipeline parses code syntax, maps vector embeddings, and triggers the CrewAI worker chain.

Review Artifact: Analyze the final Markdown report detailing threat profiles, structural vulnerabilities, and refactored secure code.

Export: Click Download Markdown Report Artifact to save the compliance log locally.

📁 Repository Structure

local-multi-agent-code-auditor/
│
├── app_ui.py            # Streamlit Frontend application (Lazy loading optimized)
├── app.py               # Core Backend script for CLI prototyping and testing
├── vulnerable_code.py   # Test script containing structural injection flaws
├── requirements.txt     # Locked-in environment package dependencies
├── .gitignore           # Git instruction set blocking local caches/DBs
└── README.md            # System operational documentation


🛡️ Enterprise Compliance Profile

Cost of Operation: ₹0.00 (Zero reliance on paid cloud tokens).

Telemetry Protection: Environmental overrides (OTEL_SDK_DISABLED=true) enforce an absolute block on background data collection.

Model Footprint: Operates strictly within a ~1.2 GB RAM footprint, reserving the rest of the system memory for the OS and IDEs.
