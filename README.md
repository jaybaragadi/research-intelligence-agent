# Research Intelligence Agent

An agentic AI research system for analyzing academic literature,
comparing methodologies and findings, identifying research gaps,
and producing evidence-grounded research insights.

## Initial Research Domain

Large Language Models for Automated Software Test Generation.

The initial research corpus will include papers covering:

- LLM-based unit test generation
- iterative test refinement
- mutation-guided test generation
- coverage-guided generation
- program-analysis-guided generation
- evaluation of LLM-generated tests

## Project Goals

The system will eventually support:

- Research paper ingestion
- Metadata extraction
- Semantic paper search
- Paper summarization
- Multi-paper comparison
- Evidence-backed question answering
- Citation verification
- Research gap analysis
- Literature review generation
- Agentic tool selection

## Planned Architecture

```text
Research Papers
      |
      v
PDF Ingestion
      |
      v
Metadata + Text Extraction
      |
      v
Chunking
      |
      v
Embeddings
      |
      v
Vector Store
      |
      v
Research Agent
      |
      +------------------+
      |        |         |
      v        v         v
    Search   Summarize  Compare
      |        |         |
      +--------+---------+
               |
               v
       Evidence Retrieval
               |
               v
         LLM Synthesis
               |
               v
      Citation Validation
               |
               v
          Final Answer




Setup

Create a virtual environment:

python -m venv .venv

Activate on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the project:

python app.py

Run tests:

pytest
Research Papers

PDF files are not stored in this repository.

Place locally obtained research PDFs in:

data/papers/
Status

Phase 1 — Project foundation.


---

# 22. Your completed Phase 1 structure

You should now have:

```text
research-intelligence-agent/
│
├── .venv/
│
├── data/
│   ├── papers/
│   │   └── .gitkeep
│   │
│   ├── processed/
│   │   └── .gitkeep
│   │
│   └── vector_store/
│       └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   │
│   ├── ingestion/
│   │   └── __init__.py
│   │
│   ├── retrieval/
│   │   └── __init__.py
│   │
│   ├── agents/
│   │   └── __init__.py
│   │
│   ├── tools/
│   │   └── __init__.py
│   │
│   └── analysis/
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_models.py
│
├── .env
├── .env.example
├── .gitignore
├── app.py
├── README.md
└── requirements.txt