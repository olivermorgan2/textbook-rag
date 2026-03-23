"""Tests for the retrieval API endpoints."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

# Sample chunk data returned by mocked search / get_chunk_by_id
_SAMPLE_CHUNK = {
    "chunk_id": "ch01-0000",
    "text": "Sample text from chapter 1.",
    "source_path": "textbook/chapters/chapter-01.md",
    "chapter_title": "Introduction",
    "section_title": "Overview",
}

_SAMPLE_SEARCH_RESULT = {**_SAMPLE_CHUNK, "score": 0.95}


# -- /api/search -------------------------------------------------------------


@patch("backend.api.api.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_search_happy_path(mock_search):
    resp = client.post("/api/search", json={"query": "what is RAG?"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["chunk_id"] == "ch01-0000"
    assert data["results"][0]["score"] == 0.95
    mock_search.assert_called_once_with("what is RAG?", top_k=5)


def test_search_empty_query():
    resp = client.post("/api/search", json={"query": ""})
    assert resp.status_code == 422  # validation error


@patch("backend.api.api.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_search_custom_top_k(mock_search):
    resp = client.post("/api/search", json={"query": "test", "top_k": 3})
    assert resp.status_code == 200
    mock_search.assert_called_once_with("test", top_k=3)


def test_search_missing_query():
    resp = client.post("/api/search", json={})
    assert resp.status_code == 422


# -- /api/fetch --------------------------------------------------------------


@patch("backend.api.api.get_chunk_by_id", return_value=_SAMPLE_CHUNK)
def test_fetch_happy_path(mock_get):
    resp = client.post("/api/fetch", json={"chunk_id": "ch01-0000"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["chunk"]["chunk_id"] == "ch01-0000"
    assert data["chunk"]["text"] == "Sample text from chapter 1."
    mock_get.assert_called_once_with("ch01-0000")


@patch("backend.api.api.get_chunk_by_id", return_value=None)
def test_fetch_not_found(mock_get):
    resp = client.post("/api/fetch", json={"chunk_id": "ch99-9999"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Chunk not found"


def test_fetch_empty_chunk_id():
    resp = client.post("/api/fetch", json={"chunk_id": ""})
    assert resp.status_code == 422


# -- /api/answer -------------------------------------------------------------


@patch("backend.api.api.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_answer_happy_path(mock_search):
    resp = client.post("/api/answer", json={"query": "what is RAG?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert isinstance(data["citations"], list)
    assert len(data["citations"]) == 1
    assert data["citations"][0]["chunk_id"] == "ch01-0000"


def test_answer_empty_query():
    resp = client.post("/api/answer", json={"query": ""})
    assert resp.status_code == 422


@patch("backend.api.api.search", return_value=[_SAMPLE_SEARCH_RESULT])
def test_answer_schema_fields(mock_search):
    resp = client.post("/api/answer", json={"query": "test"})
    assert resp.status_code == 200
    data = resp.json()
    citation = data["citations"][0]
    assert "chapter_title" in citation
    assert "section_title" in citation
    assert "source_path" in citation
