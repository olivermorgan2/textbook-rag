"""Qdrant vector-store helpers.

Provides a thin factory that returns a ``QdrantClient`` and ensures the
target collection exists.  Supports two modes:

* **In-memory** (default) — fast, no persistence, ideal for tests.
* **On-disk** — pass a ``path`` to persist data between runs.
"""

from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Module-level cache so repeated calls within one process reuse the client.
_clients: dict[str | None, QdrantClient] = {}


def get_client(path: str | None = None) -> QdrantClient:
    """Return a (cached) ``QdrantClient``.

    Parameters
    ----------
    path:
        Directory for on-disk storage.  ``None`` → in-memory.
    """
    if path not in _clients:
        if path is None:
            _clients[path] = QdrantClient(location=":memory:")
        else:
            _clients[path] = QdrantClient(path=path)
    return _clients[path]


def get_collection(
    collection_name: str,
    vector_size: int,
    *,
    path: str | None = None,
) -> QdrantClient:
    """Return a ``QdrantClient`` with *collection_name* guaranteed to exist.

    If the collection already exists it is left untouched (safe for re-runs).
    """
    client = get_client(path)

    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    return client


def reset_client_cache() -> None:
    """Clear the module-level client cache (useful in tests)."""
    _clients.clear()
