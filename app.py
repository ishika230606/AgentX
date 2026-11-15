import os
import re
import json
from datetime import datetime

import requests
import streamlit as st
from pypdf import PdfReader
from docx import Document

# ---------------- CONFIGURATION ----------------
st.set_page_config(page_title="AgentX - AI Student Assistant", page_icon="🤖", layout="wide")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------- AI MODEL CONNECTION ----------------
def ask_ai(prompt: str, temperature: float = 0.3) -> str:
    """Send a prompt to the local Ollama model and return its text response."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=600,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot reach Ollama. Make sure the Ollama app is running."
    except Exception as e:
        return f"ERROR: {e}"


# ---------------- DOCUMENT READING TOOL ----------------
def read_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file."""
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def chunk_text(text: str, size: int = 1500) -> list:
    """Split long text into chunks so the model can handle it."""
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i + size])
    return chunks


def select_relevant_chunks(task: str, chunks: list, top_k: int = 4) -> list:
    """Simple keyword-overlap ranking to pick the most relevant passages."""
    words = set(re.findall(r"\w+", task.lower()))
    words = {w for w in words if len(w) > 3}
    scored = []
    for chunk in chunks:
        chunk_words = set(re.findall(r"\w+", chunk.lower()))
        score = len(words & chunk_words)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]


# ---------------- AGENTS ----------------
def planner_agent(task: str) -> list:
    """Split the user's task into a list of subtasks."""
    prompt = f"""You are a planning agent. Break the following task into 4 to 6 short,
ordered subtasks. Respond ONLY with a JSON list of strings.

Task: {task}"""
    raw = ask_ai(prompt, temperature=0.2)
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if match:
        try:
            plan = json.loads(match.group(0))
            if isinstance(plan, list) and plan:
                return [str(p) for p in plan]
        except json.JSONDecodeError:
            pass
    # Fallback plan if the model's JSON is invalid
    return ["Understand the task", "Gather relevant information",
            "Write the report", "Review and improve the report"]


def researcher_agent(task: str, document_text: str) -> str:
    """Summarise relevant information, from the PDF if one was uploaded."""
    if document_text:
        chunks = chunk_text(document_text)
        relevant = select_relevant_chunks(task, chunks)
        context = "\n\n".join(relevant)
        prompt = f"""You are a research agent. Using ONLY the passages below from the
uploaded document, extract the key information relevant to the task.
Do not invent facts.

Task: {task}

Passages:
{context}"""
    else:
        prompt = f"""You are a research agent. Summarise the key facts relevant to this task
from general knowledge. Do not invent citations.

Task: {task}"""
    return ask_ai(prompt, temperature=0.3)


def writer_agent(task: str, research: str) -> str:
    """Write the report based on the task and the research notes."""
    prompt = f"""You are a writer agent. Write a clear, well-structured academic report
for this task. Use headings for each requested section.

Task: {task}

Research notes:
{research}"""
    return ask_ai(prompt, temperature=0.5)


def reviewer_agent(task: str, report: str) -> str:
    """Check the report for missing sections and return an improved version."""
    prompt = f"""You are a reviewer agent. Check whether the report below covers every
section the task asks for. If any section is missing, add it. Return the complete
improved report only.

Task: {task}

Report:
{report}"""
    return ask_ai(prompt, temperature=0.3)


# ---------------- REPORT TOOL ----------------
def save_docx(title: str, content: str) -> str:
    """Save the report as a DOCX file and return its path."""
    doc = Document()
    doc.add_heading(title, level=0)
    for paragraph in content.split("\n"):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"AgentX_Report_{timestamp}.docx")
    doc.save(path)
    return path


# ---------------- DASHBOARD ----------------
st.title("🤖 AgentX – Autonomous AI Student Assistant")
st.caption("Local multi-agent prototype using Ollama + Qwen 2.5 3B")

task = st.text_area(
    "Enter your task",
    height=150,
    placeholder="Example: Prepare a report on Agentic AI. Include Introduction, Architecture, Advantages and Conclusion.",
)
uploaded = st.file_uploader("Upload a PDF (optional)", type=["pdf"])

if st.button("Execute AI Agents"):
    if not task.strip():
        st.warning("Please enter a task first.")
    else:
        document_text = ""
        if uploaded is not None:
            with st.spinner("Reading PDF..."):
                document_text = read_pdf(uploaded)
            st.info(f"Extracted {len(document_text)} characters from the PDF.")

        log = st.container()

        with st.spinner("Planner Agent is creating a plan..."):
            plan = planner_agent(task)
        log.subheader("1. Planner Agent")
        for i, step in enumerate(plan, 1):
            log.write(f"{i}. {step}")

        with st.spinner("Research Agent is gathering information..."):
            research = researcher_agent(task, document_text)
        log.subheader("2. Research Agent")
        log.write(research)

        with st.spinner("Writer Agent is drafting the report..."):
            draft = writer_agent(task, research)
        log.subheader("3. Writer Agent")
        log.write(draft)

        with st.spinner("Reviewer Agent is checking the report..."):
            final_report = reviewer_agent(task, draft)
        log.subheader("4. Reviewer Agent")
        log.write(final_report)

        if final_report.startswith("ERROR"):
            st.error(final_report)
        else:
            docx_path = save_docx("AgentX Report", final_report)
            st.success(f"Report saved to {docx_path}")
            with open(docx_path, "rb") as f:
                st.download_button(
                    "Download DOCX report",
                    data=f,
                    file_name=os.path.basename(docx_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
