"""LLM module for memory extraction and image summarization."""

from __future__ import annotations

import base64
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

import boto3
import httpx
import openai

if TYPE_CHECKING:
    from cluttr.config import BedrockSettings, OpenAISettings
    from cluttr.models import Message


EXTRACTION_PROMPT = """Analyze the following conversation and extract the most important \
and useful information that should be remembered for future interactions. Focus on:
- Key facts about the user (preferences, background, goals)
- Important decisions or conclusions reached
- Specific requests or requirements mentioned
- Any information that would be valuable to remember in future conversations

Return ONLY a JSON array of strings, where each string is a distinct piece of \
information worth remembering. If there's nothing worth remembering, return an empty array [].

Example output format:
["User prefers Python over JavaScript", "User is building a chatbot for customer service", \
"User's deadline is end of March"]

Conversation:
{conversation}

Important information to remember (JSON array only):"""


IMAGE_SUMMARY_PROMPT = (
    "Describe this image in detail, focusing on the key information it contains. "
    "Be concise but comprehensive. If the image contains text, include the relevant text content."
)


class BaseLLMService(ABC):
    """Abstract base class for LLM services."""

    @abstractmethod
    def _invoke(self, messages: list[dict[str, Any]], system: str | None = None) -> str:
        """Invoke the LLM and return the response text."""
        pass

    @abstractmethod
    def summarize_image(self, image_data: dict[str, Any]) -> str:
        """Summarize an image and return text description."""
        pass

    def extract_memories(self, messages: list[Message]) -> list[str]:
        """Extract important information from a conversation."""
        conversation_text = self._format_conversation(messages)
        prompt = EXTRACTION_PROMPT.format(conversation=conversation_text)

        response = self._invoke(messages=[{"role": "user", "content": prompt}])

        try:
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
            return []
        except json.JSONDecodeError:
            return []

    def _format_conversation(self, messages: list[Message]) -> str:
        """Format messages into a conversation string, excluding system messages."""
        lines = []
        for msg in messages:
            # Skip system messages - we don't want to store system prompts
            if msg.role.lower() == "system":
                continue

            role = msg.role.capitalize()
            content = msg.get_text_content()

            images = msg.get_images()
            if images:
                image_summaries = []
                for img in images:
                    summary = self.summarize_image(img)
                    if summary:
                        image_summaries.append(f"[Image: {summary}]")
                if image_summaries:
                    content = content + " " + " ".join(image_summaries)

            lines.append(f"{role}: {content}")
        return "\n".join(lines)


class BedrockLLMService(BaseLLMService):
    """LLM service using AWS Bedrock Claude."""

    def __init__(self, config: BedrockSettings) -> None:
        """Initialize the LLM service."""
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

    def _invoke(self, messages: list[dict[str, Any]], system: str | None = None) -> str:
        """Invoke Claude model and return the response text."""
        body: dict[str, Any] = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": messages,
        }
        if system:
            body["system"] = system

        response = self.client.invoke_model(
            modelId=self.config.llm_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]

    def summarize_image(self, image_data: dict[str, Any]) -> str:
        """Summarize an image and return text description."""
        image_content = self._prepare_image_content(image_data)
        if not image_content:
            return ""

        messages = [
            {
                "role": "user",
                "content": [
                    image_content,
                    {"type": "text", "text": IMAGE_SUMMARY_PROMPT},
                ],
            }
        ]

        return self._invoke(messages=messages)

    def _prepare_image_content(self, image_data: dict[str, Any]) -> dict[str, Any] | None:
        """Prepare image content for Claude API."""
        if image_data.get("type") == "image":
            source = image_data.get("source", {})
            if source.get("type") == "base64":
                return {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": source.get("media_type", "image/png"),
                        "data": source.get("data", ""),
                    },
                }
        elif image_data.get("type") == "image_url":
            url = image_data.get("image_url", {}).get("url", "")
            if url.startswith("data:"):
                parts = url.split(",", 1)
                if len(parts) == 2:
                    media_type = parts[0].split(":")[1].split(";")[0]
                    return {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": parts[1],
                        },
                    }
            elif url.startswith(("http://", "https://")):
                return _fetch_and_encode_image_bedrock(url)
            elif Path(url).exists():
                return _load_and_encode_image_bedrock(url)
        return None


class OpenAILLMService(BaseLLMService):
    """LLM service using OpenAI."""

    def __init__(self, config: OpenAISettings) -> None:
        """Initialize the LLM service."""
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

    def _invoke(self, messages: list[dict[str, Any]], system: str | None = None) -> str:
        """Invoke OpenAI model and return the response text."""
        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=all_messages,
            max_tokens=4096,
        )

        return response.choices[0].message.content or ""

    def summarize_image(self, image_data: dict[str, Any]) -> str:
        """Summarize an image and return text description."""
        image_content = self._prepare_image_content(image_data)
        if not image_content:
            return ""

        messages = [
            {
                "role": "user",
                "content": [
                    image_content,
                    {"type": "text", "text": IMAGE_SUMMARY_PROMPT},
                ],
            }
        ]

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=1024,
        )

        return response.choices[0].message.content or ""

    def _prepare_image_content(self, image_data: dict[str, Any]) -> dict[str, Any] | None:
        """Prepare image content for OpenAI API."""
        if image_data.get("type") == "image":
            source = image_data.get("source", {})
            if source.get("type") == "base64":
                media_type = source.get("media_type", "image/png")
                data = source.get("data", "")
                return {
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{data}"},
                }
        elif image_data.get("type") == "image_url":
            url = image_data.get("image_url", {}).get("url", "")
            if url:
                # OpenAI can handle URLs directly or base64
                if url.startswith(("http://", "https://", "data:")):
                    return {"type": "image_url", "image_url": {"url": url}}
                elif Path(url).exists():
                    return _load_and_encode_image_openai(url)
        return None


def _fetch_and_encode_image_bedrock(url: str) -> dict[str, Any] | None:
    """Fetch image from URL and encode for Bedrock."""
    try:
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "image/png")
        media_type = content_type.split(";")[0].strip()
        data = base64.b64encode(response.content).decode("utf-8")
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": data,
            },
        }
    except Exception:
        return None


def _load_and_encode_image_bedrock(path: str) -> dict[str, Any] | None:
    """Load image from file path and encode for Bedrock."""
    try:
        file_path = Path(path)
        suffix = file_path.suffix.lower()
        media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        media_type = media_types.get(suffix, "image/png")
        data = base64.b64encode(file_path.read_bytes()).decode("utf-8")
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": data,
            },
        }
    except Exception:
        return None


def _load_and_encode_image_openai(path: str) -> dict[str, Any] | None:
    """Load image from file path and encode for OpenAI."""
    try:
        file_path = Path(path)
        suffix = file_path.suffix.lower()
        media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        media_type = media_types.get(suffix, "image/png")
        data = base64.b64encode(file_path.read_bytes()).decode("utf-8")
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{media_type};base64,{data}"},
        }
    except Exception:
        return None


def create_llm_service(config: BedrockSettings | OpenAISettings) -> BaseLLMService:
    """Factory function to create the appropriate LLM service."""
    if config.provider == "bedrock":
        return BedrockLLMService(config)
    elif config.provider == "openai":
        return OpenAILLMService(config)
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")
