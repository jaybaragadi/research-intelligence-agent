# Research Intelligence Agent — Architecture

## 1. Architecture Overview

Research Intelligence Agent is an evidence-grounded research analysis system designed for academic literature.

The current research domain is:

> Large Language Models for Automated Software Test Generation

The system is designed around one core principle:

> Research conclusions should remain traceable to the evidence used to produce them.

Rather than treating the research corpus as a collection of documents for generic question answering, the project separates ingestion, retrieval, evidence selection, analysis, validation, and presentation into distinct layers.

The current implementation runs locally and does not require a paid LLM API.

---

## 2. High-Level Architecture

```text
                         ┌──────────────────────┐
                         │   Research Papers    │
                         │      PDF Corpus      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │       PDF Ingestion        │
                     │                            │
                     │  - page text extraction    │
                     │  - page provenance         │
                     │  - document identity       │
                     └─────────────┬──────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Metadata / Research Structure│
                    │                              │
                    │ - title / paper metadata     │
                    │ - abstract extraction        │
                    │ - research signals           │
                    │ - section identification     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   Structure-Aware Chunking   │
                    │                              │
                    │ - section-aware boundaries   │
                    │ - paper provenance           │
                    │ - page provenance            │
                    │ - stable chunk IDs            │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   Embeddings + FAISS Index   │
                    │                              │
                    │ Sentence Transformers        │
                    │ FAISS IndexFlatIP            │
                    │ normalized vectors           │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      Hybrid Retrieval        │
                    │                              │
                    │ - semantic similarity        │
                    │ - lexical relevance          │
                    │ - paper filtering            │
                    │ - ranking                    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
            ┌────────────────────────────────────────────────┐
            │                 Research Tools                 │
            │                                                │
            │ Search │ Summarize │ Compare │ Evidence │ Cite │
            └──────────────────────┬─────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     Research Orchestration   │
                    │                              │
                    │ deterministic intent routing │
                    │ and tool/service selection   │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
   ┌───────────────────┐ ┌──────────────────┐ ┌────────────────────┐
   │ Grounded Research │ │ Comparative      │ │ Research-Gap       │
   │ Q&A               │ │ Analysis         │ │ Analysis           │
   └─────────┬─────────┘ └────────┬─────────┘ └─────────┬──────────┘
             │                    │                     │
             └────────────────────┼─────────────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │ Literature Review      │
                      │ Generation             │
                      │                        │
                      │ 8-section synthesis    │
                      │ evidence-grounded      │
                      └───────────┬────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │ Validation + Provenance│
                      │                        │
                      │ claim → evidence       │
                      │ evidence → paper       │
                      │ evidence → page        │
                      │ citations              │
                      └───────────┬────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │     Streamlit UI       │
                      │                        │
                      │ Research Q&A           │
                      │ Paper Search           │
                      │ Compare Papers         │
                      │ Research Gaps          │
                      │ Literature Review      │
                      └───────────┬────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │ Evaluation Framework   │
                      │                        │
                      │ Retrieval              │
                      │ Grounding              │
                      │ Comparison             │
                      │ Gap Analysis           │
                      │ Literature Review      │
                      │ End-to-End             │
                      └────────────────────────┘
```

---

## 3. Architectural Principles

### 3.1 Evidence First

The system does not generate research conclusions independently of retrieved source material.

Research outputs are built from evidence objects containing provenance such as:

```text
paper_id
page_number
section
chunk_id / evidence_id
evidence text
citation
```

This allows downstream outputs to remain traceable to the indexed papers.

---

### 3.2 Retrieval and Analysis Are Separate

Retrieval answers:

> Which passages appear relevant?

Analysis answers:

> What can safely be concluded from those passages?

Keeping these responsibilities separate makes it possible to measure retrieval weaknesses independently from grounding or synthesis behavior.

This distinction became important during evaluation: structural grounding remained strong even when retrieval did not always return every expected paper.

---

### 3.3 Missing Evidence Is Not Automatically a Research Gap

The research-gap architecture intentionally avoids the inference:

```text
No retrieved evidence
        ↓
Research does not exist
```

Instead, the system distinguishes among:

```text
Explicitly supported research limitations
Corpus-level coverage imbalance
Insufficient evidence in the indexed corpus
```

Research-gap claims therefore remain scoped to the indexed corpus.

---

### 3.4 Human-Interpretable Intermediate Objects

Major stages produce structured objects rather than immediately generating free-form prose.

Examples include:

```text
GroundedAnswer
ComparativeAnalysis
ResearchGapAnalysis
LiteratureReview
```

These contain claims, findings, evidence IDs, paper IDs, dimensions, validation information, and citations.

This makes the system easier to:

- test;
- inspect;
- validate;
- debug;
- evaluate;
- present in the UI.

---

### 3.5 Deterministic Validation

The current system uses deterministic analysis and validation logic.

It does not require an external paid language model to decide whether an evidence reference exists or whether provenance is present.

Examples of validation include:

```text
claim evidence references exist
finding evidence references exist
paper references are in scope
page provenance exists
required review sections exist
citation references remain traceable
```

---

## 4. Data Processing Layer

### 4.1 PDF Ingestion

Source papers are stored locally under:

```text
data/papers/
```

The ingestion layer extracts text while preserving page-level provenance.

Conceptually:

```text
PDF
 ↓
Paper
 ↓
Pages
 ↓
Page text + paper ID + page number
```

Page provenance is retained because downstream evidence must be traceable back to its location in the original paper.

---

### 4.2 Metadata and Research Structure

After ingestion, the system extracts research-oriented metadata and document structure.

This includes information such as:

```text
paper identity
title
abstract
sections
research-related signals
```

Metadata extraction is separated from retrieval so the system can use document structure during chunking and downstream research analysis.

---

## 5. Structure-Aware Chunking

The system does not treat every paper as an undifferentiated block of text.

Chunks retain research structure whenever possible:

```text
paper
  ↓
section
  ↓
page
  ↓
chunk
```

Each chunk receives a stable identifier and provenance metadata.

Example conceptually:

```text
03_mutap_chunk_0085
```

A chunk can therefore be traced back through:

```text
chunk
  → paper
  → page
  → section
```

This provenance becomes important for citation generation, comparison, gap analysis, and literature-review synthesis.

---

## 6. Retrieval Layer

### 6.1 Local Embeddings

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to generate local embeddings.

No external embedding API is required.

---

### 6.2 FAISS Vector Store

Embeddings are indexed using FAISS.

The current vector index uses:

```text
IndexFlatIP
```

with normalized vectors so inner-product similarity can be used for semantic ranking.

---

### 6.3 Hybrid Retrieval

The retrieval pipeline combines semantic and lexical relevance.

Conceptually:

```text
User Query
    │
    ├── Semantic similarity
    │
    └── Lexical relevance
             │
             ▼
        Hybrid ranking
             │
             ▼
      Ranked evidence chunks
```

Retrieval can also restrict results to selected papers when required by downstream analysis.

---

## 7. Research Tool Layer

The tool layer provides reusable research operations over the indexed corpus.

Capabilities include:

```text
Search Papers
Summarize Paper
Compare Papers
Retrieve Evidence
Generate Citations
```

These tools isolate reusable corpus operations from higher-level research workflows.

This prevents each analysis service from reimplementing retrieval logic.

---

## 8. Research Orchestration

The agent layer performs deterministic intent routing and orchestration.

Conceptually:

```text
User Request
     ↓
Intent Router
     ↓
Research Agent
     ↓
Appropriate research tools
```

The orchestration layer decides which capability should handle a request while keeping retrieval and analysis logic in their dedicated services.

The current architecture does not depend on an external agent framework.

---

## 9. Evidence-Grounded Research Q&A

The grounded answer pipeline follows:

```text
Research Question
       ↓
Evidence Retrieval
       ↓
Evidence Package
       ↓
Claim Generation
       ↓
Claim → Evidence Mapping
       ↓
Grounding Validation
       ↓
Grounded Answer
```

The primary service is:

```python
GroundedAnswerService
```

A grounded answer contains:

```text
query
answer text
claims
evidence
validation result
```

Each generated claim contains explicit supporting evidence IDs.

This makes it possible to verify that a claim does not refer to nonexistent evidence.

---

## 10. Comparative Research Analysis

Comparative analysis operates on a selected set of papers.

Primary service:

```python
ComparativeAnalysisService
```

The analysis organizes evidence using dimensions such as:

```text
generation strategy
feedback signal
iteration strategy
quality objective
evaluation method
limitations
```

The pipeline is conceptually:

```text
Selected Papers
      ↓
Evidence Retrieval
      ↓
Dimension Classification
      ↓
Paper Profiles
      ↓
Comparison Matrix
      ↓
Evidence-Backed Findings
```

The system does not force every cell in the comparison matrix to contain a result.

If supporting evidence is unavailable, the cell may remain unpopulated rather than inventing a comparison.

---

## 11. Research-Gap Analysis

Primary service:

```python
ResearchGapAnalysisService
```

The gap pipeline analyzes:

```text
explicit limitations
future-work statements
unresolved problems
underexplored areas
dimension coverage
```

Conceptually:

```text
Selected Corpus
      ↓
Gap Signal Retrieval
      ↓
Signal Classification
      ↓
Dimension Coverage
      ↓
Gap Candidates
      ↓
Gap Validation
```

Gap types include:

```text
explicit
corpus imbalance
insufficient evidence
```

The system does not claim that the absence of evidence from the indexed corpus proves absence from global research literature.

---

## 12. Literature Review Generation

Primary service:

```python
LiteratureReviewService
```

Literature-review generation combines validated research evidence from earlier analytical layers.

The review uses eight sections:

```text
1. Introduction
2. Research Landscape
3. Test Generation Strategies
4. Feedback and Iterative Refinement
5. Test Quality and Evaluation
6. Limitations and Research Gaps
7. Future Research Directions
8. Conclusion
```

Conceptually:

```text
Research Question
      │
      ├── Comparative Analysis
      │
      ├── Research-Gap Analysis
      │
      └── Validated Evidence
                    │
                    ▼
          Literature Review Planner
                    │
                    ▼
             Review Findings
                    │
                    ▼
              Review Sections
                    │
                    ▼
            Citation Validation
                    │
                    ▼
       Evidence-Grounded Literature Review
```

The resulting review retains an explicit corpus-scope statement.

---

## 13. Validation and Provenance

Validation is a first-class architectural layer rather than only a UI concern.

Important relationships include:

```text
Claim
  ↓
Evidence ID
  ↓
Evidence object
  ↓
Paper ID
  ↓
Page number
```

The same principle applies to:

```text
comparative findings
gap candidates
literature-review findings
```

This enables traceability throughout the research pipeline.

---

## 14. Streamlit Presentation Layer

The Streamlit UI exposes the research services without duplicating analytical logic.

Current UI capabilities include:

```text
Home
Research Q&A
Paper Search
Compare Papers
Research Gaps
Literature Review
```

The UI calls existing services and renders their structured outputs.

The architecture therefore remains:

```text
UI
 ↓
Service
 ↓
Research / retrieval logic
```

rather than:

```text
UI
 ↓
Duplicate research logic
```

This separation makes the backend independently testable.

---

## 15. Evaluation Architecture

Evaluation is implemented as a separate layer under:

```text
src/evaluation/
evaluation/benchmarks/
evaluation/results/
```

The evaluation system measures six areas:

```text
Retrieval
Grounding
Comparison
Research Gaps
Literature Review
End-to-End Workflow
```

Conceptually:

```text
Benchmark Case
      ↓
Evaluation Runner
      ↓
Existing Production Service
      ↓
Structured Evaluation Result
      ↓
Aggregate Metrics
      ↓
JSON Result Artifact
      ↓
Phase 13 Evaluation Report
```

The evaluation framework calls the real system services rather than maintaining a separate research implementation.

---

## 16. Evaluation Boundaries

Different metrics answer different questions.

### Retrieval metrics

Measure ranking and expected-paper discovery.

Examples:

```text
Hit@K
MRR
Recall@K
```

### Grounding metrics

Measure structural evidence traceability.

Examples:

```text
claim-evidence coverage
evidence-reference integrity
provenance completeness
backend validation
```

### Analysis metrics

Measure structural integrity of:

```text
comparison matrices
gap candidates
literature-review findings
paper coverage
evidence references
```

### End-to-end metrics

Measure whether the complete research workflow executes successfully across the major services.

A 100% structural validation result does **not** mean 100% semantic or scientific accuracy.

---

## 17. Current Repository Architecture

```text
research-intelligence-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
│
├── data/
│   ├── papers/
│   └── vector_store/
│
├── evaluation/
│   ├── benchmarks/
│   └── results/
│
├── reports/
│
├── scripts/
│   ├── evaluate_retrieval.py
│   ├── evaluate_grounding.py
│   ├── evaluate_comparison.py
│   ├── evaluate_gaps.py
│   ├── evaluate_literature_review.py
│   ├── evaluate_end_to_end.py
│   └── generate_evaluation_report.py
│
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   ├── tools/
│   ├── agents/
│   ├── generation/
│   ├── analysis/
│   ├── evaluation/
│   └── ui/
│
└── tests/
```

Each layer has a distinct responsibility:

| Layer        | Responsibility                      |
| ------------ | ----------------------------------- |
| `ingestion`  | PDF and source-text processing      |
| `retrieval`  | embeddings, FAISS, ranking          |
| `tools`      | reusable research operations        |
| `agents`     | routing and orchestration           |
| `generation` | evidence-grounded Q&A               |
| `analysis`   | comparison, gaps, literature review |
| `evaluation` | benchmarks and measurement          |
| `ui`         | Streamlit presentation              |

---

## 18. Technology Architecture

```text
Python 3.11
    │
    ├── PyPDF
    │      └── document ingestion
    │
    ├── Sentence Transformers
    │      └── local embeddings
    │
    ├── FAISS
    │      └── vector similarity search
    │
    ├── NumPy
    │      └── numerical operations
    │
    ├── Pydantic
    │      └── configuration / structured models
    │
    ├── Streamlit
    │      └── user interface
    │
    └── pytest
           └── automated testing
```

---

## 19. Why the Architecture Is Interview-Relevant

The project demonstrates several engineering concepts beyond basic RAG:

```text
document ingestion
semantic retrieval
hybrid ranking
research-oriented chunking
provenance preservation
structured intermediate representations
tool-based architecture
agent routing
grounded generation
cross-document comparison
research-gap reasoning
multi-stage synthesis
validation
evaluation design
end-to-end testing
UI/service separation
```

A key architectural decision is that the system can expose uncertainty and missing evidence instead of forcing an answer.

That is particularly important for research intelligence systems where unsupported synthesis can be more harmful than returning an incomplete result.

---

## 20. Current Architecture Boundary

The current project should be viewed as a research-intelligence prototype over a bounded corpus.

It currently does not attempt to provide:

```text
an exhaustive global literature search
continuous online paper discovery
human-equivalent scientific peer review
semantic entailment verification by an expert model
universal research-gap detection
```

These are potential future extensions rather than claims of the current implementation.