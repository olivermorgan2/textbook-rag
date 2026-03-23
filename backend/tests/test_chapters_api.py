"""Tests for the chapter browsing API endpoints."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

_SAMPLE_DOCS = [
    {
        "chapter_number": 1,
        "chapter_title": "Introduction",
        "part_number": 1,
        "part_title": "Foundations",
        "source_path": "textbook/chapters/chapter_01_content.md",
        "text": "# Introduction\n\nWelcome to chapter 1.",
        "metadata": {},
    },
    {
        "chapter_number": 2,
        "chapter_title": "Background",
        "part_number": 1,
        "part_title": "Foundations",
        "source_path": "textbook/chapters/chapter_02_content.md",
        "text": "# Background\n\nChapter 2 content here.",
        "metadata": {},
    },
]


@patch("backend.api.api.ingest_corpus", return_value=_SAMPLE_DOCS)
def test_list_chapters(mock_ingest):
    resp = client.get("/api/chapters")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["chapters"]) == 2
    assert data["chapters"][0]["chapter_number"] == 1
    assert data["chapters"][0]["chapter_title"] == "Introduction"
    assert data["chapters"][1]["chapter_number"] == 2


@patch("backend.api.api.ingest_corpus", return_value=_SAMPLE_DOCS)
def test_get_chapter(mock_ingest):
    resp = client.get("/api/chapters/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["chapter_number"] == 1
    assert data["chapter_title"] == "Introduction"
    assert "Welcome to chapter 1" in data["text"]


@patch("backend.api.api.ingest_corpus", return_value=_SAMPLE_DOCS)
def test_get_chapter_not_found(mock_ingest):
    resp = client.get("/api/chapters/99")
    assert resp.status_code == 404
    assert "Chapter 99 not found" in resp.json()["detail"]


@patch("backend.api.api.ingest_corpus", return_value=_SAMPLE_DOCS)
def test_list_chapters_schema(mock_ingest):
    resp = client.get("/api/chapters")
    data = resp.json()
    ch = data["chapters"][0]
    assert "chapter_number" in ch
    assert "chapter_title" in ch
    assert "source_path" in ch
    assert "part_title" in ch
