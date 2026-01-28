"""Database module for PostgreSQL with pgvector."""

from __future__ import annotations

from typing import TYPE_CHECKING

import asyncpg
from pgvector.asyncpg import register_vector

if TYPE_CHECKING:
    from cluttr.config import MemoryConfig
    from cluttr.models import Memory


class DatabaseService:
    """Service for database operations with pgvector."""

    def __init__(self, config: MemoryConfig) -> None:
        """Initialize the database service."""
        self.config = config
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        """Connect to the database and set up tables."""
        connection_string = self.config.postgres.get_connection_string()
        self._pool = await asyncpg.create_pool(
            connection_string,
            min_size=self.config.postgres.min_connections,
            max_size=self.config.postgres.max_connections,
            init=self._init_connection,
        )
        await self._setup_tables()

    async def _init_connection(self, conn: asyncpg.Connection) -> None:
        """Initialize connection with pgvector extension."""
        await register_vector(conn)

    async def _setup_tables(self) -> None:
        """Create necessary tables and extensions if they don't exist."""
        async with self._pool.acquire() as conn:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.config.table_name} (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({self.config.embedding_dimensions}),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await conn.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_{self.config.table_name}_user_agent
                ON {self.config.table_name} (user_id, agent_id)
            """)

            await conn.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_{self.config.table_name}_embedding
                ON {self.config.table_name}
                USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)

    async def close(self) -> None:
        """Close the database connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def insert_memory(self, memory: Memory) -> None:
        """Insert a memory into the database."""
        async with self._pool.acquire() as conn:
            await conn.execute(
                f"""
                INSERT INTO {self.config.table_name}
                (id, user_id, agent_id, content, embedding, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                memory.id,
                memory.user_id,
                memory.agent_id,
                memory.content,
                memory.embedding,
                memory.created_at,
            )

    async def find_similar(
        self,
        embedding: list[float],
        user_id: str,
        agent_id: str,
        threshold: float,
        limit: int = 1,
    ) -> list[tuple[str, str, float]]:
        """Find memories similar to the given embedding."""
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                f"""
                SELECT id, content, 1 - (embedding <=> $1) as similarity
                FROM {self.config.table_name}
                WHERE user_id = $2 AND agent_id = $3
                AND 1 - (embedding <=> $1) >= $4
                ORDER BY similarity DESC
                LIMIT $5
                """,
                embedding,
                user_id,
                agent_id,
                threshold,
                limit,
            )
            return [(row["id"], row["content"], row["similarity"]) for row in rows]

    async def search(
        self,
        embedding: list[float],
        user_id: str,
        agent_id: str,
        k: int = 10,
    ) -> list[dict]:
        """Search for similar memories."""
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                f"""
                SELECT id, user_id, agent_id, content, created_at,
                       1 - (embedding <=> $1) as similarity
                FROM {self.config.table_name}
                WHERE user_id = $2 AND agent_id = $3
                ORDER BY embedding <=> $1
                LIMIT $4
                """,
                embedding,
                user_id,
                agent_id,
                k,
            )
            return [
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "agent_id": row["agent_id"],
                    "content": row["content"],
                    "created_at": row["created_at"],
                    "similarity": row["similarity"],
                }
                for row in rows
            ]
