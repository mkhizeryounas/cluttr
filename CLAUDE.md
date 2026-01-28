# Cluttr

Long-term memory for AI agents using PostgreSQL vector storage.

## Project Structure

```
cluttr/
├── src/cluttr/          # Main package
│   ├── __init__.py      # Exports: Cluttr, Memory, SearchResult
│   ├── client.py        # Cluttr class - main API
│   ├── config.py        # Configuration types and validation
│   ├── db.py            # PostgreSQL/pgvector operations
│   ├── embeddings.py    # Bedrock Titan embeddings
│   ├── llm.py           # Claude Haiku for memory extraction
│   └── models.py        # Memory, Message, SearchResult models
├── examples/
│   └── chat_with_memory.py  # Example chat application
├── pyproject.toml       # Package config (uv)
└── README.md
```

## Key APIs

```python
from cluttr import Cluttr

config = {
    "vector_db": {"engine": "postgres", "host": "...", ...},
    "llm": {"provider": "bedrock", "region": "...", ...},
}

memory = Cluttr(config)

async with memory:
    await memory.add(messages, user_id="...", agent_id="...")
    results = await memory.search(query, user_id="...", agent_id="...")
```

## Commands

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --all-extras

# Run example
uv run python examples/chat_with_memory.py

# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Type check
uv run mypy src/
```

## Architecture Notes

- **Async-only**: All database operations are async using asyncpg
- **System messages skipped**: Memory extraction ignores system role messages
- **Duplicate detection**: Uses semantic similarity (configurable threshold)
- **Image support**: Images are summarized by Claude before storage
- **Only postgres/bedrock**: Other providers not yet supported
