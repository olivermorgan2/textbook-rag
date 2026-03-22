# Architecture

## Overview

The Textbook RAG Platform uses one shared retrieval backend to serve:

- A browser app.
- An MCP server for LLM clients.

The same ingestion, indexing, and retrieval logic is reused across both.

## Layers

1. **Content layer**
   - Raw `.md` chapters in `textbook/`.
   - One file per chapter or major section.

2. **Ingestion layer**
   - Parses Markdown headings and text.
   - Produces structured chunks with metadata.
   - Lives in `backend/ingest/`.

3. **Index layer**
   - Embeds chunks using an embedding model.
   - Stores embeddings + metadata in a vector DB.
   - Lives in `backend/rag/`.

4. **Retrieval layer**
   - Given a query, returns top‑k relevant chunks.
   - May use semantic or hybrid (semantic + keyword) search.
   - Lives in `backend/rag/`.

5. **Generation layer**
   - Uses a provider (Claude, Gemini, ChatGPT-compatible, or local) to generate answers from retrieved context.
   - Lives in `backend/providers/`.

6. **Application layer**
   - REST API for search/answer.
   - Lives in `backend/api/`.

7. **Clients**
   - **Frontend:** React + Vite app in `frontend/`.
   - **MCP server:** read‑only tools mapping to retrieval functions in `backend/mcp_*`.

## Data flow

1. Markdown files placed in `textbook/`.
2. Ingestion script parses and chunks chapters, adding metadata.
3. Indexing script embeds chunks and writes them to the vector store.
4. User asks a question (browser or MCP).
5. Retrieval finds top‑k chunks and their metadata.
6. Provider generates an answer with citations.
7. Client displays answer and source passages.

## Key design decisions

- **Single retrieval backend** for both clients.
- **Read‑only MCP tools** to avoid accidental content modification.
- **Metadata-rich chunks** to support robust citations.
- **Provider abstraction layer** so you can swap models without changing retrieval.

## Module layout (planned)

```text
backend/
  ingest/
    ingest.py
    chunker.py
  rag/
    index.py
    retrieve.py
  providers/
    base.py
    claude.py
    openai.py
    gemini.py
  api/
    api.py
    schemas.py
  mcp/
    server.py
    tools.py
frontend/
  src/
    App.jsx
    main.jsx
    components/
