"""Embeddings module supporting Bedrock and OpenAI."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import boto3
import openai

if TYPE_CHECKING:
    from cluttr.config import BedrockSettings, OpenAISettings


class BaseEmbeddingService(ABC):
    """Abstract base class for embedding services."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        pass

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        return [self.embed(text) for text in texts]


class BedrockEmbeddingService(BaseEmbeddingService):
    """Embedding service using AWS Bedrock Titan."""

    def __init__(self, config: BedrockSettings) -> None:
        """Initialize the embedding service."""
        self.config = config
        self._client = None

    @property
    def client(self):
        """Get or create the Bedrock runtime client."""
        if self._client is None:
            kwargs = {"region_name": self.config.region_name}
            if self.config.aws_access_key_id:
                kwargs["aws_access_key_id"] = self.config.aws_access_key_id
            if self.config.aws_secret_access_key:
                kwargs["aws_secret_access_key"] = self.config.aws_secret_access_key
            if self.config.aws_session_token:
                kwargs["aws_session_token"] = self.config.aws_session_token
            self._client = boto3.client("bedrock-runtime", **kwargs)
        return self._client

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        body = json.dumps({"inputText": text})

        response = self.client.invoke_model(
            modelId=self.config.embedding_model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        return response_body["embedding"]


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
