# Research Intelligence Agent

![CI](https://github.com/jaybaragadi/research-intelligence-agent/actions/workflows/ci.yml/badge.svg)

An evidence-grounded RAG system for academic literature. It goes beyond document
Q&A: it retrieves research evidence, answers questions with claims linked to
sources, compares papers, surfaces research gaps, and generates traceable
literature reviews — preserving paper → page → section → chunk → citation
provenance end to end.

Current domain: **LLMs for automated software test generation** (a bounded
10-paper corpus). Runs fully locally; no paid LLM API required.

---

## Highlights

- **Grounded Q&A** — every claim references the evidence IDs that support it, and
  a validator rejects claims that cite anything outside the retrieved set.
- **Hybrid retrieval** — Sentence-Transformer embeddings + FAISS, combined with
  lexical and section-aware signals.
- **Cross-paper comparison** — a comparison matrix that leaves cells empty rather
  than inventing unsupported conclusions.
- **Research-gap analysis** — scoped to the indexed corpus; missing evidence is
  never treated as proof a gap exists.
- **Literature reviews** — an 8-section synthesis that carries citations through.
- **Six-part evaluation harness** and **375 passing tests** across every layer.

---

## Architecture

```
PDFs → ingestion → structure-aware chunks → embeddings + FAISS
     → hybrid retrieval → grounded Q&A / comparison / gaps / review
     → evidence + citation validation → Streamlit UI
```

Retrieval, analysis, validation, and presentation are separate layers, so each
can be tested and measured independently. Full detail in
[ARCHITECTURE.md](ARCHITECTURE.md).

---

## Evaluation

A dedicated harness scores retrieval, grounding, comparison, gaps, review, and
end-to-end workflows on a small, corpus-specific benchmark.

| Area              | Key metric                   | Result  |
| ----------------- | ---------------------------- | ------- |
| Retrieval         | Hit@1 / Hit@5                | 40% / 60% |
| Retrieval         | Mean Recall@10               | 82.2%   |
| Grounding         | Claim–evidence coverage      | 100%    |
| Grounding         | Provenance completeness      | 100%    |
| Comparison        | Evidence-reference integrity | 100%    |
| Research gaps     | Evidence-reference integrity | 100%    |
| Literature review | Structural pass rate         | 100%    |
| End-to-end        | Stage success rate           | 100%    |

<!-- After running `python -m scripts.evaluate_reranker`, add the ablation:
| Retrieval (reranked) | Hit@1 / MRR | __% / __ |
-->

**Reading the numbers:** structural traceability is strong (evidence references
and provenance hold at 100%), while early **retrieval ranking is the weak point**
(Hit@1 40% vs. Recall@10 82%) — relevant papers are usually found, just not
ranked first. These are engineering/structural metrics on a bounded corpus, not
a claim of semantic or scientific accuracy.

---

## Tech stack

Python 3.11 · PyPDF · Sentence Transformers · FAISS · Pydantic · Streamlit ·
pytest · ruff

---

## Quickstart

```bash
git clone https://github.com/jaybaragadi/research-intelligence-agent.git
cd research-intelligence-agent

python3.11 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# add legally obtained PDFs to data/papers/, then launch:
streamlit run app.py

pytest          # run the test suite
```

Research PDFs and the built index are not committed. Benchmark results describe
the development corpus and may differ with a different paper set.

---

## Repository layout

```
src/
  ingestion/   metadata/   chunking/   retrieval/   tools/
  agents/      generation/ analysis/   evaluation/  ui/
scripts/       evaluation/  reports/    tests/
```

| Layer        | Responsibility                          |
| ------------ | --------------------------------------- |
| ingestion    | PDF → structured, provenance-tagged text |
| retrieval    | embeddings, FAISS, hybrid ranking       |
| generation   | evidence-grounded Q&A                    |
| analysis     | comparison, gaps, literature review     |
| evaluation   | benchmarks and metrics                   |
| ui           | Streamlit presentation                   |

---

## Status & scope

Core system implemented and evaluated; 375 tests passing in CI. The project is a
research-intelligence **prototype over a bounded corpus** — it does not attempt
exhaustive literature search, online paper discovery, or human-equivalent peer
review. Detailed benchmarks and design notes live in
[ARCHITECTURE.md](ARCHITECTURE.md).