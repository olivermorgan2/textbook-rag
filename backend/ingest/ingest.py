"""Ingestion module for loading textbook chapter Markdown and metadata files."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

_CHAPTER_NUM_RE = re.compile(r"[Cc]hapter_(\d+)_")


def _extract_chapter_number(filename: str) -> int | None:
    """Extract the chapter number from a filename like chapter_10_metadata.json."""
    m = _CHAPTER_NUM_RE.search(filename)
    return int(m.group(1)) if m else None


def _find_md_file(chapters_dir: Path, chapter_num: int) -> Path | None:
    """Find the .md file for a given chapter number (case-insensitive)."""
    pattern = f"*hapter_{chapter_num:02d}_*.md"
    matches = list(chapters_dir.glob(pattern))
    if not matches:
        # Try without zero-padding
        pattern = f"*hapter_{chapter_num}_*.md"
        matches = list(chapters_dir.glob(pattern))
    # Filter out metadata files
    matches = [m for m in matches if "metadata" not in m.name.lower()]
    return matches[0] if matches else None


def _find_json_file(chapters_dir: Path, chapter_num: int) -> Path | None:
    """Find the metadata JSON file for a given chapter number."""
    pattern = f"chapter_{chapter_num:02d}_metadata.json"
    path = chapters_dir / pattern
    if path.exists():
        return path
    # Try without zero-padding
    pattern = f"chapter_{chapter_num}_metadata.json"
    path = chapters_dir / pattern
    return path if path.exists() else None


def ingest_corpus(chapters_dir: str | Path) -> list[dict]:
    """Load all chapter .md and .json pairs from *chapters_dir*.

    Returns a list of document dicts sorted by chapter number.  Each dict
    contains at least: chapter_number, chapter_title, part_number, part_title,
    source_path, text, and metadata.
    """
    chapters_dir = Path(chapters_dir)
    if not chapters_dir.is_dir():
        raise FileNotFoundError(f"Chapters directory not found: {chapters_dir}")

    # Collect all chapter numbers from both .md and .json files
    chapter_nums: set[int] = set()
    for path in chapters_dir.iterdir():
        num = _extract_chapter_number(path.name)
        if num is not None and (
            path.suffix == ".md" or path.name.endswith("_metadata.json")
        ):
            chapter_nums.add(num)

    documents: list[dict] = []

    for chapter_num in sorted(chapter_nums):
        md_path = _find_md_file(chapters_dir, chapter_num)
        json_path = _find_json_file(chapters_dir, chapter_num)

        # JSON exists but no Markdown -> skip
        if json_path and not md_path:
            logger.warning(
                "Chapter %d: metadata JSON found (%s) but no .md file — skipping",
                chapter_num,
                json_path.name,
            )
            continue

        # Load Markdown content
        text = md_path.read_text(encoding="utf-8")

        # Load metadata if available
        metadata: dict | None = None
        if json_path:
            metadata = json.loads(json_path.read_text(encoding="utf-8"))
        else:
            logger.warning(
                "Chapter %d: .md found (%s) but no metadata JSON — ingesting with minimal metadata",
                chapter_num,
                md_path.name,
            )

        # Build document
        chapter_title = metadata.get("title", "") if metadata else ""
        part = metadata.get("part", {}) if metadata else {}

        documents.append(
            {
                "chapter_number": chapter_num,
                "chapter_title": chapter_title,
                "part_number": part.get("part_number") if part else None,
                "part_title": part.get("part_title") if part else None,
                "source_path": str(md_path),
                "text": text,
                "metadata": metadata,
            }
        )

    logger.info("Ingested %d chapter documents from %s", len(documents), chapters_dir)
    return documents
