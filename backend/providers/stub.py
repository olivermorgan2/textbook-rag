"""Stub provider that echoes context without calling an LLM.

Useful for testing the retrieval pipeline end-to-end without needing
an API key or network access.
"""

from __future__ import annotations

from backend.providers.base import BaseProvider


class StubProvider(BaseProvider):
    """Returns context chunks verbatim as the answer."""

    def generate(self, query: str, context: list[dict]) -> dict:
        if not context:
            return {"answer": "No relevant context found.", "citations": []}

        answer_parts = [chunk.get("text", "") for chunk in context]
        citations = [
            {
                "chunk_id": chunk.get("chunk_id", ""),
                "chapter_title": chunk.get("chapter_title", ""),
                "section_title": chunk.get("section_title", ""),
                "source_path": chunk.get("source_path", ""),
            }
            for chunk in context
        ]

        return {
            "answer": "\n\n---\n\n".join(answer_parts),
            "citations": citations,
        }
