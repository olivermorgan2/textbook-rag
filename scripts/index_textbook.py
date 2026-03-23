#!/usr/bin/env python3
"""CLI entry point: ingest → chunk → embed → index.

Usage:
    python -m scripts.index_textbook [--chapters-dir textbook/chapters] [--storage-path data/qdrant]

Defaults to in-memory indexing (useful for smoke-testing).  Pass ``--storage-path``
to persist the index to disk for later retrieval.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Ensure the repo root is on sys.path so ``backend`` is importable.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from backend.ingest import ingest_corpus, chunk_document
from backend.rag.index import build_index

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Index the textbook corpus.")
    parser.add_argument(
        "--chapters-dir",
        default="textbook/chapters",
        help="Path to the directory containing chapter .md and .json files.",
    )
    parser.add_argument(
        "--storage-path",
        default=None,
        help="Directory for on-disk Qdrant storage (omit for in-memory).",
    )
    parser.add_argument(
        "--max-chunk-size",
        type=int,
        default=1500,
        help="Maximum characters per chunk.",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=0,
        help="Character overlap between consecutive chunks.",
    )
    args = parser.parse_args(argv)

    # 1. Ingest
    logger.info("Ingesting from %s …", args.chapters_dir)
    documents = ingest_corpus(args.chapters_dir)
    logger.info("Found %d chapter documents.", len(documents))

    # 2. Chunk
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(
            doc,
            max_chunk_size=args.max_chunk_size,
            overlap=args.overlap,
        )
        all_chunks.extend(chunks)
    logger.info("Produced %d chunks.", len(all_chunks))

    # 3. Index
    indexed = build_index(all_chunks, storage_path=args.storage_path)
    logger.info("Indexed %d chunks. Done.", indexed)


if __name__ == "__main__":
    main()
