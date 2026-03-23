"""Chapter-aware Markdown chunking with stable IDs and metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Chunk:
    """A single chunk of text with metadata."""

    chunk_id: str
    text: str
    source_path: str
    chapter_title: str
    section_title: str

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source_path": self.source_path,
            "chapter_title": self.chapter_title,
            "section_title": self.section_title,
        }


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# Minimum chunk size (chars) — sections smaller than this are merged with the
# previous chunk rather than emitted standalone.
_MIN_CHUNK_SIZE = 200


def chunk_document(
    doc: dict,
    *,
    max_chunk_size: int = 1500,
    overlap: int = 0,
) -> list[Chunk]:
    """Split a document dict (as returned by ``ingest_corpus``) into chunks.

    Parameters
    ----------
    doc:
        Must contain at least ``text``, ``source_path``, ``chapter_number``,
        and ``chapter_title``.
    max_chunk_size:
        Maximum number of characters per chunk.
    overlap:
        Number of characters to repeat at the start of each subsequent chunk
        when a section is split due to exceeding *max_chunk_size*.

    Returns
    -------
    list[Chunk]
        Ordered list of chunks with stable IDs and metadata.
    """
    text: str = doc["text"]
    source_path: str = doc["source_path"]
    chapter_num: int = doc["chapter_number"]
    chapter_title: str = doc.get("chapter_title", "")

    # ------------------------------------------------------------------
    # 1. Split the document into (heading, body) sections
    # ------------------------------------------------------------------
    sections = _split_by_headings(text)

    # ------------------------------------------------------------------
    # 2. Build raw chunks respecting size limits, merging tiny sections
    # ------------------------------------------------------------------
    raw_chunks: list[tuple[str, str]] = []  # (section_title, text)

    for section_title, section_text in sections:
        if not section_text.strip():
            continue

        if len(section_text) <= max_chunk_size:
            # If this section is very small, merge it into the previous chunk
            if raw_chunks and len(section_text) < _MIN_CHUNK_SIZE:
                prev_title, prev_text = raw_chunks[-1]
                merged = prev_text + "\n\n" + section_text
                if len(merged) <= max_chunk_size:
                    raw_chunks[-1] = (prev_title, merged)
                    continue
            raw_chunks.append((section_title, section_text))
        else:
            # Section exceeds limit — split at paragraph boundaries
            sub_chunks = _split_large_section(section_text, max_chunk_size, overlap)
            for sub in sub_chunks:
                raw_chunks.append((section_title, sub))

    # ------------------------------------------------------------------
    # 3. Assign stable IDs and build Chunk objects
    # ------------------------------------------------------------------
    chunks: list[Chunk] = []
    for idx, (section_title, chunk_text) in enumerate(raw_chunks):
        chunk_id = f"ch{chapter_num:02d}-{idx:04d}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                text=chunk_text,
                source_path=source_path,
                chapter_title=chapter_title,
                section_title=section_title,
            )
        )

    return chunks


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _split_by_headings(text: str) -> list[tuple[str, str]]:
    """Split Markdown *text* into ``(heading_text, body)`` pairs.

    Content before the first heading gets an empty heading string.
    The heading line itself is included at the start of *body* so the
    chunk retains structural context.
    """
    matches = list(_HEADING_RE.finditer(text))

    if not matches:
        return [("", text)]

    sections: list[tuple[str, str]] = []

    # Content before the first heading
    if matches[0].start() > 0:
        preamble = text[: matches[0].start()].strip()
        if preamble:
            sections.append(("", preamble))

    for i, match in enumerate(matches):
        heading_text = match.group(2).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections.append((heading_text, body))

    return sections


def _split_large_section(
    text: str,
    max_size: int,
    overlap: int,
) -> list[str]:
    """Split *text* into pieces of at most *max_size* chars.

    Tries to break at paragraph boundaries (double newlines).  Falls back to
    a hard character split if a single paragraph exceeds the limit.
    """
    paragraphs = re.split(r"\n{2,}", text)
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para).strip() if current else para
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            # If a single paragraph is too large, hard-split it
            if len(para) > max_size:
                chunks.extend(_hard_split(para, max_size, overlap))
                current = ""
            else:
                current = para

    if current:
        chunks.append(current)

    # Apply overlap between consecutive chunks
    if overlap > 0 and len(chunks) > 1:
        overlapped = [chunks[0]]
        for i in range(1, len(chunks)):
            prev = chunks[i - 1]
            tail = prev[-overlap:] if len(prev) >= overlap else prev
            overlapped.append(tail + "\n" + chunks[i])
        chunks = overlapped

    return chunks


def _hard_split(text: str, max_size: int, overlap: int) -> list[str]:
    """Character-level split as a last resort."""
    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = start + max_size
        pieces.append(text[start:end])
        start = end - overlap if overlap else end
    return pieces
