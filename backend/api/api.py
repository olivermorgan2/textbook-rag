"""FastAPI router for the retrieval API."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    AnswerRequest,
    AnswerResponse,
    ChapterDetailResponse,
    ChapterListResponse,
    ChapterSummary,
    ChunkResult,
    CitationItem,
    FetchRequest,
    FetchResponse,
    SearchRequest,
    SearchResponse,
)
from backend.ingest.ingest import ingest_corpus
from backend.providers.base import BaseProvider
from backend.rag.citations import build_citations
from backend.rag.index import get_chunk_by_id
from backend.rag.retrieve import search

router = APIRouter(prefix="/api")

# The provider is injected at app startup via ``set_provider``.
_provider: BaseProvider | None = None

# Default chapters directory (can be overridden for tests).
_CHAPTERS_DIR = Path(__file__).resolve().parent.parent.parent / "textbook" / "chapters"


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


@router.get("/chapters", response_model=ChapterListResponse)
def api_list_chapters() -> ChapterListResponse:
    docs = ingest_corpus(_CHAPTERS_DIR)
    summaries = [
        ChapterSummary(
            chapter_number=d["chapter_number"],
            chapter_title=d["chapter_title"],
            part_title=d.get("part_title"),
            source_path=d["source_path"],
        )
        for d in docs
    ]
    return ChapterListResponse(chapters=summaries)


@router.get("/chapters/{chapter_number}", response_model=ChapterDetailResponse)
def api_get_chapter(chapter_number: int) -> ChapterDetailResponse:
    docs = ingest_corpus(_CHAPTERS_DIR)
    for d in docs:
        if d["chapter_number"] == chapter_number:
            return ChapterDetailResponse(
                chapter_number=d["chapter_number"],
                chapter_title=d["chapter_title"],
                part_title=d.get("part_title"),
                source_path=d["source_path"],
                text=d["text"],
            )
    raise HTTPException(status_code=404, detail=f"Chapter {chapter_number} not found")
