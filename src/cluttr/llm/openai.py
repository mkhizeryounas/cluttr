"""OpenAI LLM service."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import TYPE_CHECKING, Any

import openai

from cluttr.llm.base import IMAGE_SUMMARY_PROMPT, BaseLLMService

if TYPE_CHECKING:
    from cluttr.config import OpenAISettings


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
                    return _load_and_encode_image(url)
        return None


def _load_and_encode_image(path: str) -> dict[str, Any] | None:
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
