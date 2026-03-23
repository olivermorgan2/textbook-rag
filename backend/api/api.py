"""FastAPI router for the retrieval API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    AnswerRequest,
    AnswerResponse,
    ChunkResult,
    CitationItem,
    FetchRequest,
    FetchResponse,
    SearchRequest,
    SearchResponse,
)
from backend.providers.base import BaseProvider
from backend.rag.citations import build_citations
from backend.rag.index import get_chunk_by_id
from backend.rag.retrieve import search

router = APIRouter(prefix="/api")

# The provider is injected at app startup via ``set_provider``.
_provider: BaseProvider | None = None


def set_provider(provider: BaseProvider) -> None:
    """Set the LLM provider used by the /answer endpoint."""
    global _provider
    _provider = provider


@router.post("/search", response_model=SearchResponse)
def api_search(req: SearchRequest) -> SearchResponse:
    results = search(req.query, top_k=req.top_k)
    return SearchResponse(
        results=[ChunkResult(**r) for r in results],
    )


@router.post("/fetch", response_model=FetchResponse)
def api_fetch(req: FetchRequest) -> FetchResponse:
    payload = get_chunk_by_id(req.chunk_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return FetchResponse(chunk=ChunkResult(**payload))


@router.post("/answer", response_model=AnswerResponse)
def api_answer(req: AnswerRequest) -> AnswerResponse:
    if _provider is None:
        raise HTTPException(status_code=500, detail="No provider configured")

    results = search(req.query, top_k=req.top_k)
    generated = _provider.generate(req.query, results)

    citations = build_citations(results)

    return AnswerResponse(
        answer=generated["answer"],
        citations=[CitationItem(**c.to_dict()) for c in citations],
    )
