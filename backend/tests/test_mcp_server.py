"""Tests for the MCP server tools."""

from __future__ import annotations

from unittest.mock import patch

from backend.mcp_server import fetch_chunk, list_chapters, search_textbook

_SAMPLE_CHUNK = {
    "chunk_id": "ch01-0000",
    "text": "Sample text from chapter 1.",
    "source_path": "textbook/chapters/chapter-01.md",
    "chapter_title": "Introduction",
    "section_title": "Overview",
}

_SAMPLE_SEARCH_RESULT = {**_SAMPLE_CHUNK, "score": 0.95}

_SAMPLE_DOC = {
    "chapter_number": 1,
    "chapter_title": "Introduction",
    "part_title": "Part I",
    "source_path": "textbook/chapters/chapter-01.md",
    "text": "Full chapter text...",
}


# -- search_textbook ---------------------------------------------------------


@patch("backend.mcp_server.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_search_textbook_returns_results(mock_search):
    results = search_textbook("what is RAG?")
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "ch01-0000"
    assert results[0]["score"] == 0.95
    mock_search.assert_called_once_with("what is RAG?", top_k=5)


@patch("backend.mcp_server.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_search_textbook_custom_top_k(mock_search):
    search_textbook("test", top_k=3)
    mock_search.assert_called_once_with("test", top_k=3)


@patch("backend.mcp_server.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_search_textbook_result_shape(mock_search):
    results = search_textbook("query")
    result = results[0]
    assert "chunk_id" in result
    assert "text" in result
    assert "source_path" in result
    assert "chapter_title" in result
    assert "section_title" in result
    assert "score" in result


# -- fetch_chunk --------------------------------------------------------------


@patch("backend.mcp_server.get_chunk_by_id", return_value=_SAMPLE_CHUNK)
def test_fetch_chunk_found(mock_get):
    result = fetch_chunk("ch01-0000")
    assert result["chunk_id"] == "ch01-0000"
    assert result["text"] == "Sample text from chapter 1."
    mock_get.assert_called_once_with("ch01-0000")


@patch("backend.mcp_server.get_chunk_by_id", return_value=None)
def test_fetch_chunk_not_found(mock_get):
    result = fetch_chunk("ch99-9999")
    assert "error" in result
    assert "ch99-9999" in result["error"]


# -- list_chapters ------------------------------------------------------------


@patch("backend.mcp_server.ingest_corpus", return_value=[_SAMPLE_DOC])
def test_list_chapters_returns_summaries(mock_ingest):
    chapters = list_chapters()
    assert isinstance(chapters, list)
    assert len(chapters) == 1
    ch = chapters[0]
    assert ch["chapter_number"] == 1
    assert ch["chapter_title"] == "Introduction"
    assert ch["part_title"] == "Part I"
    assert ch["source_path"] == "textbook/chapters/chapter-01.md"


@patch("backend.mcp_server.ingest_corpus", return_value=[_SAMPLE_DOC])
def test_list_chapters_excludes_text(mock_ingest):
    chapters = list_chapters()
    assert "text" not in chapters[0]
