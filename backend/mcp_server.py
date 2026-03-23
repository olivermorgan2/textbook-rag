"""Read-only MCP server exposing textbook retrieval tools."""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from backend.ingest.ingest import ingest_corpus
from backend.rag.index import get_chunk_by_id
from backend.rag.retrieve import search

mcp = FastMCP("textbook-rag")

_CHAPTERS_DIR = Path(__file__).resolve().parent.parent / "textbook" / "chapters"


@mcp.tool()
def search_textbook(query: str, top_k: int = 5) -> list[dict]:
    """Search the textbook for chunks matching a query.

    Args:
        query: The search query.
        top_k: Number of results to return (default 5).

    Returns:
        List of matching chunks with scores.
    """
    return search(query, top_k=top_k)


@mcp.tool()
def fetch_chunk(chunk_id: str) -> dict:
    """Fetch a single chunk by its ID.

    Args:
        chunk_id: The unique chunk identifier (e.g. 'ch01-0000').

    Returns:
        The chunk payload, or an error dict if not found.
    """
    result = get_chunk_by_id(chunk_id)
    if result is None:
        return {"error": f"Chunk '{chunk_id}' not found"}
    return result


@mcp.tool()
def list_chapters() -> list[dict]:
    """List all chapters in the textbook.

    Returns:
        List of chapter summaries with number, title, part, and source path.
    """
    docs = ingest_corpus(_CHAPTERS_DIR)
    return [
        {
            "chapter_number": d["chapter_number"],
            "chapter_title": d["chapter_title"],
            "part_title": d.get("part_title"),
            "source_path": d["source_path"],
        }
        for d in docs
    ]


if __name__ == "__main__":
    mcp.run()
