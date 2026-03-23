You are working in my `textbook-rag` repository.

Context:
- Markdown-native RAG system with a shared retrieval backend.
- Follow CLAUDE.md rules (shared retrieval, read-only MCP, preserve metadata/citations).
- Architecture and phases: docs/architecture.md, docs/implementation-plan.md.

GitHub Issue:
- Title: [FEAT] Build embedding and indexing pipeline
- Milestone: M2 – Ingestion
- Labels: type:feature, area:backend, area:retrieval, priority:high

Goal
Create a pipeline that embeds chunks and stores them in a vector index with associated metadata.

Why it matters
This is the backbone of retrieval: without an index, we cannot efficiently search the textbook corpus.

Requirements
- Choose a vector store for v1 (e.g. Qdrant, Chroma, pgvector).
- Implement an indexing script/command that:
  - Runs ingestion + chunking.
  - Embeds each chunk.
  - Writes embeddings and metadata to the vector store.
- Design for re-runs without corrupting or duplicating the index.

Acceptance criteria
- A single function/command indexes all chunks from `textbook/`.
- Indexed chunks can be queried by `chunk_id`.
- Indexing can be re-run without duplicating entries.
- At least one test verifies the index is populated from a small test corpus.

Scope and constraints
- Primary folders: backend/rag/, backend/ingest/, backend/tests/
- Avoid: frontend/, docs/, .github/
- Retrieval backend must remain model-provider-agnostic.

Instructions for you
1. Read:
   - CLAUDE.md
   - docs/architecture.md
   - Current ingestion + chunking code.
2. Propose a PLAN:
   - which vector store you’ll use for v1,
   - which files/modules you’ll create (e.g. backend/rag/index.py),
   - how you’ll structure the indexing API (functions/CLI),
   - how you will test indexing.
3. Wait for my approval.
4. Implement:
   - indexing pipeline from ingestion → chunking → embeddings → index,
   - a simple way to re-run indexing safely,
   - tests for a small test corpus.
5. Summarize changes and give pytest command(s) to run.

Wait for my approval before editing files.
