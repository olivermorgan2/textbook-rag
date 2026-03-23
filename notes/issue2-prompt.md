You are working in my `textbook-rag` repository.

Context:
- This project is a Markdown-native RAG system for a 35-chapter textbook.
- Each chapter has a `.md` content file and a matching metadata `.json` file (e.g. `chapter_10_sti_bloodborne.md` and `chapter_10_metadata.json` in `textbook/chapters/`).
- Follow the rules in `CLAUDE.md` (shared retrieval backend, read-only MCP, preserve metadata and citations).
- The architecture and phases are described in `docs/architecture.md` and `docs/implementation-plan.md`.

GitHub Issue:
- Title: [FEAT] Parse Markdown textbook files
- Milestone: M2 – Ingestion
- Labels: type:feature, area:ingest, area:backend, priority:high

Goal
Implement a basic ingestion step that reads paired `.md` and `.json` textbook files for each chapter and exposes them as in-memory documents with chapter-level metadata.

Why it matters
All downstream chunking, indexing, and retrieval depend on reliable access to the raw Markdown content and the rich chapter metadata defined in the JSON files.

Requirements
- Read all `.md` files under `textbook/chapters/`.
- For each chapter:
  - Load the Markdown file (e.g. `chapter_10_sti_bloodborne.md`).
  - Load the corresponding metadata JSON file (e.g. `chapter_10_metadata.json`).
- Match `.md` and `.json` by chapter number.
- For each matched pair, create a document object/dict that includes at least:
  - `chapter_number`
  - `chapter_title`
  - `part_number` and `part_title` (if available)
  - `source_path` (path to the `.md` file)
  - `text` (full Markdown content)
  - `metadata` (the full parsed JSON object)
- Handle missing pairs gracefully:
  - If `.md` exists but `.json` is missing → ingest with minimal metadata and log a warning.
  - If `.json` exists but `.md` is missing → log a warning and skip.

Acceptance criteria
- A function (e.g. `ingest_corpus`) loads all chapter `.md` and `.json` pairs from `textbook/chapters/`.
- Each returned document includes: `chapter_number`, `chapter_title`, `source_path`, `text`, and `metadata`.
- Markdown and JSON are correctly matched by chapter number for the provided example files (e.g. chapter 10).
- Missing pairs are handled without crashing, with a clear log or warning.
- There is at least one pytest that:
  - creates a small temporary `textbook/chapters/` with 1–2 chapter pairs,
  - runs `ingest_corpus`,
  - asserts that the document objects contain both Markdown text and JSON metadata.

Scope and constraints
- Primary folders to touch: backend/ingest/, backend/tests/
- Folders to avoid unless absolutely necessary: docs/, frontend/, .github/
- Keep the ingestion API simple and easy to reuse in indexing and evaluation.

Instructions for you
1. Read:
   - README.md
   - CLAUDE.md
   - docs/prd.md
   - docs/architecture.md
   - docs/implementation-plan.md
   - Any existing modules under backend/ingest/ and backend/tests/
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files/modules you will create or modify,
   - how you will parse chapter numbers and match `.md` to `.json`,
   - the shape of the document objects returned by `ingest_corpus`,
   - how you will test it with pytest (using tmp_path and small fake files).
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - add or update the necessary files under backend/ingest/,
   - add tests under backend/tests/,
   - ensure imports are consistent.
5. At the end, summarize:
   - what changed (files and key functions),
   - which tests you added/updated,
   - the exact pytest command I should run to verify.

Do not start editing files until I explicitly approve your plan.
