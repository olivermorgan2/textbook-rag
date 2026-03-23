"""FastAPI application entry point."""

from __future__ import annotations

import os

from fastapi import FastAPI

from backend.api.api import router, set_provider
from backend.providers.stub import StubProvider

app = FastAPI(title="Textbook RAG API")

# Configure the provider from an environment variable.
# Default to the stub provider (no LLM key required).
_PROVIDER_MAP = {
    "stub": StubProvider,
}

provider_name = os.getenv("RAG_PROVIDER", "stub")
provider_cls = _PROVIDER_MAP.get(provider_name)
if provider_cls is None:
    raise ValueError(f"Unknown provider: {provider_name!r}. Available: {list(_PROVIDER_MAP)}")

set_provider(provider_cls())
app.include_router(router)
