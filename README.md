# Cluttr

[![Lint](https://github.com/mkhizeryounas/cluttr/actions/workflows/lint.yml/badge.svg)](https://github.com/mkhizeryounas/cluttr/actions/workflows/lint.yml)

Long-term memory for AI agents using PostgreSQL vector storage.

🌐 [https://www.cluttr.co](https://cluttr-co.vercel.app)

## Installation

```bash
# From PyPI
uv add cluttr

# From GitHub
uv add git+https://github.com/mkhizeryounas/cluttr.git
```

## Quick Start

```python
import asyncio
from cluttr import Cluttr

async def main():
    # Configure
    config = {
        "vector_db": {
            "engine": "postgres",
            "host": "localhost",
            "port": 5432,
            "database": "cluttr",
            "user": "postgres",
            "password": "secret",
        },
        "llm": {
            "provider": "bedrock",
            "region": "us-east-1",
        },
    }

    # Create memory instance
    memory = Cluttr(config)

    async with memory:
        # Add memories from a conversation
        messages = [
            {"role": "user", "content": "I prefer Python over JavaScript"},
            {"role": "assistant", "content": "Got it! I'll remember that you prefer Python."},
        ]

        await memory.add(messages, user_id="user_123", agent_id="agent_456")

        # Search for relevant memories
        results = await memory.search(
            "What programming language does the user prefer?",
            k=5,
            user_id="user_123",
            agent_id="agent_456",
        )
        for r in results:
            print(f"[{r.similarity:.2f}] {r.memory.content}")

asyncio.run(main())
```

## Configuration

### AWS Bedrock Provider

```python
config = {
    "vector_db": {
        "engine": "postgres",  # Only 'postgres' supported
        "host": "localhost",
        "port": 5432,
        "database": "cluttr",
        "user": "postgres",
        "password": "secret",
        # OR use connection_string instead:
        # "connection_string": "postgresql://user:pass@host:port/db",
    },
    "llm": {
        "provider": "bedrock",
        "region": "us-east-1",
        "model": "anthropic.claude-3-haiku-20240307-v1:0",  # Optional
        "embedding_model": "amazon.titan-embed-text-v2:0",  # Optional
        "aws_access_key_id": "...",  # Optional, uses default credentials
        "aws_secret_access_key": "...",
        "aws_session_token": "...",
    },
    "similarity_threshold": 0.95,  # Optional, for duplicate detection
}

memory = Cluttr(config)
```

### OpenAI Provider

```python
config = {
    "vector_db": {
        "engine": "postgres",
        "host": "localhost",
        "port": 5432,
        "database": "cluttr",
        "user": "postgres",
        "password": "secret",
    },
    "llm": {
        "provider": "openai",
        "api_key": "sk-...",
        "model": "gpt-4o-mini",  # Optional, default: gpt-4o-mini
        "embedding_model": "text-embedding-3-small",  # Optional
        "base_url": "...",  # Optional, for custom endpoints
    },
    "similarity_threshold": 0.95,  # Optional
}

memory = Cluttr(config)
```

## Usage

### Adding Memories

```python
# Add with specific user/agent
await memory.add(messages, user_id="user_123", agent_id="agent_456")

# Add with defaults (user_id="default_user", agent_id="default_agent")
await memory.add(messages)
```

### Searching Memories

```python
# Search with specific user/agent
results = await memory.search(
    "What does the user like?",
    k=10,
    user_id="user_123",
    agent_id="agent_456",
)

# Search with defaults
results = await memory.search("query", k=5)

# Access results
for result in results:
    print(result.memory.content)
    print(result.similarity)
```

### Image Support

Images in messages are automatically summarized:

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Here's my system architecture"},
            {
                "type": "image_url",
                "image_url": {"url": "https://example.com/diagram.png"}
            }
        ]
    }
]

await memory.add(messages)
```

Supported image formats:
- Base64 encoded images
- URLs (http/https)
- Local file paths

## Features

- **Automatic Memory Extraction**: LLM extracts important facts from conversations
- **Smart Query Expansion**: Search queries are automatically optimized for vector matching
- **Duplicate Detection**: LLM-powered deduplication prevents redundant memories
- **Image Support**: Images are automatically summarized and stored as searchable memories
- **PostgreSQL + pgvector**: Battle-tested vector similarity search
- **Multiple Providers**: AWS Bedrock (Claude + Titan) and OpenAI (GPT-4o-mini)
- **Async Native**: Full async/await support

## Development

```bash
# Clone the repository
git clone https://github.com/mkhizeryounas/cluttr.git
cd cluttr

# Install dependencies
uv sync --all-extras

# Install package in editable mode (required to run examples)
uv pip install -e . --force-reinstall

# Run examples
uv run python examples/chat_with_memory_openai.py
```

## Requirements

- Python 3.11+
- PostgreSQL with pgvector extension
- AWS credentials (for Bedrock) or OpenAI API key

## Supabase Setup

Cluttr works with [Supabase](https://supabase.com) as the PostgreSQL backend.

### 1. Enable pgvector Extension

In your Supabase dashboard, go to **Database → Extensions** and enable the `vector` extension.

Or run this SQL:

```sql
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;
```

### 2. Configure Connection

```python
config = {
    "vector_db": {
        "engine": "postgres",
        "host": "db.<project-ref>.supabase.co",
        "port": 5432,
        "database": "postgres",
        "user": "postgres",
        "password": "<your-db-password>",
    },
    "llm": {
        "provider": "openai",
        "api_key": "sk-...",
    },
}
```

Or use a connection string:

```python
config = {
    "vector_db": {
        "engine": "postgres",
        "connection_string": "postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres",
    },
    "llm": {
        "provider": "openai",
        "api_key": "sk-...",
    },
}
```

### 3. Table Schema

Cluttr automatically creates the `cluttr_memories` table on first connection:

```sql
CREATE TABLE IF NOT EXISTS cluttr_memories (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- 1536 for OpenAI, 1024 for Bedrock
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## License

MIT
