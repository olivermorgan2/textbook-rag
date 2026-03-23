"""Abstract base class for model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Common interface for LLM providers.

    Every provider must implement ``generate``, which takes a user query
    and a list of context chunks and returns an answer with citations.
    """

    @abstractmethod
    def generate(
        self,
        query: str,
        context: list[dict],
    ) -> dict:
        """Generate an answer from *query* using *context* chunks.

        Parameters
        ----------
        query:
            The user's question.
        context:
            List of chunk dicts (each has ``chunk_id``, ``text``, etc.).

        Returns
        -------
        dict
            ``{"answer": str, "citations": list[dict]}`` where each
            citation maps back to a specific chunk.
        """
