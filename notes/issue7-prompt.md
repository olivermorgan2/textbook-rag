You are working in my `textbook-rag` repository.

Context:
- React + Vite frontend talking to FastAPI backend.
- Frontend should be minimal but usable.

GitHub Issue:
- Title: [FEAT] Build browser chat UI
- Milestone: M4 – Browser UI
- Labels: type:feature, area:frontend, priority:high

Goal
Create a minimal frontend that lets a user ask questions and see answers + citations.

Why it matters
This is the primary human-facing interface for interacting with the textbook.

Requirements
- Use React + Vite.
- Implement:
  - Text area for entering a question.
  - Submit button to call `/api/answer`.
  - Area to display the answer.
  - Area to display citations (chapter, section, file).

Acceptance criteria
- User can type a question and submit it.
- UI displays the answer from `/api/answer`.
- UI shows a list of citations for the answer.
- Basic error states (e.g. backend unreachable) are handled.

Scope and constraints
- Primary folders: frontend/, frontend/src/
- Avoid: backend/, docs/, .github/
- Respect existing Vite config and API paths (`/api`).

Instructions for you
1. Read:
   - README.md (local dev notes),
   - any existing frontend files.
2. Propose a PLAN:
   - components to create (e.g. App, AnswerPanel, CitationsPanel),
   - how to call `/api/answer` and handle loading/errors,
   - basic layout and styling approach.
3. Wait for approval.
4. Implement the UI and any needed CSS.
5. Summarize changes and commands to run the frontend dev server.

Do not edit files until I approve your plan.
