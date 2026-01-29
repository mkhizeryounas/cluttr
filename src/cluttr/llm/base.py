"""Base LLM service for memory extraction."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cluttr.models import Message


EXTRACTION_PROMPT = """Extract key facts about the user from this conversation.

Rules:
- Return 0-2 facts maximum (only the most important)
- Combine related facts into one (e.g., "User likes JS, TS, and Bun" not separate)
- Skip greetings, small talk, and task-specific details
- Focus on lasting preferences, personal info, or important context

Return a JSON array of strings. Return [] if nothing important.

Conversation:
{conversation}

JSON array:"""


IMAGE_SUMMARY_PROMPT = (
    "Describe this image in detail, focusing on the key information it contains. "
    "Be concise but comprehensive. If the image contains text, include the relevant text content."
)

DEDUP_PROMPT = """I want to save this new fact about a user:
"{new_memory}"

Here are the existing memories I already have:
{existing_memories}

Is this new fact already covered by any existing memory? Answer with just "YES" or "NO".
- YES if the new fact is redundant, a duplicate, or already implied by existing memories
- NO if the new fact adds genuinely new information"""


QUERY_EXPANSION_PROMPT = """Rewrite this search query for vector search.

Query: {query}

Rules:
- Convert questions to statements (e.g., "What language?" -> "prefers language")
- Keep it concise (5-10 words max)
- Focus on key concepts that would match stored facts
- Return ONLY the rewritten query, nothing else

Rewritten query:"""


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

    def is_duplicate(self, new_memory: str, existing_memories: list[str]) -> bool:
        """Check if a new memory is a duplicate of existing memories using LLM."""
        if not existing_memories:
            return False

        existing_list = "\n".join(f"- {m}" for m in existing_memories)
        prompt = DEDUP_PROMPT.format(new_memory=new_memory, existing_memories=existing_list)

        response = self._invoke(messages=[{"role": "user", "content": prompt}])
        return response.strip().upper().startswith("YES")

    def expand_query(self, query: str) -> str:
        """Expand a search query for better semantic matching."""
        prompt = QUERY_EXPANSION_PROMPT.format(query=query)
        response = self._invoke(messages=[{"role": "user", "content": prompt}])
        expanded = response.strip()
        # Return expanded query, or original if expansion fails
        return expanded if expanded else query
