"""Tests for the citation formatting utility."""

from backend.rag.citations import Citation, build_citations, format_citation


class TestBuildCitations:
    def test_complete_metadata(self):
        chunks = [
            {
                "chunk_id": "ch01-0001",
                "text": "Some text",
                "source_path": "textbook/ch01.md",
                "chapter_title": "Introduction",
                "section_title": "Overview",
                "score": 0.95,
            },
            {
                "chunk_id": "ch02-0003",
                "text": "More text",
                "source_path": "textbook/ch02.md",
                "chapter_title": "Methods",
                "section_title": "Data Collection",
                "score": 0.88,
            },
        ]
        citations = build_citations(chunks)

        assert len(citations) == 2
        assert citations[0].chunk_id == "ch01-0001"
        assert citations[0].chapter_title == "Introduction"
        assert citations[0].section_title == "Overview"
        assert citations[0].source_path == "textbook/ch01.md"
        assert citations[1].chunk_id == "ch02-0003"
        assert citations[1].chapter_title == "Methods"

    def test_missing_section_title(self):
        chunks = [
            {
                "chunk_id": "ch01-0000",
                "text": "Preamble text",
                "source_path": "textbook/ch01.md",
                "chapter_title": "Introduction",
            },
        ]
        citations = build_citations(chunks)

        assert len(citations) == 1
        assert citations[0].section_title == ""
        assert citations[0].chunk_id == "ch01-0000"

    def test_missing_chapter_title(self):
        chunks = [
            {
                "chunk_id": "ch03-0002",
                "text": "Some content",
                "source_path": "textbook/ch03.md",
                "section_title": "Results",
            },
        ]
        citations = build_citations(chunks)

        assert citations[0].chapter_title == ""
        assert citations[0].section_title == "Results"

    def test_minimal_metadata(self):
        chunks = [{"text": "orphan chunk"}]
        citations = build_citations(chunks)

        assert len(citations) == 1
        assert citations[0].chunk_id == ""
        assert citations[0].source_path == ""

    def test_empty_input(self):
        assert build_citations([]) == []


class TestFormatCitation:
    def test_full_citation(self):
        c = Citation(
            chunk_id="ch01-0001",
            chapter_title="Introduction",
            section_title="Overview",
            source_path="textbook/ch01.md",
        )
        assert format_citation(c) == "Introduction — Overview (textbook/ch01.md)"

    def test_no_section(self):
        c = Citation(
            chunk_id="ch01-0000",
            chapter_title="Introduction",
            section_title="",
            source_path="textbook/ch01.md",
        )
        assert format_citation(c) == "Introduction (textbook/ch01.md)"

    def test_no_chapter(self):
        c = Citation(
            chunk_id="ch03-0002",
            chapter_title="",
            section_title="Results",
            source_path="textbook/ch03.md",
        )
        assert format_citation(c) == "Results (textbook/ch03.md)"

    def test_only_source_path(self):
        c = Citation(
            chunk_id="ch01-0001",
            chapter_title="",
            section_title="",
            source_path="textbook/ch01.md",
        )
        assert format_citation(c) == "textbook/ch01.md"

    def test_fallback_to_chunk_id(self):
        c = Citation(
            chunk_id="ch01-0001",
            chapter_title="",
            section_title="",
            source_path="",
        )
        assert format_citation(c) == "ch01-0001"


class TestCitationToDict:
    def test_round_trip(self):
        c = Citation(
            chunk_id="ch01-0001",
            chapter_title="Introduction",
            section_title="Overview",
            source_path="textbook/ch01.md",
        )
        d = c.to_dict()
        assert d == {
            "chunk_id": "ch01-0001",
            "chapter_title": "Introduction",
            "section_title": "Overview",
            "source_path": "textbook/ch01.md",
        }
