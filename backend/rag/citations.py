"""Citation formatting utility for retrieved chunks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Citation:
    """A citation derived from a retrieved chunk's metadata."""

    chunk_id: str
    chapter_title: str
    section_title: str
    source_path: str

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "chapter_title": self.chapter_title,
            "section_title": self.section_title,
            "source_path": self.source_path,
        }


def build_citations(chunks: list[dict]) -> list[Citation]:
    """Extract citation metadata from retrieved chunk dicts.

    Missing metadata fields default to ``""`` so that partial citations
    are returned rather than raising errors.
    """
    citations: list[Citation] = []
    for chunk in chunks:
        citations.append(
            Citation(
                chunk_id=chunk.get("chunk_id", ""),
                chapter_title=chunk.get("chapter_title", ""),
                section_title=chunk.get("section_title", ""),
                source_path=chunk.get("source_path", ""),
            )
        )
    return citations


def format_citation(citation: Citation) -> str:
    """Return a human-readable string representation of a citation.

    Format: ``"Chapter Title — Section Title (source_path)"``

    Parts are omitted when empty.
    """
    parts: list[str] = []
    if citation.chapter_title:
        parts.append(citation.chapter_title)
    if citation.section_title:
        parts.append(citation.section_title)

    label = " — ".join(parts)

    if citation.source_path:
        return f"{label} ({citation.source_path})" if label else citation.source_path
    return label or citation.chunk_id
