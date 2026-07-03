import os
import streamlit as st

st.set_page_config(page_title="Privacy-Preserving Code Auditor", page_icon="🤖", layout="wide")

st.title("Privacy-Preserving Multi-Agent Code Auditor")
st.markdown("### 100% Local & Air-Gapped Repository Vulnerability Scanning Engine")
st.caption("Powered by CrewAI, Ollama (Qwen2.5-Coder), and ChromaDB")
st.sidebar.header("System Settings")
st.sidebar.info("Computing Layer: Local CPU/RAM\n\nAPI Token Costs: ₹0.00\n\nData Privacy: Absolute")

repo_path = st.text_input("📁 Enter target local repository directory path:", value=os.getcwd())

if st.button("Start Multi-Agent Security Audit"):
    if not os.path.exists(repo_path):
        st.error("❌ The specified directory path does not exist. Please check your path and try again.")
    else:
        progress_box = st.status("Initializing Intelligence Subsystems...", expanded=True)
        
        with progress_box:
            st.write("🔌 Loading local AI libraries and model configurations...")
            from pathlib import Path
            from crewai import Agent, Task, Crew, Process, LLM
            from langchain_community.document_loaders.generic import GenericLoader
            from langchain_community.document_loaders.parsers import LanguageParser
            from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma

            os.environ["OPENAI_API_KEY"] = "NA"
            os.environ["OTEL_SDK_DISABLED"] = "true"
            
            st.write("Actively scanning local repository filesystem...")
            loader = GenericLoader.from_filesystem(
                path=repo_path,
                glob="*.py",
                suffixes=[".py"],
                parser=LanguageParser(language=Language.PYTHON, parser_threshold=10)
            )
            raw_documents = loader.load()
            
            if not raw_documents:
                st.error("No Python (.py) files discovered in the selected folder.")
                st.stop()
                
            st.write(f"Found {len(raw_documents)} files. Fragmenting into semantic code blocks...")
            text_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=1000, chunk_overlap=100
            )
            split_docs = text_splitter.split_documents(raw_documents)
            
            st.write(f"Embedding {len(split_docs)} chunks into local Chroma Vector Database via all-MiniLM-L6-v2...")
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_store = Chroma.from_documents(split_docs, embedding_model)
            
            st.write("Running semantic proximity search for high-risk exploit vulnerabilities...")
            query_focus = "vulnerable sql injection execution parameter connection f-string input"
            relevant_chunks = vector_store.similarity_search(query_focus, k=3)
            extracted_context = "\n\n--- Code Chunk ---\n\n".join([doc.page_content for doc in relevant_chunks])
            
            st.write(" Establishing secure pipe to local Ollama inference engine...")
            local_llm = LLM(model="ollama/qwen2.5-coder:1.5b", base_url="http://localhost:11434")
            
            st.write("Summoning Agentic Workforces: Senior Security Auditor & Lead Manager...")
            security_auditor = Agent(
                role='Senior Security Auditor',
                goal='Analyze high-risk code segments and extract explicit security flaws.',
                backstory='You are a hard-nosed application security auditor who reviews parsed vector context for code level flaws.',
                verbose=True,
                allow_delegation=False,
                llm=local_llm
            )
            
            engineering_manager = Agent(
                role='Lead Software Engineering Manager',
                goal='Synthesize raw code analysis into a flawless executive markdown document.',
                backstory='You compile raw engine logs into immaculate, comprehensive markdown reports. You never use placeholders.',
                verbose=True,
                allow_delegation=False,
                llm=local_llm
            )
            
            security_task = Task(
                description=f"Analyze these high-risk code segments retrieved from the vector store and list their exploits:\n\n{extracted_context}",
                expected_output="A list highlighting security flaws and specific attack vectors.",
                agent=security_auditor
            )
            
            manager_task = Task(
                description="Compile the security findings into a comprehensive final document.",
                expected_output="A fully populated Markdown report detailing the exact vulnerabilities found and providing a fully corrected, parameterized code block.",
                agent=engineering_manager
            )
            
            rag_crew = Crew(
                agents=[security_auditor, engineering_manager],
                tasks=[security_task, manager_task],
                process=Process.sequential
            )
            
            st.write(" Executing multi-agent neural synthesis. Running calculations...")
            final_report = rag_crew.kickoff()
            progress_box.update(label=" Audit Cycle Completed Successfully!", state="complete", expanded=False)

        st.success("Final Audit Report Generated!")
        st.markdown(final_report)
        
        st.download_button(
            label="📥 Download Markdown Report Artifact",
            data=str(final_report),
            file_name="security_compliance_report.md",
            mime="text/markdown"
        )