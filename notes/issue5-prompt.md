You are working in my `textbook-rag` repository.

Context:
- Shared retrieval backend for both browser app and MCP.
- Follow CLAUDE.md and docs/architecture.md.
- Implementation phases: docs/implementation-plan.md.

GitHub Issue:
- Title: [FEAT] Implement retrieval API (search, fetch, answer)
- Milestone: M3 – Retrieval
- Labels: type:feature, area:backend, area:retrieval, priority:high

Goal
Expose REST endpoints for search, fetch, and answer that use the shared retrieval backend.

Why it matters
The browser app and MCP server will both rely on these APIs to access the textbook corpus.

Requirements
- Add endpoints under `/api`:
  - `POST /api/search` → given a query, return top‑k chunks + metadata.
  - `POST /api/fetch` → given a `chunk_id`, return the full chunk + metadata.
  - `POST /api/answer` → given a query, run retrieval + model provider and return an answer + citations.
- Use a provider abstraction for generation.

Acceptance criteria
- `/api/search` returns ranked chunks with metadata for a non-empty query.
- `/api/fetch` returns a chunk for a valid `chunk_id`, and a clear error otherwise.
- `/api/answer` returns:
  - `answer` string,
  - `citations` list referencing underlying chunks.
- Pytests cover happy paths, empty/invalid queries, and response schemas.

Scope and constraints
- Primary folders: backend/api/, backend/rag/, backend/providers/, backend/tests/
- Avoid: docs/, frontend/, .github/
- Retrieval logic must be shared and provider-agnostic.

Instructions for you
1. Read:
   - README.md
   - CLAUDE.md
   - docs/architecture.md
   - Existing retrieval + provider code.
2. Propose a PLAN:
   - which FastAPI router(s) to create/extend,
   - request/response Pydantic models,
   - how `/api/answer` will call retrieval + a stub provider,
   - tests to add for each endpoint.
3. Wait for approval.
4. Implement:
   - the endpoints,
   - provider abstraction wiring,
   - tests using TestClient.
5. Summarize changes and show pytest command.

Do not modify files until I approve your plan.
