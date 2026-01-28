"""Base LLM service for memory extraction."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
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
