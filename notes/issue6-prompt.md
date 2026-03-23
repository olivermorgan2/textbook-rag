You are working in my `textbook-rag` repository.

Context:
- Citations are critical for trust and verification.
- Follow CLAUDE.md; keep citations consistent and non-fabricated.

GitHub Issue:
- Title: [FEAT] Implement citation formatting utility
- Milestone: M3 – Retrieval
- Labels: type:feature, area:retrieval, priority:high

Goal
Create a utility that turns chunk metadata into human-readable citations.

Why it matters
Citations are essential for trust and for mapping answers back to the textbook.

Requirements
- Given a list of retrieved chunks, produce a list of citation objects including:
  - `chunk_id`
  - `chapter_title`
  - `section_title`
  - `source_path`
- Optionally support a formatted string representation for UI.

Acceptance criteria
- Citation utility produces citation objects for each result chunk.
- Required metadata (`chunk_id`, `source_path`) is present in normal cases.
- Tests cover field mapping and behavior with partially missing metadata.

Scope and constraints
- Primary folders: backend/rag/, backend/tests/
- Avoid: frontend/ (will just consume the resulting citations), docs/, .github/

Instructions for you
1. Read:
   - CLAUDE.md (citation rules),
   - any existing retrieval response structures.
2. Propose a PLAN:
   - where to place the utility (e.g. backend/rag/citations.py),
   - function signatures,
   - handling of missing metadata,
   - tests you will add.
3. Wait for approval.
4. Implement the utility and tests.
5. Summarize changes and pytest command.

Wait for my approval before implementing.
