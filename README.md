# Research Intelligence Agent

[![CI](https://github.com/jaybaragadi/research-intelligence-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/jaybaragadi/research-intelligence-agent/actions/workflows/ci.yml)

An **evidence-grounded AI research system** for analyzing academic literature, answering research questions, comparing methodologies, identifying research gaps, and generating citation-traceable literature reviews.

The current corpus focuses on:

> **Large Language Models for Automated Software Test Generation**

The project was designed as a research-intelligence pipeline rather than a generic chatbot. Its core principle is simple:

> **Generated research claims should be traceable to retrieved evidence.**

## Live Demo

**Streamlit Application:**  
https://research-intelligence-agent-z6eq5bn8vfnznwmpfgmtw5.streamlit.app/

### Research Intelligence Dashboard

![Research Intelligence Agent Home](docs/screenshots/research-intelligence-home.png)

### Evidence-Grounded Research Q&A

![Evidence-Grounded Research Q&A](docs/screenshots/research-qa-evidence.png)

---

## What It Does

The application supports six research workflows:

| Capability | Description |
|---|---|
| **Research Q&A** | Answers research questions using retrieved evidence with claim-level provenance |
| **Paper Search** | Searches the indexed research corpus using semantic retrieval |
| **Compare Papers** | Compares research approaches across structured dimensions |
| **Research Gap Analysis** | Identifies evidence-supported limitations and corpus-level gaps |
| **Literature Review** | Produces structured, citation-traceable research reviews |
| **Evidence Validation** | Validates that generated claims reference retrieved evidence |

The system currently indexes **10 research papers** covering LLM-based and hybrid approaches to automated software test generation.

---

## Architecture

```text
Research Papers
      │
      ▼
PDF Ingestion
      │
      ▼
Metadata + Research Structure Extraction
      │
      ▼
Structure-Aware Chunking
      │
      ▼
Sentence Transformer Embeddings
      │
      ▼
FAISS Vector Index
      │
      ▼
Hybrid Retrieval
      │
      ├───────────────┐
      ▼               ▼
Evidence Package   Comparative Analysis
      │               │
      ▼               ▼
Grounded Q&A      Research Gap Analysis
                      │
                      ▼
               Literature Review
                      │
                      ▼
            Citation / Provenance Validation
```

The application preserves provenance including:

```text
Paper → Page → Section → Chunk → Evidence → Claim
```

This makes generated findings auditable instead of returning unsupported research summaries.

---

## Evidence-Grounded Generation

The default workflow intentionally uses a **deterministic grounded generator** rather than requiring an external LLM.

For each research request:

1. Relevant chunks are retrieved from FAISS.
2. Retrieved evidence is packaged with provenance.
3. Research claims are generated from that evidence.
4. Each claim references specific evidence IDs.
5. The backend validates those references before returning the result.

This provides a reproducible baseline and makes retrieval and grounding failures easier to detect.

An optional LLM synthesis path can be enabled separately while preserving the deterministic baseline.

---

## Research Analysis

### Paper Comparison

Papers can be compared across research dimensions including:

- generation strategy
- feedback signal
- iteration strategy
- quality objective
- evaluation method
- reported limitations

Comparison findings are linked back to supporting evidence.

### Research Gap Analysis

Gap detection deliberately avoids the unsafe assumption:

> `No retrieved evidence = no research exists`

Instead, findings are categorized as:

- **Explicit Gap** — directly supported by paper evidence
- **Corpus Imbalance** — uneven representation within the indexed corpus
- **Insufficient Evidence** — available evidence is not strong enough for a broader conclusion

All findings are scoped to the indexed corpus rather than presented as universal claims about the entire literature.

### Literature Review Generation

The system produces structured reviews covering:

1. Introduction
2. Research Landscape
3. Test Generation Strategies
4. Feedback and Iterative Refinement
5. Test Quality and Evaluation
6. Limitations and Research Gaps
7. Future Research Directions
8. Conclusion

Findings retain evidence and citation provenance throughout the review.

---

## Retrieval Evaluation

A frozen baseline and two cross-encoder reranking strategies were evaluated using the same benchmark.

| Retrieval Strategy | Hit@1 | Hit@3 | Hit@5 | MRR | Recall@3 | Recall@5 | Recall@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Frozen Baseline | 40% | 40% | 60% | 0.5119 | 24.44% | 48.89% | 82.22% |
| Pure Cross-Encoder | 0% | 60% | 60% | 0.2841 | 31.11% | 42.22% | 88.89% |
| **50/50 Fused Reranking** | **40%** | **60%** | **80%** | **0.5289** | **44.44%** | **55.56%** | **88.89%** |

### Key Finding

Pure cross-encoder reranking improved some deeper-recall metrics but significantly degraded early ranking.

A fixed **50/50 fusion of the original retrieval score and cross-encoder score** produced the strongest aggregate experimental result:

- Hit@5 improved from **60% → 80%**
- Recall@3 improved from **24.44% → 44.44%**
- Recall@5 improved from **48.89% → 55.56%**
- Recall@10 improved from **82.22% → 88.89%**
- MRR improved from **0.5119 → 0.5289**

The fusion weight was intentionally **not tuned on the benchmark** to avoid optimizing against the evaluation set.

> **Evaluation caveat:** the retrieval benchmark currently contains five research questions. These results demonstrate behavior within this project benchmark and should not be interpreted as general retrieval accuracy.

Full experiment details are available in:

```text
evaluation/retrieval_reranking_experiment.md
```

---

## Grounding & System Evaluation

Evaluation extends beyond retrieval and covers grounding, comparison, gap analysis, literature review generation, and end-to-end execution.

| Evaluation Area | Result |
|---|---:|
| Claim–Evidence Coverage | 100% |
| Evidence Reference Integrity | 100% |
| Provenance Completeness | 100% |
| Comparison Structural Validation | 100% |
| Gap Analysis Structural Validation | 100% |
| Literature Review Structural Validation | 100% |
| End-to-End Structural Validation | 100% |

These metrics measure **structural grounding and provenance integrity**. They should not be interpreted as 100% semantic correctness or general research accuracy.

The evaluation framework is intentionally separated from the production pipeline so retrieval and generation experiments can be compared against stable baselines.

---

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python 3.11 |
| UI | Streamlit |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS CPU |
| Reranking | Cross-Encoder |
| Data Models | Pydantic |
| PDF Processing | PyPDF |
| Numerical Processing | NumPy |
| Testing | Pytest |
| Code Quality | Ruff + Black |
| CI | GitHub Actions |
| Containerization | Docker |
| Deployment | Streamlit Community Cloud |

The default application does **not require a paid LLM API**.

---

## Project Structure

```text
research-intelligence-agent/
│
├── app.py
├── README.md
├── ARCHITECTURE.md
├── Dockerfile
├── .dockerignore
├── requirements.txt
│
├── data/
│   ├── papers/
│   └── vector_store/
│
├── evaluation/
│   └── results/
│
├── reports/
├── scripts/
│
├── src/
│   ├── agents/
│   ├── analysis/
│   ├── chunking/
│   ├── evaluation/
│   ├── generation/
│   ├── ingestion/
│   ├── metadata/
│   ├── retrieval/
│   ├── tools/
│   └── ui/
│
└── tests/
```

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for additional implementation details.

---

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jaybaragadi/research-intelligence-agent.git
cd research-intelligence-agent
```

### 2. Create a Python 3.11 environment

Windows:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Run with Docker

Build the image:

```bash
docker build -t research-intelligence-agent:local .
```

Run the container:

```bash
docker run --rm -p 8501:8501 \
  --name research-intelligence-agent \
  research-intelligence-agent:local
```

Open:

```text
http://localhost:8501
```

Verify container health:

```bash
docker inspect --format='{{.State.Health.Status}}' research-intelligence-agent
```

Expected:

```text
healthy
```

The Docker image packages the runtime application and vector-store artifacts required for retrieval.

---

## Testing & CI

Run the test suite:

```bash
pytest
```

Run code-quality checks:

```bash
python -m ruff check .
python -m black --check .
```

GitHub Actions automatically runs the reproducible CI suite along with Ruff and Black checks on repository changes.

Some real-corpus integration validation is intentionally maintained separately from the clean CI suite.

---

## Engineering Decisions

A few design decisions were intentional:

**Deterministic baseline before LLM generation**  
Provides reproducible behavior and makes retrieval and grounding defects observable.

**Evidence-first generation**  
Claims are derived from retrieved evidence rather than allowing unrestricted generation.

**Provenance throughout the pipeline**  
Paper, page, section, chunk, evidence, and claim relationships remain traceable.

**No automatic “missing evidence = research gap” inference**  
Gap analysis distinguishes insufficient evidence from supported research limitations.

**Frozen retrieval baseline during reranking experiments**  
Prevents experimental changes from silently altering benchmark comparisons.

**No benchmark-specific reranker weight tuning**  
The 50/50 fusion was fixed rather than optimized against the same five evaluation questions.

---

## Current Limitations & Next Steps

The project is intentionally scoped as a research prototype rather than a claim of production-scale research coverage.

Future work includes:

- expanding the research corpus and held-out benchmark;
- human relevance judgments for retrieval evaluation;
- semantic entailment evaluation in addition to structural grounding;
- larger-scale cross-encoder reranking experiments;
- improved citation presentation;
- evaluation of optional LLM synthesis against the deterministic baseline.

---

## Why This Project

This project explores a practical question in applied AI:

> **How can a RAG system produce useful research analysis while keeping its conclusions traceable to evidence?**

The result combines retrieval engineering, evidence grounding, research analysis, evaluation, experimentation, CI, cloud deployment, and containerization in one end-to-end system.

---

## Repository

**GitHub:**  
https://github.com/jaybaragadi/research-intelligence-agent

**Live Application:**  
https://research-intelligence-agent-z6eq5bn8vfnznwmpfgmtw5.streamlit.app/