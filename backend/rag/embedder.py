"""Embedding wrapper using sentence-transformers.

Keeps the embedding model as a swappable detail — callers only see
``embed_texts(texts) -> list[list[float]]``.
"""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model(model_name: str = DEFAULT_MODEL_NAME) -> SentenceTransformer:
    """Load (and cache) the sentence-transformer model."""
    return SentenceTransformer(model_name)


def embed_texts(
    texts: list[str],
    *,
    model_name: str = DEFAULT_MODEL_NAME,
    batch_size: int = 64,
) -> list[list[float]]:
    """Return embedding vectors for *texts*.

    Parameters
    ----------
    texts:
        Plain-text strings to embed.
    model_name:
        HuggingFace model identifier.
    batch_size:
        Encoding batch size passed to the model.

    Returns
    -------
    list[list[float]]
        One vector per input text.
    """
    model = _get_model(model_name)
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=False)
    return [vec.tolist() for vec in embeddings]
