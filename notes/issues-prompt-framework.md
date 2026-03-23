You are working in my `textbook-rag` repository.

Context:
- This project is a Markdown-native RAG system for a 35-chapter textbook.
- Follow the rules in `CLAUDE.md` (shared retrieval backend, read-only MCP, preserve metadata and citations).
- The architecture and module layout are described in `docs/architecture.md`.
- The implementation phases and priorities are described in `docs/implementation-plan.md`.

GitHub Issue:
- Title: {{ISSUE_TITLE}}
- Milestone: {{MILESTONE}}
- Labels: {{LABELS}}

Goal
{{GOAL}}

Why it matters
{{WHY_IT_MATTERS}}

Requirements
{{REQUIREMENTS_LIST}}

Acceptance criteria
{{ACCEPTANCE_CRITERIA_LIST}}

Scope and constraints
- Primary folders to touch: {{PRIMARY_FOLDERS}}
- Folders to avoid unless absolutely necessary: {{AVOID_FOLDERS}}
- Keep retrieval logic shared and provider-agnostic.
- MCP tools must remain read-only.

Instructions for you
1. Read the relevant docs and existing code:
   - `README.md`
   - `CLAUDE.md`
   - `docs/prd.md`
   - `docs/architecture.md`
   - `docs/implementation-plan.md`
   - Any existing modules under {{PRIMARY_FOLDERS}}.
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which new files/modules you will create,
   - which existing files you will modify,
   - how you will structure the key functions/classes,
   - how you will test the changes.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - add or update the necessary files,
   - keep changes focused on this issue’s scope,
   - add or update tests to cover the new behavior.
5. At the end, summarize:
   - what changed (files and key functions),
   - which tests you added/updated,
   - the exact commands I should run to verify (e.g. pytest, npm scripts).

Do not start editing files until I explicitly approve your plan.
