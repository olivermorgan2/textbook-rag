"""Tests for backend.ingest.ingest module."""

from __future__ import annotations

import json

from backend.ingest.ingest import ingest_corpus

SAMPLE_METADATA = {
    "chapter_number": 1,
    "title": "Introduction to Global Health",
    "part": {"part_number": 1, "part_title": "Foundations"},
    "version": "1.0",
    "learning_objectives": [],
}

SAMPLE_MD = "# Chapter 1: Introduction to Global Health\n\nSome content here.\n"


def _write_pair(chapters_dir, chapter_num, md_text, metadata):
    """Helper to write a matched .md + .json pair."""
    md_path = chapters_dir / f"chapter_{chapter_num:02d}_topic.md"
    md_path.write_text(md_text, encoding="utf-8")
    json_path = chapters_dir / f"chapter_{chapter_num:02d}_metadata.json"
    json_path.write_text(json.dumps(metadata), encoding="utf-8")


def test_ingest_matched_pair(tmp_path):
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    _write_pair(chapters, 1, SAMPLE_MD, SAMPLE_METADATA)

    docs = ingest_corpus(chapters)

    assert len(docs) == 1
    doc = docs[0]
    assert doc["chapter_number"] == 1
    assert doc["chapter_title"] == "Introduction to Global Health"
    assert doc["part_number"] == 1
    assert doc["part_title"] == "Foundations"
    assert doc["text"] == SAMPLE_MD
    assert doc["metadata"] == SAMPLE_METADATA
    assert "chapter_01_topic.md" in doc["source_path"]


def test_ingest_missing_json(tmp_path):
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    md_path = chapters / "chapter_05_diseases.md"
    md_path.write_text("# Chapter 5\n\nContent.\n", encoding="utf-8")

    docs = ingest_corpus(chapters)

    assert len(docs) == 1
    doc = docs[0]
    assert doc["chapter_number"] == 5
    assert doc["chapter_title"] == ""
    assert doc["metadata"] is None
    assert doc["text"].startswith("# Chapter 5")


def test_ingest_missing_md(tmp_path):
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    json_path = chapters / "chapter_03_metadata.json"
    json_path.write_text(json.dumps({"chapter_number": 3, "title": "Test"}), encoding="utf-8")

    docs = ingest_corpus(chapters)

    assert len(docs) == 0


def test_ingest_multiple_chapters(tmp_path):
    chapters = tmp_path / "chapters"
    chapters.mkdir()

    meta_1 = {**SAMPLE_METADATA, "chapter_number": 1}
    meta_2 = {
        "chapter_number": 2,
        "title": "Health Determinants",
        "part": {"part_number": 1, "part_title": "Foundations"},
    }

    _write_pair(chapters, 1, SAMPLE_MD, meta_1)
    _write_pair(chapters, 2, "# Chapter 2\n\nDeterminants.\n", meta_2)

    docs = ingest_corpus(chapters)

    assert len(docs) == 2
    assert docs[0]["chapter_number"] == 1
    assert docs[1]["chapter_number"] == 2
    assert docs[1]["chapter_title"] == "Health Determinants"
    assert docs[0]["metadata"] is not None
    assert docs[1]["metadata"] is not None
