You are working in my `textbook-rag` repository.

Context:
- This project is a Markdown-native RAG system for a 35-chapter textbook.
- Follow the rules in `CLAUDE.md` (shared retrieval backend, read-only MCP, preserve metadata and citations).
- The architecture is described in `docs/architecture.md`.
- The implementation phases are described in `docs/implementation-plan.md`.

GitHub Issue:
- Title: [FEAT] Implement chapter-aware chunking
- Milestone: M2 – Ingestion
- Labels: type:feature, area:ingest, area:retrieval, priority:high

Goal
Split ingested Markdown documents into semantically meaningful chunks with stable IDs and metadata.

Why it matters
Good chunking is critical for retrieval quality and for producing accurate citations back to the textbook.

Requirements
- Implement a chunking function that:
  - Respects Markdown headings where possible.
  - Applies a size limit (e.g. character or token budget) with optional overlap.
  - Produces chunk IDs that are stable and human-readable (e.g. `ch01-0000`).
- Attach metadata per chunk:
  - `chunk_id`
  - `source_path`
  - `chapter_title` (if derivable from the top heading)
  - `section_title` (if derivable from subheadings)

Acceptance criteria
- Chunking function takes a document and returns a list of chunks with metadata.
- Each chunk has a unique `chunk_id` within its file.
- Chunk size stays under the configured limit.
- Pytests cover:
  - multiple chunks for a long document,
  - metadata presence (`chunk_id`, `source_path`),
  - basic heading-respecting behavior.

Scope and constraints
- Primary folders to touch: backend/ingest/, backend/rag/, backend/tests/
- Folders to avoid unless necessary: docs/, frontend/, .github/
- Keep logic clear and simple; optimize later if needed.

Instructions for you
1. Read:
   - README.md
   - CLAUDE.md
   - docs/architecture.md
   - docs/implementation-plan.md
   - Existing ingestion code in backend/ingest/
2. Propose a short, step-by-step implementation PLAN:
   - file(s) to create/modify,
   - chunking algorithm (how you respect headings + size limits),
   - chunk metadata structure,
   - tests you will add.
3. Wait for my approval.
4. After approval, implement:
   - chunking function(s),
   - any needed changes to ingestion to call the chunker,
   - tests in backend/tests/.
5. Finish with a summary and the pytest command I should run.

Do not edit files until I approve your plan.
