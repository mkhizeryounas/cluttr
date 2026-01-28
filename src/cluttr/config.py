"""Configuration module for cluttr."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cluttr.client import MemoryClient


@dataclass
class BedrockConfig:
    """Configuration for AWS Bedrock."""

    region_name: str = "us-east-1"
    embedding_model_id: str = "amazon.titan-embed-text-v2:0"
    llm_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_session_token: str | None = None


@dataclass
class PostgresConfig:
    """Configuration for PostgreSQL connection."""

    connection_string: str | None = None
    host: str = "localhost"
    port: int = 5432
    database: str = "cluttr"
    user: str = "postgres"
    password: str = ""
    min_connections: int = 1
    max_connections: int = 10

    def get_connection_string(self) -> str:
        """Get the connection string, building from params if not provided."""
        if self.connection_string:
            return self.connection_string
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class MemoryConfig:
    """Main configuration for cluttr."""

    postgres: PostgresConfig = field(default_factory=PostgresConfig)
    bedrock: BedrockConfig = field(default_factory=BedrockConfig)
    default_user_id: str = "default_user"
    default_agent_id: str = "default_agent"
    similarity_threshold: float = 0.95
    embedding_dimensions: int = 1024
    table_name: str = "memories"

    @classmethod
    def from_connection_string(
        cls,
        connection_string: str,
        *,
        default_user_id: str = "default_user",
        default_agent_id: str = "default_agent",
        region_name: str = "us-east-1",
        embedding_model_id: str = "amazon.titan-embed-text-v2:0",
        llm_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        similarity_threshold: float = 0.95,
    ) -> MemoryConfig:
        """Create config from a PostgreSQL connection string."""
        return cls(
            postgres=PostgresConfig(connection_string=connection_string),
            bedrock=BedrockConfig(
                region_name=region_name,
                embedding_model_id=embedding_model_id,
                llm_model_id=llm_model_id,
            ),
            default_user_id=default_user_id,
            default_agent_id=default_agent_id,
            similarity_threshold=similarity_threshold,
        )

    @classmethod
    def from_params(
        cls,
        *,
        host: str = "localhost",
        port: int = 5432,
        database: str = "cluttr",
        user: str = "postgres",
        password: str = "",
        default_user_id: str = "default_user",
        default_agent_id: str = "default_agent",
        region_name: str = "us-east-1",
        embedding_model_id: str = "amazon.titan-embed-text-v2:0",
        llm_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        similarity_threshold: float = 0.95,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
    ) -> MemoryConfig:
        """Create config from individual PostgreSQL parameters."""
        return cls(
            postgres=PostgresConfig(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
            ),
            bedrock=BedrockConfig(
                region_name=region_name,
                embedding_model_id=embedding_model_id,
                llm_model_id=llm_model_id,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
            ),
            default_user_id=default_user_id,
            default_agent_id=default_agent_id,
            similarity_threshold=similarity_threshold,
        )

    async def connect(self) -> MemoryClient:
        """Create and connect a MemoryClient with this configuration."""
        from cluttr.client import MemoryClient

        client = MemoryClient(self)
        await client.connect()
        return client
