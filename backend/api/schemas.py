"""Pydantic models for the retrieval API."""

from __future__ import annotations

from pydantic import BaseModel, Field


# -- Requests ---------------------------------------------------------------

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query text")
    top_k: int = Field(5, ge=1, le=50, description="Number of results")


class FetchRequest(BaseModel):
    chunk_id: str = Field(..., min_length=1, description="Chunk identifier")


class AnswerRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question to answer")
    top_k: int = Field(5, ge=1, le=50, description="Number of chunks for context")


# -- Responses ---------------------------------------------------------------

class ChunkResult(BaseModel):
    chunk_id: str
    text: str
    source_path: str
    chapter_title: str
    section_title: str
    score: float | None = None


class SearchResponse(BaseModel):
    results: list[ChunkResult]


class FetchResponse(BaseModel):
    chunk: ChunkResult


class CitationItem(BaseModel):
    chunk_id: str
    chapter_title: str
    section_title: str
    source_path: str


class AnswerResponse(BaseModel):
    answer: str
    citations: list[CitationItem]


class ChapterSummary(BaseModel):
    chapter_number: int
    chapter_title: str
    part_title: str | None = None
    source_path: str


class ChapterListResponse(BaseModel):
    chapters: list[ChapterSummary]


class ChapterDetailResponse(BaseModel):
    chapter_number: int
    chapter_title: str
    part_title: str | None = None
    source_path: str
    text: str


class ErrorResponse(BaseModel):
    detail: str
