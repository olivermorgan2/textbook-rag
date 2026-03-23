# Textbook RAG Platform

A Markdown-native Retrieval Augmented Generation (RAG) system for querying a 35‑chapter textbook through:

- A browser app.
- An MCP server for AI clients such as Claude, ChatGPT, Gemini, and others.

The core idea: **one shared retrieval backend** that ingests `.md` chapters, indexes them, and serves both humans (via a web UI) and LLMs (via tools/MCP).

## Goals

- Ingest and index a 35‑chapter textbook stored as Markdown.
- Provide a browser interface for question answering and chapter browsing.
- Provide an MCP interface so LLM clients can retrieve from the same corpus.
- Ground all answers in retrieved passages with citations.
- Make the repo easy to fork for other Markdown corpora.

## Repository structure (planned)

```text
textbook-rag/
├─ textbook/              # Markdown chapters
├─ backend/               # FastAPI app, ingestion, retrieval, MCP wrapper
├─ frontend/              # React + Vite app
├─ mcp/                   # MCP configuration / integration (optional)
├─ eval/                  # Evaluation data and scripts
├─ docs/                  # Product and architecture docs
├─ .github/               # CI workflows and templates
├─ CLAUDE.md              # Project rules for Claude Code
└─ README.md
Key documents
	•	 docs/prd.md  – Product requirements.
	•	 docs/architecture.md  – System design.
	•	 docs/implementation-plan.md  – Phased build plan.
	•	 docs/user-stories.md  – User stories.
	•	 docs/issue-process.md  – How we use GitHub issues and Claude Code.
	•	 docs/evaluation.md  – How we evaluate RAG quality.
	•	 docs/deployment.md  – Notes on local and production deployment.
High-level architecture
	1.	Ingestion Parse  .md  chapters, extract headings, chunk text, and attach metadata such as chapter number, chapter title, section title, and source path.
	2.	Indexing Embed chunks with an embedding model and store embeddings + metadata in a vector database (for example, Qdrant or pgvector).
	3.	Retrieval Given a user question, perform semantic (and optionally hybrid) search over the index to return top‑k relevant chunks with their metadata.
	4.	Generation Call a model provider (Claude, Gemini, ChatGPT-compatible, or a local model) with the question plus retrieved chunks to generate a grounded answer.
	5.	Browser app A React/Vite front end that sends questions to the backend, displays the answer, and shows citations back to the original Markdown chunks.
	6.	MCP server A read‑only MCP integration that exposes search/fetch tools wrapping the same retrieval backend, so AI clients can query the textbook without direct access to the files.
Local development (planned)
Backend (FastAPI)

cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

**Backend will be available at:
	•	 http://localhost:8000 
Frontend (React + Vite)

cd frontend
npm install
npm run dev

Frontend will be available at (by default):
	•	 http://localhost:5173 
The Vite dev server will proxy  /api  requests to the backend during development.
Docker (optional)
Once Dockerfiles and  docker-compose.yml  are in place, you can run:


docker compose up --build

Expected ports:
	•	Backend:  http://localhost:8000 
	•	Frontend:  http://localhost:5173 
Environment configuration
	•	Use  .env  (not committed) or environment variables for secrets and configuration (LLM keys, vector DB URL, etc.).
	•	Keep a non-sensitive  .env.example  in the repo to document required variables.
	•	Do not commit real secrets.
Status
This repository is in early development. The main artifacts to consult are:
	•	 docs/implementation-plan.md  – for the build phases and order of work.
	•	The GitHub Project board – for live issue status and current focus.
	•	 CLAUDE.md  – for project rules and how to work with this repo using Claude Code.
Contributing
For now, contributions are expected to follow this pattern:
	1.	Open or pick an issue with clear acceptance criteria.
	2.	Use Claude Code (or your editor) to implement the change in a feature branch.
	3.	Add or update tests.
	4.	Run tests locally.
	5.	Open a pull request and ensure CI passes.
	6.	Update docs if architecture or behavior changed.
The guiding principle is: keep retrieval logic shared, keep MCP read‑only, and always preserve correct citations back to the textbook.

