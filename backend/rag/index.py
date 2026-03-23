"""Embedding + indexing pipeline.

``build_index`` takes a list of ``Chunk`` objects, embeds them, and upserts
them into a Qdrant collection.  Because point IDs are derived deterministically
from ``chunk_id``, re-running the pipeline overwrites existing entries rather
than creating duplicates.
"""

from __future__ import annotations

import hashlib
import logging
import uuid
from typing import TYPE_CHECKING

from backend.rag.embedder import embed_texts
from backend.rag.store import get_collection

if TYPE_CHECKING:
    from backend.ingest.chunker import Chunk

from qdrant_client.models import PointStruct

logger = logging.getLogger(__name__)

COLLECTION_NAME = "textbook"


def _chunk_id_to_uuid(chunk_id: str) -> str:
    """Derive a deterministic UUID from a chunk_id string."""
    h = hashlib.sha256(chunk_id.encode()).digest()[:16]
    return str(uuid.UUID(bytes=h))


def build_index(
    chunks: list[Chunk],
    *,
    collection_name: str = COLLECTION_NAME,
    storage_path: str | None = None,
    batch_size: int = 64,
) -> int:
    """Embed *chunks* and upsert them into the vector store.

    Parameters
    ----------
    chunks:
        Chunk objects produced by ``chunk_document``.
    collection_name:
        Name of the Qdrant collection.
    storage_path:
        On-disk path for persistence (``None`` → in-memory).
    batch_size:
        Batch size for embedding and upsert operations.

    Returns
    -------
    int
        Number of chunks indexed.
    """
    if not chunks:
        return 0

    texts = [c.text for c in chunks]
    vectors = embed_texts(texts, batch_size=batch_size)
    vector_size = len(vectors[0])

    client = get_collection(
        collection_name,
        vector_size=vector_size,
        path=storage_path,
    )

    # Upsert in batches
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i : i + batch_size]
        batch_vectors = vectors[i : i + batch_size]

        points = [
            PointStruct(
                id=_chunk_id_to_uuid(chunk.chunk_id),
                vector=vec,
                payload=chunk.to_dict(),
            )
            for chunk, vec in zip(batch_chunks, batch_vectors)
        ]

        client.upsert(collection_name=collection_name, points=points)

    logger.info(
        "Indexed %d chunks into collection '%s'", len(chunks), collection_name
    )
    return len(chunks)


def get_chunk_by_id(
    chunk_id: str,
    *,
    collection_name: str = COLLECTION_NAME,
    storage_path: str | None = None,
) -> dict | None:
    """Retrieve a single chunk's payload by its ``chunk_id``.

    Returns the payload dict, or ``None`` if not found.
    """
    client = get_collection(
        collection_name,
        vector_size=1,  # collection must already exist; size is ignored
        path=storage_path,
    )

    point_id = _chunk_id_to_uuid(chunk_id)

    results = client.retrieve(
        collection_name=collection_name,
        ids=[point_id],
        with_payload=True,
    )

    if results:
        return results[0].payload
    return None
