# Lab 20: Multi-Agent Research System

This repository implements a production-grade multi-agent research workflow built with LangGraph, utilizing OpenAI and Tavily. The system compares a single-agent baseline against a sophisticated multi-agent pipeline (Supervisor, Researcher, Analyst, Writer, and Critic) capable of iterating over search extraction, analysis, and synthesis.

---

## 1. Installation & Setup

Ensure you have Python 3.10+ installed.

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # Linux / macOS
   source .venv/bin/activate  
   
   # Windows
   .venv\Scripts\activate
   ```

2. **Install project dependencies:**
   ```bash
   # Install the project along with development and LLM dependencies
   pip install -e ".[dev,llm]"
   ```

3. **Configure Environment Variables:**
   Copy the provided `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your API keys:
   - `OPENAI_API_KEY`: Required for the LLM client.
   - `TAVILY_API_KEY`: Optional but recommended for live search. If omitted, the system falls back to a local mock search.
   - `LANGSMITH_API_KEY`: Optional. Include this to automatically export rich traces of your workflow to LangSmith.

---

## 2. Running the Project

You can interact with the project using the unified CLI. 

### Single-Agent Baseline
To run the minimal single-agent baseline implementation:
```bash
make run-baseline
# Alternatively:
python -m multi_agent_research_lab.cli baseline --query "Research GraphRAG state-of-the-art"
```

### Multi-Agent Workflow
To run the full multi-agent orchestrated graph (Supervisor -> Researcher -> Analyst -> Writer -> Critic):
```bash
make run-multi
# Alternatively:
python -m multi_agent_research_lab.cli multi-agent --query "Research GraphRAG state-of-the-art"
```

### Output Results
- **Console Output:** The final synthesized answer and evaluation metrics (Latency, Quality, Cost, Iterations) will be beautifully formatted and printed directly to standard output (stdout) via the terminal.
- **LangSmith Tracing:** If you provided a `LANGSMITH_API_KEY` in your `.env`, full nested traces (including spans for each agent node) are automatically captured and uploaded to your LangSmith dashboard.

---

## 3. Testing and Code Quality

This project enforces strict typing and linting to maintain a clean codebase. Use the following `make` commands:

- **Run Unit Tests:**
  ```bash
  make test
  # Note: 4/4 passing tests are expected.
  ```

- **Run Linters and Formatters:**
  ```bash
  make lint
  make typecheck
  ```

---

## 4. Documentation & Reports

The project requires specific deliverables which have been completed and are located in the following directories:

- **Benchmark & Report:** 
  You can find the comprehensive report comparing the baseline with the multi-agent system (including latency, cost analysis, and failure mode explanations) located at:
   `reports/benchmark_report.md` and 
  LangSmith trace: 
  `reports\LangSmith_trace.jpeg`

- **Design Document:** 
  The detailed multi-agent system architecture and agent roles are documented at:
   `docs/design_template.md`

- **Exit Ticket & Lab Guidelines:** 
  The exit ticket answers and general lab instructions are located at:
   `docs/lab_guide.md`
