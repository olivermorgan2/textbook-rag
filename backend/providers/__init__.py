"""Model provider adapters."""

from backend.providers.base import BaseProvider
from backend.providers.stub import StubProvider

__all__ = ["BaseProvider", "StubProvider"]
