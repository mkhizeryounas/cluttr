"""Base embedding service."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseEmbeddingService(ABC):
    """Abstract base class for embedding services."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        pass

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        return [self.embed(text) for text in texts]
