"""LLM module for memory extraction and image summarization."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluttr.llm.base import BaseLLMService
from cluttr.llm.bedrock import BedrockLLMService
from cluttr.llm.openai import OpenAILLMService

if TYPE_CHECKING:
    from cluttr.config import BedrockSettings, OpenAISettings

__all__ = [
    "BaseLLMService",
    "BedrockLLMService",
    "OpenAILLMService",
    "create_llm_service",
]


def create_llm_service(config: BedrockSettings | OpenAISettings) -> BaseLLMService:
    """Factory function to create the appropriate LLM service."""
    if config.provider == "bedrock":
        return BedrockLLMService(config)
    elif config.provider == "openai":
        return OpenAILLMService(config)
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")
