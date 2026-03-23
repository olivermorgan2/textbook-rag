# Evaluation

## Purpose

Define how we evaluate the Textbook RAG Platform for:

- Retrieval quality.
- Answer grounding.
- Citation coverage.
- Latency.

## Metrics

### Retrieval quality

- **Precision@k** – fraction of retrieved chunks in top‑k that are relevant.
- **Recall@k** – fraction of relevant chunks that appear in top‑k.
- **MRR** – mean reciprocal rank of the first relevant chunk.

### Answer grounding

- **Grounded answer rate** – percentage of answers fully supported by retrieved text.
- **Hallucination rate (approx.)** – percentage of answers that include unsupported claims.

### Citation quality

- **Citation coverage** – percentage of answers with at least one citation.
- **Citation correctness** – percentage of citations that actually point to the used chunks.

### Latency

- **Retrieval latency** – time from query to retrieved chunks.
- **End‑to‑end latency** – time from query to answer.

## Benchmark dataset

File: `eval/questions.json`

Each record:

```json
{
  "id": "q-001",
  "question": "Example question...",
  "expected_chapter": "Chapter X",
  "expected_section": "Section name",
  "expected_sources": ["chX-0000"],
  "difficulty": "easy|medium|hard",
  "notes": "Optional notes"
}
