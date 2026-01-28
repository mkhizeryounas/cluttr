"""Configuration module for cluttr."""

from __future__ import annotations

from typing import TypedDict


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


class BedrockLLMConfig(TypedDict, total=False):
    """Configuration for Bedrock LLM provider."""

    provider: str  # 'bedrock'
    region: str
    model: str
    embedding_model: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str


class OpenAILLMConfig(TypedDict, total=False):
    """Configuration for OpenAI LLM provider."""

    provider: str  # 'openai'
    api_key: str
    model: str
    embedding_model: str
    base_url: str  # For OpenAI-compatible APIs


LLMConfig = BedrockLLMConfig | OpenAILLMConfig


class CluttrConfigDict(TypedDict, total=False):
    """Configuration dictionary for Cluttr."""

    vector_db: VectorDBConfig
    llm: LLMConfig
    similarity_threshold: float


# Internal config classes used by services
class BedrockSettings:
    """Internal settings for AWS Bedrock."""

    def __init__(self, config: BedrockLLMConfig) -> None:
        self.provider = "bedrock"
        self.region_name = config.get("region", "us-east-1")
        self.llm_model_id = config.get("model", "anthropic.claude-3-haiku-20240307-v1:0")
        self.embedding_model_id = config.get("embedding_model", "amazon.titan-embed-text-v2:0")
        self.aws_access_key_id = config.get("aws_access_key_id")
        self.aws_secret_access_key = config.get("aws_secret_access_key")
        self.aws_session_token = config.get("aws_session_token")


class OpenAISettings:
    """Internal settings for OpenAI."""

    def __init__(self, config: OpenAILLMConfig) -> None:
        self.provider = "openai"
        self.api_key = config.get("api_key")
        self.model = config.get("model", "gpt-4o-mini")
        self.embedding_model = config.get("embedding_model", "text-embedding-3-small")
        self.base_url = config.get("base_url")


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
            raise ValueError(
                f"Unsupported vector_db engine: {engine}. Only 'postgres' is supported."
            )

        # Get provider
        self.llm_provider = llm.get("provider", "bedrock")
        if self.llm_provider not in ("bedrock", "openai"):
            raise ValueError(
                f"Unsupported llm provider: {self.llm_provider}. Supported: 'bedrock', 'openai'."
            )

        self.postgres = PostgresSettings(vector_db)

        # Set up LLM settings based on provider
        if self.llm_provider == "bedrock":
            self.llm_settings: BedrockSettings | OpenAISettings = BedrockSettings(llm)
            self.embedding_dimensions = 1024  # Titan
        else:
            self.llm_settings = OpenAISettings(llm)
            self.embedding_dimensions = 1536  # text-embedding-3-small

        self.similarity_threshold = config.get("similarity_threshold", 0.95)
        self.table_name = "memories"
