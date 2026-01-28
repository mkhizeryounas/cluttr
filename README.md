# Cluttr

Long-term memory for AI agents using PostgreSQL vector storage.

## Installation

```bash
uv add cluttr
```

## Quick Start

```python
import asyncio
from cluttr import MemoryConfig

async def main():
    # Configure with connection string
    config = MemoryConfig.from_connection_string(
        "postgresql://user:password@localhost:5432/cluttr",
        default_user_id="user_123",
        default_agent_id="agent_456",
    )

    # Connect and get client
    client = await config.connect()

    # Add memories from a conversation
    messages = [
        {"role": "user", "content": "I prefer Python over JavaScript"},
        {"role": "assistant", "content": "Got it! I'll remember that you prefer Python."},
        {"role": "user", "content": "My project deadline is end of March"},
    ]

    memories = await client.add(messages)
    print(f"Added {len(memories)} memories")

    # Search for relevant memories
    results = await client.search("What programming language does the user prefer?", k=5)
    for r in results:
        print(f"[{r.similarity:.2f}] {r.memory.content}")

    await client.close()

asyncio.run(main())
```

## Configuration

### Using Connection String

```python
config = MemoryConfig.from_connection_string(
    "postgresql://user:password@localhost:5432/cluttr",
    default_user_id="user_123",
    default_agent_id="agent_456",
    region_name="us-east-1",  # AWS region for Bedrock
    similarity_threshold=0.95,  # For duplicate detection
)
```

### Using Individual Parameters

```python
config = MemoryConfig.from_params(
    host="localhost",
    port=5432,
    database="cluttr",
    user="postgres",
    password="secret",
    default_user_id="user_123",
    default_agent_id="agent_456",
    region_name="us-east-1",
    embedding_model_id="amazon.titan-embed-text-v2:0",
    llm_model_id="anthropic.claude-3-haiku-20240307-v1:0",
    aws_access_key_id="...",  # Optional, uses default credentials if not provided
    aws_secret_access_key="...",
)
```

## Usage

### Context Manager

```python
async with await config.connect() as client:
    await client.add(messages)
    results = await client.search("query")
```

### Adding Memories

```python
# Add with default user/agent
memories = await client.add(messages)

# Add with specific user/agent
memories = await client.add(
    messages,
    user_id="custom_user",
    agent_id="custom_agent",
)
```

### Searching Memories

```python
# Search with defaults
results = await client.search("What does the user like?", k=10)

# Search specific user/agent
results = await client.search(
    "query",
    k=5,
    user_id="custom_user",
    agent_id="custom_agent",
)

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

# Images are summarized and included in memory extraction
await client.add(messages)
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
