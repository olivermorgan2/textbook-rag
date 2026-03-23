"""Evaluation harness for retrieval quality and citation coverage.

Usage
-----
    python -m eval.run_eval [--top-k 5] [--output eval/results/]
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
EVAL_DIR = Path(__file__).resolve().parent
QUESTIONS_PATH = EVAL_DIR / "questions.json"
DEFAULT_OUTPUT_DIR = EVAL_DIR / "results"

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Metrics helpers
# ---------------------------------------------------------------------------

def _recall_at_k(retrieved_ids: list[str], expected_ids: list[str]) -> float:
    """Fraction of expected sources that appear in the retrieved set."""
    if not expected_ids:
        return 0.0
    found = sum(1 for eid in expected_ids if eid in retrieved_ids)
    return found / len(expected_ids)


def _precision_at_k(retrieved_ids: list[str], expected_ids: list[str]) -> float:
    """Fraction of retrieved chunks that are in the expected set."""
    if not retrieved_ids:
        return 0.0
    relevant = sum(1 for rid in retrieved_ids if rid in expected_ids)
    return relevant / len(retrieved_ids)


def _reciprocal_rank(retrieved_ids: list[str], expected_ids: list[str]) -> float:
    """Reciprocal rank of the first relevant chunk (0 if none found)."""
    for i, rid in enumerate(retrieved_ids):
        if rid in expected_ids:
            return 1.0 / (i + 1)
    return 0.0


# ---------------------------------------------------------------------------
# Main evaluation logic
# ---------------------------------------------------------------------------

def load_questions(path: Path | None = None) -> list[dict]:
    """Load the benchmark questions from JSON."""
    path = path or QUESTIONS_PATH
    with open(path) as f:
        return json.load(f)


def evaluate(top_k: int = 5, storage_path: str | None = None) -> dict:
    """Run retrieval for each benchmark question and compute metrics."""
    # Import retrieval inside the function so the module can be imported
    # without requiring all backend dependencies (handy for linting).
    from backend.rag.retrieve import search

    questions = load_questions()
    per_question: list[dict] = []

    total_recall = 0.0
    total_precision = 0.0
    total_rr = 0.0
    total_hit = 0  # questions with at least one expected source retrieved

    for q in questions:
        qid = q["id"]
        query = q["question"]
        expected = q["expected_sources"]

        t0 = time.perf_counter()
        results = search(query, top_k=top_k, storage_path=storage_path)
        latency_ms = (time.perf_counter() - t0) * 1000

        retrieved_ids = [r["chunk_id"] for r in results]

        recall = _recall_at_k(retrieved_ids, expected)
        precision = _precision_at_k(retrieved_ids, expected)
        rr = _reciprocal_rank(retrieved_ids, expected)
        hit = int(any(rid in expected for rid in retrieved_ids))

        total_recall += recall
        total_precision += precision
        total_rr += rr
        total_hit += hit

        per_question.append({
            "id": qid,
            "question": query,
            "expected_sources": expected,
            "retrieved_sources": retrieved_ids,
            "recall_at_k": round(recall, 4),
            "precision_at_k": round(precision, 4),
            "reciprocal_rank": round(rr, 4),
            "hit": hit,
            "retrieval_latency_ms": round(latency_ms, 1),
        })

    n = len(questions)
    aggregate = {
        "num_questions": n,
        "top_k": top_k,
        "mean_recall_at_k": round(total_recall / n, 4) if n else 0.0,
        "mean_precision_at_k": round(total_precision / n, 4) if n else 0.0,
        "mrr": round(total_rr / n, 4) if n else 0.0,
        "citation_coverage": round(total_hit / n, 4) if n else 0.0,
    }

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "aggregate": aggregate,
        "per_question": per_question,
    }


def save_results(results: dict, output_dir: Path | None = None) -> Path:
    """Write results JSON to the output directory and return the path."""
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = output_dir / f"eval_{ts}.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run retrieval evaluation")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to retrieve (default: 5)")
    parser.add_argument("--storage-path", type=str, default=None, help="Path to on-disk Qdrant storage (default: in-memory)")
    parser.add_argument("--output", type=str, default=None, help="Output directory for results (default: eval/results/)")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logger.info("Running evaluation with top_k=%d ...", args.top_k)
    results = evaluate(top_k=args.top_k, storage_path=args.storage_path)

    output_dir = Path(args.output) if args.output else None
    path = save_results(results, output_dir)

    agg = results["aggregate"]
    print(f"\n{'='*50}")
    print(f"Evaluation Results (top_k={agg['top_k']})")
    print(f"{'='*50}")
    print(f"  Questions:          {agg['num_questions']}")
    print(f"  Mean Recall@{agg['top_k']}:      {agg['mean_recall_at_k']:.4f}")
    print(f"  Mean Precision@{agg['top_k']}:   {agg['mean_precision_at_k']:.4f}")
    print(f"  MRR:                {agg['mrr']:.4f}")
    print(f"  Citation Coverage:  {agg['citation_coverage']:.4f}")
    print(f"{'='*50}")
    print(f"Results saved to: {path}")


if __name__ == "__main__":
    main()
