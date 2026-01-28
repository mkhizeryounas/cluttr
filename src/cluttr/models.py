"""Data models for cluttr."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class Message:
    """A single message in a conversation."""

    role: str
    content: str | list[dict[str, Any]]

    def get_text_content(self) -> str:
        """Extract text content from message."""
        if isinstance(self.content, str):
            return self.content
        text_parts = []
        for part in self.content:
            if part.get("type") == "text":
                text_parts.append(part.get("text", ""))
        return " ".join(text_parts)

    def get_images(self) -> list[dict[str, Any]]:
        """Extract image parts from message."""
        if isinstance(self.content, str):
            return []
        images = []
        for part in self.content:
            if part.get("type") == "image":
                images.append(part)
            elif part.get("type") == "image_url":
                images.append(part)
        return images

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Message:
        """Create a Message from a dictionary."""
        return cls(role=data["role"], content=data["content"])


@dataclass
class Memory:
    """A memory extracted from conversations."""

    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    agent_id: str = ""
    content: str = ""
    embedding: list[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        """Convert memory to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SearchResult:
    """A search result with similarity score."""

    memory: Memory
    similarity: float

    def to_dict(self) -> dict[str, Any]:
        """Convert search result to dictionary."""
        return {
            **self.memory.to_dict(),
            "similarity": self.similarity,
        }
