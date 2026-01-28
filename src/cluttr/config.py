"""Configuration module for cluttr."""

from __future__ import annotations

from typing import Any, TypedDict


class VectorDBConfig(TypedDict, total=False):
    """Configuration for vector database."""

    engine: str  # Only 'postgres' supported
    host: str
    port: int
    database: str
    user: str
    password: str
    connection_string: str  # Alternative to host/port/database/user/password
    min_connections: int
    max_connections: int


class LLMConfig(TypedDict, total=False):
    """Configuration for LLM provider."""

    provider: str  # Only 'bedrock' supported
    region: str
    model: str  # LLM model for extraction
    embedding_model: str  # Model for embeddings
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str


class CluttrConfigDict(TypedDict, total=False):
    """Configuration dictionary for Cluttr."""

    vector_db: VectorDBConfig
    llm: LLMConfig
    similarity_threshold: float


# Internal config classes used by services
class BedrockSettings:
    """Internal settings for AWS Bedrock."""

    def __init__(self, config: LLMConfig) -> None:
        self.region_name = config.get("region", "us-east-1")
        self.llm_model_id = config.get("model", "anthropic.claude-3-haiku-20240307-v1:0")
        self.embedding_model_id = config.get("embedding_model", "amazon.titan-embed-text-v2:0")
        self.aws_access_key_id = config.get("aws_access_key_id")
        self.aws_secret_access_key = config.get("aws_secret_access_key")
        self.aws_session_token = config.get("aws_session_token")


class PostgresSettings:
    """Internal settings for PostgreSQL."""

    def __init__(self, config: VectorDBConfig) -> None:
        self.connection_string = config.get("connection_string")
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 5432)
        self.database = config.get("database", "cluttr")
        self.user = config.get("user", "postgres")
        self.password = config.get("password", "")
        self.min_connections = config.get("min_connections", 1)
        self.max_connections = config.get("max_connections", 10)

    def get_connection_string(self) -> str:
        """Get the connection string, building from params if not provided."""
        if self.connection_string:
            return self.connection_string
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class CluttrConfig:
    """Internal configuration holder for Cluttr."""

    def __init__(self, config: CluttrConfigDict) -> None:
        vector_db = config.get("vector_db", {})
        llm = config.get("llm", {})

        # Validate engine
        engine = vector_db.get("engine", "postgres")
        if engine != "postgres":
            raise ValueError(f"Unsupported vector_db engine: {engine}. Only 'postgres' is supported.")

        # Validate provider
        provider = llm.get("provider", "bedrock")
        if provider != "bedrock":
            raise ValueError(f"Unsupported llm provider: {provider}. Only 'bedrock' is supported.")

        self.postgres = PostgresSettings(vector_db)
        self.bedrock = BedrockSettings(llm)
        self.similarity_threshold = config.get("similarity_threshold", 0.95)
        self.embedding_dimensions = 1024
        self.table_name = "memories"
