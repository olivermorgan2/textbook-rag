# CLAUDE.md

## Project

Textbook RAG Platform

## Purpose

Build a Markdown-native RAG system for a 35‑chapter textbook with:

- A browser app for human users.
- An MCP server for AI clients (Claude, ChatGPT, Gemini, etc.).

The **retrieval backend must be shared** between all clients.

## What you should optimize for

- Keep retrieval logic in one place and reuse it.
- Preserve citations and source metadata.
- Avoid unnecessary abstractions.
- Keep the codebase easy to fork and extend.
- Prefer small, incremental changes.

## Architecture rules

- `textbook/` – Markdown source chapters.
- `backend/ingest/` – Markdown parsing, chunking, metadata.
- `backend/rag/` – Embeddings, vector index, retrieval.
- `backend/api/` – REST API (`/api/search`, `/api/fetch`, `/api/answer`).
- `backend/providers/` – Model provider integrations.
- `backend/mcp_*` – MCP server / tools (read‑only).
- `frontend/` – Browser app (React + Vite).
- `eval/` – Benchmarks and scripts.
- `docs/` – Product and architecture docs.
- `.github/` – CI workflows and templates.

## Working rules

- Do **not** edit textbook content unless explicitly asked.
- MCP tools must be **read‑only** (no write access to the corpus or index).
- Preserve `chapter`, `section`, and `source_path` metadata on every chunk.
- Retrieval logic should be provider‑agnostic.
- The browser app and MCP server must use the same retrieval functions.

## Chunking rules

- Respect Markdown heading structure.
- Chunk by chapter/section with a token/character limit and optional overlap.
- Do not produce extremely small chunks (they should be semantically meaningful).
- Ensure each chunk includes meta `chunk_id`, `chapter_title`, `section_title`, `source_path`.

## Retrieval rules

- Implement semantic search; add keyword/hybrid when possible.
- Always return chunk metadata with results.
- When generating answers, include citations that map back to specific chunks.
- Never fabricate citations.

## Model/provider rules

- Provider adapters must implement a common interface (e.g. `generate(query, context)`).
- The retrieval layer must not depend on a specific model vendor.
- Switching providers must **not** require reindexing.

## MCP rules

- Expose tools like `search_textbook`, `fetch_chunk`, `list_chapters`, `get_chapter`.
- Tools must be read‑only.
- Use the same retrieval functions already used by the REST API.
- Keep tool schemas simple and deterministic.

## Browser app rules

- Must support question answering and show citations clearly.
- Should support basic chapter browsing.
- Keep UX simple and fast; no complex auth for v1.

## Testing rules

- Add tests for ingestion, chunking, indexing, retrieval, citation formatting, and API behavior.
- Add tests for MCP tools (schemas and basic outputs).
- Add at least one evaluation script in `eval/`.

## Documentation rules

- `README.md` – high‑level overview and quickstart.
- `docs/prd.md` – product requirements.
- `docs/architecture.md` – architecture and module layout.
- `docs/implementation-plan.md` – phases and tasks.
- `docs/user-stories.md` – user stories.
- `docs/issue-process.md` – how issues, labels, and milestones work.
- `docs/evaluation.md` – how we evaluate the system.

## Claude Code workflow

- Use Planning Mode for multi‑file or multi‑layer changes.
- Keep each session focused on a single GitHub issue.
- Update docs when architecture or behavior changes.
- If a plan drifts, stop, re‑plan, then continue.

## Definition of done

A change is done when:

- It satisfies the associated issue’s acceptance criteria.
- Tests pass locally and in CI.
- Docs are updated if necessary.
- Citations remain correct and retrievable.
