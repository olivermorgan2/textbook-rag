# User Stories

## Epic A: Reader experience

1. As a reader, I want to ask a question about any chapter so I can get an immediate answer.
2. As a reader, I want citations for each answer so I can verify the information.
3. As a reader, I want to browse chapters manually so I can read the textbook in order.
4. As a reader, I want to search across all chapters so I can quickly find concepts.
5. As a reader, I want to compare two chapters so I can understand similarities and differences.
6. As a reader, I want answers to show chapter and section names so I can trust the source.

## Epic B: Developer experience

7. As a developer, I want to clone the repo and run it locally so I can experiment easily.
8. As a developer, I want to replace the sample textbook with my own Markdown files so I can adapt the system.
9. As a developer, I want the system to reindex only changed files so updates are fast.
10. As a developer, I want environment variables documented so I can configure the app quickly.
11. As a developer, I want Docker support so I can run the stack consistently on different machines.
12. As a developer, I want GitHub Actions so I can be confident changes don’t break tests.

## Epic C: AI client experience

13. As a ChatGPT user, I want ChatGPT to call textbook search tools via MCP so I can query the corpus from chat.
14. As a Claude user, I want Claude to access the same textbook via MCP so I can use my preferred assistant.
15. As a Gemini user, I want Gemini to use the same retrieval backend so I get consistent answers.
16. As a power user, I want different models to use the same retrieved context so I can compare answers across models.
17. As a power user, I want to switch models without rebuilding the index so experiments are fast.

## Epic D: Trust and governance

18. As an admin, I want read‑only access in MCP so the corpus cannot be modified accidentally.
19. As an admin, I want logs and usage metrics so I can diagnose retrieval failures and performance issues.
20. As a maintainer, I want an evaluation set so I can measure retrieval and citation quality over time.
