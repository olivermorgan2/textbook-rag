You are working in my `textbook-rag` repository.

Context:
- Browser app currently focuses on Q&A.
- We want a simple chapter browser panel as well.

GitHub Issue:
- Title: [FEAT] Add chapter browser UI
- Milestone: M4 – Browser UI
- Labels: type:feature, area:frontend, priority:medium

Goal
Provide a simple way to browse chapters and sections directly in the browser app.

Why it matters
Users also want to navigate the textbook manually alongside asking questions.

Requirements
- Implement a panel that:
  - Lists available chapters (from backend or a simple config).
  - Allows selecting a chapter to view its content or a summary.
- Show basic chapter metadata (title, number).

Acceptance criteria
- Chapter list is visible and scrollable.
- Selecting a chapter shows its content or at least a placeholder.
- The UI remains usable on a standard laptop screen.

Scope and constraints
- Primary folders: frontend/src/
- Avoid: backend/ (unless you explicitly need a simple `/api/chapters` and we agree on that), docs/, .github/

Instructions for you
1. Read:
   - Existing frontend layout and components.
2. Propose a PLAN:
   - how to represent chapters (static config vs backend endpoint),
   - components to add,
   - how the chapter panel will coexist with the chat UI.
3. Wait for approval.
4. Implement the chapter browser UI.
5. Summarize changes and commands to run frontend.

Wait for my approval before coding.
