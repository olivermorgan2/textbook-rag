"""Semantic search over the indexed textbook chunks."""

from __future__ import annotations

import logging

from backend.rag.embedder import embed_texts
from backend.rag.index import COLLECTION_NAME
from backend.rag.store import get_client

logger = logging.getLogger(__name__)


def search(
    query: str,
    *,
    top_k: int = 5,
    collection_name: str = COLLECTION_NAME,
    storage_path: str | None = None,
) -> list[dict]:
    """Embed *query* and return the top-k most similar chunks.

    Each result dict contains the chunk payload plus a ``score`` field.
    """
    vectors = embed_texts([query])
    query_vector = vectors[0]

    client = get_client(path=storage_path)

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    return [
        {**point.payload, "score": point.score}
        for point in results.points
    ]
