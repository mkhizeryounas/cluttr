"""Bedrock embedding service using AWS Titan."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import boto3

from cluttr.embeddings.base import BaseEmbeddingService

if TYPE_CHECKING:
    from cluttr.config import BedrockSettings


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
