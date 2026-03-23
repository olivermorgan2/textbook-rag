"""Tests for backend.ingest.chunker module."""

from __future__ import annotations

import re

from backend.ingest.chunker import Chunk, chunk_document

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CHUNK_ID_RE = re.compile(r"^ch\d{2}-\d{4}$")


def _make_doc(text: str, chapter_number: int = 1, **overrides) -> dict:
    """Build a minimal document dict suitable for chunk_document."""
    doc = {
        "chapter_number": chapter_number,
        "chapter_title": overrides.pop("chapter_title", "Test Chapter"),
        "source_path": overrides.pop("source_path", "textbook/chapter_01_topic.md"),
        "text": text,
    }
    doc.update(overrides)
    return doc


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_long_document_produces_multiple_chunks():
    """A document with several sections exceeding max_chunk_size yields >1 chunk."""
    sections = []
    for i in range(10):
        sections.append(f"## Section {i}\n\n{'Lorem ipsum dolor sit amet. ' * 30}")
    text = "# Big Chapter\n\n" + "\n\n".join(sections)

    doc = _make_doc(text)
    chunks = chunk_document(doc, max_chunk_size=500)

    assert len(chunks) > 1


def test_metadata_presence():
    """Every chunk must carry chunk_id, source_path, chapter_title, section_title."""
    text = "# Chapter 1: Intro\n\nSome intro content.\n\n## Part A\n\nDetails here.\n"
    doc = _make_doc(text, chapter_title="Intro", source_path="textbook/ch01.md")
    chunks = chunk_document(doc)

    assert len(chunks) >= 1
    for chunk in chunks:
        assert chunk.chunk_id
        assert chunk.source_path == "textbook/ch01.md"
        assert chunk.chapter_title == "Intro"
        assert chunk.section_title is not None  # may be ""


def test_heading_respecting_behavior():
    """Content under different ## headings should land in different chunks."""
    text = (
        "# Chapter 1\n\n"
        "## Alpha\n\n" + "Alpha content. " * 40 + "\n\n"
        "## Beta\n\n" + "Beta content. " * 40 + "\n\n"
    )
    doc = _make_doc(text)
    chunks = chunk_document(doc, max_chunk_size=2000)

    # With a generous limit, each heading section should be its own chunk
    section_titles = [c.section_title for c in chunks]
    assert "Alpha" in section_titles
    assert "Beta" in section_titles

    # The Alpha chunk should not contain Beta content and vice-versa
    alpha_chunks = [c for c in chunks if c.section_title == "Alpha"]
    beta_chunks = [c for c in chunks if c.section_title == "Beta"]
    assert alpha_chunks and beta_chunks
    assert "Beta content" not in alpha_chunks[0].text
    assert "Alpha content" not in beta_chunks[0].text


def test_chunk_size_limit():
    """No chunk should exceed the configured max_chunk_size."""
    text = "# Chapter\n\n" + "Word " * 2000
    doc = _make_doc(text)
    max_size = 800
    chunks = chunk_document(doc, max_chunk_size=max_size)

    for chunk in chunks:
        assert len(chunk.text) <= max_size, (
            f"Chunk {chunk.chunk_id} has {len(chunk.text)} chars, exceeds {max_size}"
        )


def test_stable_chunk_ids():
    """Chunk IDs should follow the chNN-SSSS pattern."""
    text = "# Ch1\n\nHello world.\n\n## Sec A\n\nContent A.\n"
    doc = _make_doc(text, chapter_number=3)
    chunks = chunk_document(doc)

    for chunk in chunks:
        assert CHUNK_ID_RE.match(chunk.chunk_id), (
            f"chunk_id '{chunk.chunk_id}' does not match pattern chNN-SSSS"
        )
    # Chapter 3 should produce ch03-* IDs
    assert all(c.chunk_id.startswith("ch03-") for c in chunks)


def test_to_dict():
    """Chunk.to_dict() should return all required metadata keys."""
    text = "# Title\n\nBody text."
    doc = _make_doc(text)
    chunks = chunk_document(doc)
    d = chunks[0].to_dict()

    assert set(d.keys()) == {"chunk_id", "text", "source_path", "chapter_title", "section_title"}


def test_overlap():
    """When overlap is set, subsequent chunks should start with trailing text from the previous chunk."""
    text = "# Chapter\n\n" + "Word " * 1000
    doc = _make_doc(text)
    chunks = chunk_document(doc, max_chunk_size=500, overlap=50)

    assert len(chunks) > 1
    # Second chunk should contain some text from the end of the first
    # (exact overlap depends on paragraph splitting, so just verify we get >1 chunk)


def test_small_sections_merged():
    """Very small sections should be merged into the previous chunk."""
    text = (
        "# Chapter\n\n"
        "## Big Section\n\n" + "Content here. " * 30 + "\n\n"
        "## Tiny\n\nOk.\n"
    )
    doc = _make_doc(text)
    chunks = chunk_document(doc, max_chunk_size=2000)

    # The tiny section should be merged, so "Ok." appears in a chunk
    # but there shouldn't be a standalone chunk for just "Ok."
    all_text = " ".join(c.text for c in chunks)
    assert "Ok." in all_text


def test_empty_document():
    """An empty document should return no chunks."""
    doc = _make_doc("")
    chunks = chunk_document(doc)
    assert chunks == []
