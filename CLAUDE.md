# Cluttr

Long-term memory for AI agents using PostgreSQL vector storage.

## Project Structure

```
cluttr/
├── src/cluttr/          # Main package
│   ├── __init__.py      # Exports: Cluttr, Memory, SearchResult
│   ├── client.py        # Cluttr class - main API
│   ├── config.py        # Configuration types and validation
│   ├── db.py            # PostgreSQL/pgvector operations (table: cluttr_memories)
│   ├── embeddings/      # Embedding services (Bedrock, OpenAI)
│   ├── llm/             # LLM services for memory extraction
│   └── models.py        # Memory, Message, SearchResult models
├── examples/
│   ├── chat_with_memory.py        # Example with Bedrock
│   └── chat_with_memory_openai.py # Example with OpenAI
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
- **Duplicate detection**: Uses LLM to determine if new facts are already covered
- **Query expansion**: Search queries are automatically optimized by LLM for better vector matching
- **Image support**: Images are summarized by LLM before storage
- **Providers**: Supports AWS Bedrock and OpenAI
- **Supabase compatible**: Works with Supabase (pgvector in extensions schema)

## Versioning

**Important**: When making changes to the package (src/cluttr/), bump the version in `pyproject.toml` before committing. The package is published to PyPI, so version updates are required for new releases.

```bash
# Version is in pyproject.toml
version = "0.1.0"  # Update this
```

Follow semantic versioning:
- **Patch** (0.1.x): Bug fixes
- **Minor** (0.x.0): New features, backward compatible
- **Major** (x.0.0): Breaking changes
