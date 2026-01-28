"""Main client module for cluttr."""

from __future__ import annotations

from typing import Any

from cluttr.config import CluttrConfig, CluttrConfigDict
from cluttr.db import DatabaseService
from cluttr.embeddings import EmbeddingService
from cluttr.llm import LLMService
from cluttr.models import Memory, Message, SearchResult


class Cluttr:
    """Long-term memory for AI agents."""

    def __init__(self, config: CluttrConfigDict) -> None:
        """
        Initialize Cluttr memory.

        Args:
            config: Configuration dictionary
                {
                    "vector_db": {
                        "engine": "postgres",  # Only 'postgres' supported
                        "host": "localhost",
                        "port": 5432,
                        "database": "cluttr",
                        "user": "postgres",
                        "password": "...",
                        # OR use connection_string instead:
                        "connection_string": "postgresql://user:pass@host:port/db",
                    },
                    "llm": {
                        "provider": "bedrock",  # Only 'bedrock' supported
                        "region": "us-east-1",
                        "model": "anthropic.claude-3-haiku-20240307-v1:0",
                        "embedding_model": "amazon.titan-embed-text-v2:0",
                        "aws_access_key_id": "...",  # Optional
                        "aws_secret_access_key": "...",
                        "aws_session_token": "...",
                    },
                    "similarity_threshold": 0.95,  # Optional
                }
        """
        self._config = CluttrConfig(config)
        self._db = DatabaseService(self._config)
        self._embeddings = EmbeddingService(self._config.bedrock)
        self._llm = LLMService(self._config.bedrock)
        self._connected = False

    async def connect(self) -> None:
        """Connect to the database."""
        await self._db.connect()
        self._connected = True

    async def close(self) -> None:
        """Close the database connection."""
        await self._db.close()
        self._connected = False

    async def __aenter__(self) -> Cluttr:
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    def _ensure_connected(self) -> None:
        """Ensure the client is connected."""
        if not self._connected:
            raise RuntimeError("Not connected. Call connect() or use 'async with' context manager.")

    async def add(
        self,
        messages: list[dict[str, Any]],
        user_id: str = "default_user",
        agent_id: str = "default_agent",
    ) -> list[Memory]:
        """
        Add memories from a conversation.

        Args:
            messages: List of messages in OpenAI format
                      [{"role": "user", "content": "..."}]
            user_id: User ID (default: "default_user")
            agent_id: Agent ID (default: "default_agent")

        Returns:
            List of memories that were added
        """
        self._ensure_connected()

        parsed_messages = [Message.from_dict(m) for m in messages]

        extracted = self._llm.extract_memories(parsed_messages)

        if not extracted:
            return []

        added_memories = []
        for content in extracted:
            is_duplicate = await self._is_duplicate(content, user_id, agent_id)
            if is_duplicate:
                continue

            embedding = self._embeddings.embed(content)

            memory = Memory(
                user_id=user_id,
                agent_id=agent_id,
                content=content,
                embedding=embedding,
            )

            await self._db.insert_memory(memory)
            added_memories.append(memory)

        return added_memories

    async def search(
        self,
        query: str,
        k: int = 10,
        user_id: str = "default_user",
        agent_id: str = "default_agent",
    ) -> list[SearchResult]:
        """
        Search for relevant memories.

        Args:
            query: Search query text
            k: Number of results to return (default 10)
            user_id: User ID to filter by (default: "default_user")
            agent_id: Agent ID to filter by (default: "default_agent")

        Returns:
            List of SearchResult objects with memory and similarity score
        """
        self._ensure_connected()

        embedding = self._embeddings.embed(query)

        results = await self._db.search(
            embedding=embedding,
            user_id=user_id,
            agent_id=agent_id,
            k=k,
        )

        return [
            SearchResult(
                memory=Memory(
                    id=r["id"],
                    user_id=r["user_id"],
                    agent_id=r["agent_id"],
                    content=r["content"],
                    created_at=r["created_at"],
                ),
                similarity=r["similarity"],
            )
            for r in results
        ]

    async def _is_duplicate(
        self,
        content: str,
        user_id: str,
        agent_id: str,
    ) -> bool:
        """Check if a memory is a duplicate based on semantic similarity."""
        embedding = self._embeddings.embed(content)

        similar = await self._db.find_similar(
            embedding=embedding,
            user_id=user_id,
            agent_id=agent_id,
            threshold=self._config.similarity_threshold,
            limit=1,
        )

        return len(similar) > 0
