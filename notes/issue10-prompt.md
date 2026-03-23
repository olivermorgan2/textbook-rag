You are working in my `textbook-rag` repository.

Context:
- We need a basic evaluation harness for retrieval and citations.
- docs/evaluation.md describes the metrics and dataset format.

GitHub Issue:
- Title: [EVAL] Add evaluation harness for retrieval and citations
- Milestone: M6 – Evaluation & CI
- Labels: type:eval, area:ci, priority:medium

Goal
Add a basic evaluation harness to measure retrieval quality and citation behavior using a small benchmark set.

Why it matters
We need an objective way to detect regressions in retrieval and citation quality as the system evolves.

Requirements
- Create `eval/questions.json` with a small set of benchmark questions and expected sources.
- Implement an evaluation script (e.g. `eval/run_eval.py`) that:
  - Loads the questions.
  - Runs retrieval for each question.
  - Computes simple metrics (e.g. retrieval @k, citation coverage).
- Save results to a file (e.g. `eval/results/*.json`).

Acceptance criteria
- `eval/questions.json` exists with at least a few test questions.
- Running the eval script produces a metrics output file.
- Metrics include at least retrieval @k and citation coverage.
- Instructions for running the eval are added to `docs/evaluation.md`.

Scope and constraints
- Primary folders: eval/, backend/rag/ (for retrieval calls), docs/
- Avoid: frontend/, backend/providers/ (no need to involve generation for v1 of eval).

Instructions for you
1. Read:
   - docs/evaluation.md,
   - retrieval API/function interfaces.
2. Propose a PLAN:
   - structure of `eval/questions.json`,
   - the evaluation script design,
   - metrics to compute and how to output them.
3. Wait for approval.
4. Implement:
   - questions file,
   - evaluation script,
   - small documentation update.
5. Summarize changes and the exact command to run the eval.

Wait for my approval before implementing.
