"""Tests for the embedding + indexing pipeline (backend.rag.index)."""

from __future__ import annotations

import pytest

from backend.ingest.chunker import Chunk, chunk_document
from backend.rag.index import build_index, get_chunk_by_id
from backend.rag.store import reset_client_cache

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SMALL_CORPUS_DOCS = [
    {
        "chapter_number": 1,
        "chapter_title": "Introduction",
        "source_path": "textbook/chapter_01_content.md",
        "text": (
            "# Introduction\n\n"
            "This is the introduction to the textbook. "
            "It covers the basics of the subject.\n\n"
            "## Background\n\n"
            "Some background information here. " * 10
        ),
    },
    {
        "chapter_number": 2,
        "chapter_title": "Fundamentals",
        "source_path": "textbook/chapter_02_content.md",
        "text": (
            "# Fundamentals\n\n"
            "This chapter covers fundamentals.\n\n"
            "## Key Concepts\n\n"
            "Important concepts explained. " * 10
        ),
    },
]


def _make_chunks() -> list[Chunk]:
    """Chunk the small test corpus."""
    chunks: list[Chunk] = []
    for doc in SMALL_CORPUS_DOCS:
        chunks.extend(chunk_document(doc, max_chunk_size=1500))
    return chunks


@pytest.fixture(autouse=True)
def _fresh_qdrant():
    """Ensure each test gets a clean in-memory Qdrant client."""
    reset_client_cache()
    yield
    reset_client_cache()


# Use a unique collection per test module to avoid cross-test interference.
COLLECTION = "test_textbook"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_build_index_populates():
    """Indexing a small corpus should create the expected number of points."""
    chunks = _make_chunks()
    assert len(chunks) > 0, "Fixture should produce at least one chunk"

    count = build_index(chunks, collection_name=COLLECTION)
    assert count == len(chunks)


def test_reindex_no_duplicates():
    """Running build_index twice should not duplicate entries."""
    chunks = _make_chunks()

    build_index(chunks, collection_name=COLLECTION)
    build_index(chunks, collection_name=COLLECTION)

    # Retrieve all points and verify count matches chunks, not 2x.
    from backend.rag.store import get_client

    client = get_client()
    info = client.get_collection(COLLECTION)
    assert info.points_count == len(chunks)


def test_get_chunk_by_id():
    """After indexing, a chunk should be retrievable by its chunk_id."""
    chunks = _make_chunks()
    build_index(chunks, collection_name=COLLECTION)

    target = chunks[0]
    result = get_chunk_by_id(target.chunk_id, collection_name=COLLECTION)

    assert result is not None
    assert result["chunk_id"] == target.chunk_id
    assert result["chapter_title"] == target.chapter_title
    assert result["source_path"] == target.source_path


def test_get_chunk_by_id_not_found():
    """Querying a non-existent chunk_id should return None."""
    chunks = _make_chunks()
    build_index(chunks, collection_name=COLLECTION)

    result = get_chunk_by_id("ch99-9999", collection_name=COLLECTION)
    assert result is None


def test_empty_chunks():
    """Indexing an empty list should return 0 and not error."""
    count = build_index([], collection_name=COLLECTION)
    assert count == 0
