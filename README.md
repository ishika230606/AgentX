# AgentX
An autonomous multi-agent AI student assistant using Python, Streamlit, Ollama, and Qwen 2.5 3B for task planning, PDF analysis, and automated report generation.
# 🤖 AgentX – Autonomous AI Student Assistant

AgentX is an AI-powered autonomous student assistant developed using Python, Streamlit, Ollama, and Qwen 2.5 3B. It uses a multi-agent architecture to automate task planning, document analysis, research, report writing, and reviewing.

The system consists of four specialized AI agents that work together to convert user instructions into structured academic reports. It runs locally using Ollama, without requiring paid AI APIs.

## ✨ Features

- 🧭 **Planner Agent:** Breaks user tasks into 4–6 organized subtasks.
- 🔎 **Research Agent:** Extracts relevant information from uploaded PDF documents or uses general model knowledge.
- ✍️ **Writer Agent:** Generates structured academic reports based on research results.
- 🔍 **Reviewer Agent:** Reviews and improves reports to ensure requested sections are covered.
- 📄 **PDF Document Analysis:** Upload PDF documents for context-based research.
- 📥 **DOCX Report Generation:** Download the final generated report as a Word document.
- ⚙️ **Customizable Settings:** Adjust AI model, creativity, and PDF passage selection.
- 🔒 **Local AI Processing:** Uses Ollama to run the language model locally without paid AI APIs.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Ollama | Local LLM execution |
| Qwen 2.5 3B | Language model |
| Requests | Communication with Ollama API |
| PyPDF | PDF text extraction |
| python-docx | Word document generation |

## 🧠 Multi-Agent Architecture

AgentX follows a sequential multi-agent workflow.

```text
       USER INPUT
           |
           v
     PLANNER AGENT
           |
           v
    RESEARCH AGENT
           |
           v
     WRITER AGENT
           |
           v
    REVIEWER AGENT
           |
           v
     FINAL REPORT
           |
           v
      DOCX DOWNLOAD
```

### Agent Responsibilities

**1. Planner Agent**
- Understands the user's task.
- Divides the task into smaller steps.
- Creates an ordered execution plan.

**2. Research Agent**
- Reads uploaded PDF documents.
- Splits extracted text into smaller chunks.
- Selects relevant passages using keyword matching.
- Generates research notes.

**3. Writer Agent**
- Uses the research notes.
- Generates a structured academic report.
- Organizes information using appropriate headings.

**4. Reviewer Agent**
- Checks the generated report.
- Identifies missing sections.
- Produces an improved final report.

## 📂 Project Structure

```text
AgentX/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── output/
    └── .gitkeep
```

## 💻 Installation and Setup

### Prerequisites

- Python 3.10 or newer
- Git
- Ollama installed on your computer
- Sufficient system memory to run Qwen 2.5 3B

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AgentX.git
```

Navigate to the project directory:

```bash
cd AgentX
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install the Ollama Model

Download and install Ollama:

https://ollama.com/

Pull the Qwen 2.5 3B model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running locally.

### Step 5: Run the Application

Execute the following command:

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🚀 How to Use AgentX

1. Open the AgentX application.
2. Enter your task in the task input area.
3. Optionally upload a PDF document.
4. Click **Execute AI Agents**.
5. The Planner Agent creates an execution plan.
6. The Research Agent gathers relevant information.
7. The Writer Agent prepares the report.
8. The Reviewer Agent checks and improves the report.
9. View the final report and download it in DOCX format.

## ⚙️ Configuration

The application provides customizable settings:

- **Ollama Model:** Select the local model name.
- **Ollama URL:** Configure the local Ollama API endpoint.
- **Writer Creativity:** Adjust the generation temperature.
- **PDF Passages:** Select the number of relevant PDF passages used during research.

Default model:

```text
qwen2.5:3b
```

Default Ollama API:

```text
http://localhost:11434/api/generate
```

## 🔮 Future Enhancements

- Add support for multiple document formats.
- Implement advanced semantic document retrieval.
- Introduce parallel agent execution.
- Add source citation and reference generation.
- Integrate additional specialized AI agents.
- Improve task memory and conversation history.

## 🎯 Project Objective

The primary objective of AgentX is to demonstrate how Agentic AI can automate complex academic tasks through collaboration between specialized AI agents. The project provides a cost-effective, locally executable prototype for intelligent task automation and academic report generation.

## 👩‍💻 Author

Ishika

AI & Machine Learning Student

GitHub: https://github.com/ishika230606

## 📜 License

This project is developed for educational and academic purposes. No license has been specified yet.
