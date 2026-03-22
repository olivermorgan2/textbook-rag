# Issue Process

## Purpose

This document explains how we use GitHub issues, labels, milestones, and Claude Code to manage work on the Textbook RAG Platform.

## Templates

We use GitHub issue templates for:

- Feature requests.
- Bugs.
- Tasks.
- Evaluation work.

Each issue should have:

- A clear goal.
- Why it matters.
- A proposed approach (optional).
- Acceptance criteria.
- Dependencies.
- Notes / references.

## Labels

Suggested label families:

- **Type:** `type:feature`, `type:bug`, `type:task`, `type:docs`, `type:eval`.
- **Area:** `area:backend`, `area:frontend`, `area:ingest`, `area:retrieval`, `area:mcp`, `area:ci`, `area:docs`.
- **Priority:** `priority:high`, `priority:medium`, `priority:low`.
- **Status:** `status:blocked`, `status:ready`, `status:review`.

## Milestones

Suggested milestones:

- `M1 – Scaffold`
- `M2 – Ingestion`
- `M3 – Retrieval`
- `M4 – Browser UI`
- `M5 – MCP`
- `M6 – Evaluation & CI`

## Project board

We use a GitHub Project board with columns:

- Backlog
- Ready
- In progress
- Review
- Done

Issues move across the board as work progresses.

## Definition of ready

An issue is ready when:

- The goal is clearly described.
- Scope is small enough for a single branch / PR.
- Acceptance criteria are testable.
- Dependencies are known.

## Definition of done

An issue is done when:

- The feature/bugfix is implemented.
- Tests pass locally and in CI.
- Docs are updated if needed.
- Citations remain correct (for retrieval-related issues).
- The issue and associated PR are closed.

## Claude Code usage

- Use Claude Code for implementation and refactoring.
- Use Planning Mode for multi‑file changes.
- Give Claude one issue at a time with context (PRD, architecture, relevant files).
- Keep sessions focused to avoid scope creep.

Suggested prompt shape:

> Here is issue #X with acceptance criteria. Here are the relevant files. Please propose a plan, wait for my approval, then implement and update tests.

## Evaluation issues

Evaluation issues should:

- Reference the benchmark dataset.
- Specify which metrics to run (retrieval@k, grounding, citations, latency).
- Include acceptance thresholds where applicable.
