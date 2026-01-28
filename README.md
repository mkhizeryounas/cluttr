# Cluttr

Long-term memory for AI agents using PostgreSQL vector storage.

## Installation

```bash
uv add cluttr
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
        "provider": "bedrock",  # Only 'bedrock' supported
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

- **Automatic Memory Extraction**: Uses Claude to extract important information from conversations
- **Duplicate Detection**: Semantic similarity-based duplicate prevention
- **Image Support**: Automatic image summarization for multimodal conversations
- **PostgreSQL + pgvector**: Efficient vector similarity search
- **AWS Bedrock**: Uses Titan for embeddings and Claude for extraction
- **Async Support**: Full async/await support

## Requirements

- Python 3.11+
- PostgreSQL with pgvector extension
- AWS credentials configured for Bedrock access

## License

MIT
