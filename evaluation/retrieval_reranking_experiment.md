# Retrieval Reranking Experiment

## Objective

Evaluate whether a cross-encoder reranker improves the Phase 13 frozen
retrieval baseline for the Research Intelligence Agent.

The benchmark contains five retrieval questions and uses the same
evaluation cases and metrics for every configuration.

No benchmark questions were changed between experiments.

---

## Configurations

### 1. Frozen Hybrid Baseline

Existing retrieval pipeline:

- Sentence Transformer embeddings
- FAISS semantic retrieval
- lexical relevance
- concept bonuses
- section-aware bonuses
- per-paper result diversity

This is the frozen Phase 13 baseline.

### 2. Pure Cross-Encoder Reranking

Candidate chunks are retrieved using the existing hybrid retriever and
then completely reordered using:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

The cross-encoder score becomes the final ranking score.

Candidate pool:

`candidate_k = 30`

### 3. Fused Cross-Encoder Reranking

The same candidate pool is reranked using a fusion of:

- normalized existing hybrid retrieval score
- normalized cross-encoder score

Fusion weights:

- Hybrid retrieval: 0.50
- Cross-encoder: 0.50

No weight tuning was performed against the benchmark.

---

## Results

| Metric | Hybrid Baseline | Pure Cross-Encoder | Fused Cross-Encoder |
|---|---:|---:|---:|
| Hit@1 | 40.00% | 0.00% | 40.00% |
| Hit@3 | 40.00% | 60.00% | 60.00% |
| Hit@5 | 60.00% | 60.00% | 80.00% |
| MRR | 0.5119 | 0.2841 | 0.5289 |
| Recall@3 | 24.44% | 31.11% | 44.44% |
| Recall@5 | 48.89% | 42.22% | 55.56% |
| Recall@10 | 82.22% | 88.89% | 88.89% |

---

## Findings

The pure cross-encoder increased some broader retrieval metrics but
significantly degraded top-rank performance.

Hit@1 decreased from 40.00% to 0.00%, and MRR decreased from 0.5119
to 0.2841.

This shows that replacing the existing hybrid ranking signal entirely
with the general-purpose cross-encoder was not beneficial for this
specialized research corpus.

The fused configuration produced the strongest aggregate result.

Compared with the frozen hybrid baseline:

- Hit@1 remained at 40.00%.
- Hit@3 increased from 40.00% to 60.00%.
- Hit@5 increased from 60.00% to 80.00%.
- MRR increased from 0.5119 to 0.5289.
- Recall@3 increased from 24.44% to 44.44%.
- Recall@5 increased from 48.89% to 55.56%.
- Recall@10 increased from 82.22% to 88.89%.

The experiment therefore suggests that the cross-encoder is more useful
as an additional ranking signal than as a complete replacement for the
existing hybrid retriever.

---

## Known Limitations

The benchmark currently contains only five retrieval questions.

Therefore, these results should be interpreted as an experimental
comparison rather than a statistically robust demonstration that the
fused approach generalizes to all research queries.

The 0.50 / 0.50 fusion weight was selected before evaluation and was not
optimized against the benchmark.

A larger held-out retrieval benchmark would be required before tuning
fusion weights or making stronger generalization claims.

---

## Decision

The frozen hybrid retriever remains the stable baseline.

The fused cross-encoder reranker is retained as the strongest
experimental retrieval configuration.

The pure cross-encoder configuration is retained for reproducibility,
but is not recommended as the primary retrieval strategy.