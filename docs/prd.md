# Product Requirements Document

## Product name

Textbook RAG Platform

## Summary

A GitHub-hosted, Markdown-native RAG platform for querying a 35‑chapter textbook through:

- A browser app for interactive question answering.
- An MCP server for LLM clients such as Claude, ChatGPT, and Gemini.

The core value is one shared retrieval backend usable by both humans and AI tools.

## Problem statement

Long Markdown textbooks are hard to search, compare, and cite. Users may have different clients (browser vs. LLM) but need consistent, citation-backed answers from the same corpus.

## Goals

- Ingest and index a 35‑chapter textbook from `.md` files.
- Enable browser-based question answering and chapter browsing.
- Enable MCP-based retrieval for LLM clients.
- Ground answers in retrieved passages with citations.
- Make the repository easy to fork for other Markdown corpora.

## Non-goals

- Training or fine-tuning models.
- OCR or non-Markdown ingestion in v1.
- Web browsing as part of the RAG flow.
- Multi-tenant billing or complex auth in v1.
- Editing textbook content through the app.

## Target users

- **Readers:** want quick answers and citations.
- **Researchers:** need reliable references across chapters.
- **Developers:** want a reusable RAG starter repo for Markdown corpora.
- **AI users:** want assistants to answer from the textbook via MCP.

## Core user journeys

1. Reader uses browser to ask a question, sees answer + citations, and opens source chapter.
2. LLM client uses MCP tools to search, fetch, and answer from the same corpus.
3. Developer forks the repo, swaps in their own `.md` files, reindexes, and deploys.

## Scope

### In scope

- Markdown ingestion.
- Chunking, embeddings, vector indexing.
- Retrieval and answer generation with citations.
- Browser app (chat + chapter browsing).
- MCP server (read‑only tools).
- Evaluation scripts and basic metrics.
- CI workflows for tests and build.

### Out of scope

- Fine-tuning.
- Advanced analytics dashboards.
- Complex access control and multi-tenant features.
- Non-text modalities (audio/video).

## Functional requirements

1. Ingest `.md` files from a configured directory.
2. Preserve chapter and section metadata.
3. Chunk content with logical boundaries and size limits.
4. Embed chunks and store them with metadata.
5. Support semantic search over the corpus.
6. Return top‑k chunks with metadata for each query.
7. Generate answers using retrieved context and a configurable model provider.
8. Show citations in the browser app.
9. Expose retrieval via MCP tools.
10. Support reindexing on file changes.
11. Support at least one local and one deployable configuration.
12. Provide basic logs and evaluation scripts.

## Non-functional requirements

- Interactive latency for typical queries.
- Reproducible from `git clone` with documented steps.
- Secure by default; read‑only corpus.
- Model-agnostic retrieval backend.
- Easy to fork and customize.

## Architecture (high level)

Layers:

1. **Content:** Markdown chapters in `textbook/`.
2. **Ingestion:** parsing, chunking, metadata extraction.
3. **Index:** embeddings and vector storage.
4. **Retrieval:** semantic search, ranking, metadata.
5. **Generation:** LLM provider using retrieved context.
6. **Clients:** browser app and MCP server over the same backend.

## Data model (chunk)

- `chunk_id`
- `doc_id` or `file_name`
- `chapter_number`
- `chapter_title`
- `section_title`
- `source_path`
- `text`
- `embedding`
- `created_at`
- `updated_at`

## Success metrics

- Time to first answer from fresh install.
- Retrieval precision/recall on benchmark questions.
- Citation coverage rate.
- Grounded answer rate (answers supported by retrieved text).
- Number of forks/adopters.

## Risks

- Poor chunking → weak retrieval.
- Citation bugs → reduced trust.
- Stale index after content changes.
- Model-provider lock‑in if abstraction is weak.

## Release plan

- **v1:** ingestion, indexing, retrieval API, browser app, MCP scaffold, basic evaluation, CI.
- **v1.1:** hybrid retrieval, better evaluation, multiple providers, improved UI.
- **v2:** multi-corpus support, stronger auth, analytics, deployment templates.
