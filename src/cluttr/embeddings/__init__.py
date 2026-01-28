"""Embeddings module supporting Bedrock and OpenAI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluttr.embeddings.base import BaseEmbeddingService
from cluttr.embeddings.bedrock import BedrockEmbeddingService
from cluttr.embeddings.openai import OpenAIEmbeddingService

if TYPE_CHECKING:
    from cluttr.config import BedrockSettings, OpenAISettings

__all__ = [
    "BaseEmbeddingService",
    "BedrockEmbeddingService",
    "OpenAIEmbeddingService",
    "create_embedding_service",
]


def create_embedding_service(
    config: BedrockSettings | OpenAISettings,
) -> BaseEmbeddingService:
    """Factory function to create the appropriate embedding service."""
    if config.provider == "bedrock":
        return BedrockEmbeddingService(config)
    elif config.provider == "openai":
        return OpenAIEmbeddingService(config)
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")
