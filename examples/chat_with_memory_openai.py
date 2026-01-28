"""Example: Chat with memory using cluttr and OpenAI."""

import asyncio
import os

import openai

from cluttr import Cluttr

# Load .env file in development
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Database configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "cluttr")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

# OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"


async def main():
    # Get user and agent IDs
    user_id = input("Enter user ID (or press Enter for 'default_user'): ").strip()
    user_id = user_id or "default_user"

    agent_id = input("Enter agent ID (or press Enter for 'default_agent'): ").strip()
    agent_id = agent_id or "default_agent"

    # Configuration
    config = {
        "vector_db": {
            "engine": "postgres",
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
        },
        "llm": {
            "provider": "openai",
            "api_key": OPENAI_API_KEY,
            "model": LLM_MODEL,
            "embedding_model": EMBEDDING_MODEL,
        },
    }

    # Create Cluttr memory instance
    memory = Cluttr(config)

    # Create OpenAI client for chat
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    print(f"\nConnected as user '{user_id}' with agent '{agent_id}'")
    print("Type 'exit' to quit\n")

    async with memory:
        messages = []

        while True:
            # Get user input
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break
            if not user_input:
                continue

            # Search for relevant memories
            memories = await memory.search(
                user_input, k=5, user_id=user_id, agent_id=agent_id
            )

            # Build context from memories
            memory_context = ""
            if memories:
                memory_lines = [f"- {m.memory.content}" for m in memories]
                memory_context = (
                    "Relevant information about this user:\n" + "\n".join(memory_lines)
                )

            # Build system prompt with memory context
            system_prompt = "You are a helpful assistant."
            if memory_context:
                system_prompt += f"\n\n{memory_context}"

            # Add user message to history
            messages.append({"role": "user", "content": user_input})

            # Call LLM
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "system", "content": system_prompt}, *messages],
                max_tokens=1024,
            )

            assistant_message = response.choices[0].message.content

            # Add assistant response to history
            messages.append({"role": "assistant", "content": assistant_message})

            print(f"Assistant: {assistant_message}\n")

            # Save conversation to memory (only user + assistant, no system)
            added = await memory.add(messages[-2:], user_id=user_id, agent_id=agent_id)
            if added:
                print(f"  [Saved {len(added)} new memory/memories]\n")


if __name__ == "__main__":
    asyncio.run(main())
