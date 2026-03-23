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
```

## Running the evaluation

### Prerequisites

The textbook must be ingested and indexed before running the evaluation.
See the main README for ingestion instructions.

### Command

From the project root:

```bash
# First, index the textbook to disk (if not already done):
python3 scripts/index_textbook.py --storage-path data/qdrant

# Then run the evaluation:
python3 -m eval.run_eval --storage-path data/qdrant
```

Options:

- `--top-k N` – number of results to retrieve per question (default: 5).
- `--storage-path DIR` – path to on-disk Qdrant storage (default: in-memory).
- `--output DIR` – directory for results JSON (default: `eval/results/`).

### Output

The script prints aggregate metrics to stdout and saves a timestamped JSON
file to `eval/results/`. Each results file contains:

- **aggregate** – mean Recall@k, mean Precision@k, MRR, and citation coverage.
- **per_question** – per-question breakdown including retrieved sources and
  retrieval latency.

### Adding benchmark questions

Add new entries to `eval/questions.json` following the schema above. Use
chunk IDs from the indexed corpus as `expected_sources` (format: `chNN-XXXX`).
