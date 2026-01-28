"""OpenAI embedding service."""

from __future__ import annotations

from typing import TYPE_CHECKING

import openai

from cluttr.embeddings.base import BaseEmbeddingService

if TYPE_CHECKING:
    from cluttr.config import OpenAISettings


class OpenAIEmbeddingService(BaseEmbeddingService):
    """Embedding service using OpenAI."""

    def __init__(self, config: OpenAISettings) -> None:
        """Initialize the embedding service."""
        self.config = config
        self._client = None

    @property
    def client(self) -> openai.OpenAI:
        """Get or create the OpenAI client."""
        if self._client is None:
            kwargs = {}
            if self.config.api_key:
                kwargs["api_key"] = self.config.api_key
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            self._client = openai.OpenAI(**kwargs)
        return self._client

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=text,
        )
        return response.data[0].embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts (optimized for OpenAI)."""
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=texts,
        )
        return [item.embedding for item in response.data]
