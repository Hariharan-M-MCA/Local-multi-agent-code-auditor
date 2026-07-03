import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OTEL_SDK_DISABLED"] = "true"

print("Parsing local repository files...")


loader = GenericLoader.from_filesystem(
    path=".",
    glob="*.py",  # Swapped to global scanning to read ALL python files in the folder!
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=10)
)
raw_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, 
    chunk_size=1000, 
    chunk_overlap=100
)
split_docs = text_splitter.split_documents(raw_documents)

print(f"Generated {len(split_docs)} semantic code chunks. Embedding into local Vector DB...")

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Chroma.from_documents(split_docs, embedding_model)

query_focus = "vulnerable sql injection execution parameter connection f-string input"
relevant_chunks = vector_store.similarity_search(query_focus, k=3)
extracted_context = "\n\n--- Code Chunk ---\n\n".join([doc.page_content for doc in relevant_chunks])

print("Connecting to local Qwen model...")

local_llm = LLM(
    model="ollama/qwen2.5-coder:1.5b",
    base_url="http://localhost:11434"
)

security_auditor = Agent(
    role='Senior Security Auditor',
    goal='Identify vulnerabilities and security flaws in the provided code snippets.',
    backstory='You are an aggressive application security expert. You scan raw code vectors exclusively for active software exploits.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

engineering_manager = Agent(
    role='Lead Software Engineering Manager',
    goal='Generate a comprehensive, fully written markdown security compliance report.',
    backstory='You compile raw security reviews into client-ready Markdown code compliance summaries. You never write incomplete outlines or placeholder summaries.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)


security_task = Task(
    description=f"Analyze these high-risk code segments retrieved from the vector store and list their exploits:\n\n{extracted_context}",
    expected_output="A bulleted list highlighting security flaws, dangerous entry points, and specific attack vectors found.",
    agent=security_auditor
)

manager_task = Task(
    description="Compile the security findings into a comprehensive final review document.",
    expected_output="A fully populated Markdown report detailing the exact vulnerabilities found and providing a fully corrected, parameterized code block.",
    agent=engineering_manager
)


rag_crew = Crew(
    agents=[security_auditor, engineering_manager],
    tasks=[security_task, manager_task],
    process=Process.sequential
)

print("Starting RAG-driven automated system audit...")
result = rag_crew.kickoff()

print("\n=======================================================")
print("FINAL RAG EXECUTIVE AUDIT REPORT:")
print("=======================================================")
print(result)