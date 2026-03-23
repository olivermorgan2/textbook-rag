You are working in my `textbook-rag` repository.

Context:
- MCP should expose read-only tools over the same retrieval backend.
- Follow CLAUDE.md: MCP tools must be read-only.

GitHub Issue:
- Title: [FEAT] Scaffold MCP server (read-only tools)
- Milestone: M5 – MCP
- Labels: type:feature, area:mcp, area:backend, priority:high

Goal
Create a read-only MCP server that exposes search/fetch/list-chapter tools backed by the same retrieval logic as the REST API.

Why it matters
This enables LLM clients (Claude, ChatGPT, Gemini, etc.) to query the textbook corpus via standard tools.

Requirements
- Implement an MCP server entry point (e.g. backend/mcp/server.py).
- Expose tools such as:
  - `search_textbook(query, top_k)`
  - `fetch_chunk(chunk_id)`
  - `list_chapters()`
- Tools must be read-only and reuse the same retrieval backend.

Acceptance criteria
- MCP server can start locally and respond to tool calls.
- Tools reuse the same retrieval backend functions as the REST API.
- At least one test verifies the shape of tool responses.

Scope and constraints
- Primary folders: backend/mcp/, backend/rag/, backend/api/, backend/tests/
- Avoid: frontend/, docs/, .github/
- Do not add write-capable tools.

Instructions for you
1. Read:
   - CLAUDE.md (MCP section),
   - Existing retrieval API functions.
2. Propose a PLAN:
   - MCP server structure,
   - how tools will call existing retrieval functions,
   - tests you’ll add.
3. Wait for approval.
4. Implement the MCP scaffold and tests.
5. Summarize changes and how to start the MCP server locally.

Wait for my approval before editing.
