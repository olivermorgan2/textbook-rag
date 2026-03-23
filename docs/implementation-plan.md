
***

## `docs/implementation-plan.md`

```md
# Implementation Plan

## Phase 0: Foundation

- Create repo structure for `backend/`, `frontend/`, `textbook/`, `docs/`, `eval/`, `.github/`.
- Add `README.md`, `CLAUDE.md`, and core docs.
- Add issue and PR templates.

## Phase 1: Ingestion

- Implement Markdown parsing.
- Implement chapter/section-aware chunking.
- Attach metadata to every chunk.
- Add tests for ingestion and chunking.

## Phase 2: Indexing

- Choose a vector DB (e.g. Qdrant OSS or pgvector).
- Implement embedding and indexing.
- Implement idempotent reindex command.
- Add tests for index creation and updates.

## Phase 3: Retrieval API

- Implement `/api/search` to return top‑k chunks.
- Implement `/api/fetch` to return full chunk content.
- Implement `/api/answer` that calls retrieval + generation.
- Implement citation formatting utility.
- Add tests for API behavior.

## Phase 4: Browser app

- Set up React + Vite frontend.
- Add chat UI for asking questions.
- Add citation panel.
- Add chapter browser (list chapters, open chapter view).

## Phase 5: MCP server

- Implement read‑only MCP server wrapping retrieval functions.
- Expose tools: `search_textbook`, `fetch_chunk`, `list_chapters`, `get_chapter`.
- Add tests for MCP tool schemas and basic outputs.

## Phase 6: Evaluation

- Create `eval/questions.json` with a benchmark set.
- Implement evaluation script (retrieval precision, citation coverage, latency).
- Add docs on how to run evaluation.

## Phase 7: CI and automation

- Add GitHub Actions for:
  - backend tests,
  - frontend build,
  - linting.
- Optionally add Claude Code GitHub Actions workflow.
- Ensure PRs run CI before merge.

## Phase 8: Packaging and documentation

- Polish `README.md`.
- Add `docs/deployment.md`.
- Add contribution guidelines.
- Ensure everything works from `git clone` + documented commands.
