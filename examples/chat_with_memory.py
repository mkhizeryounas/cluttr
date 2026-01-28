"""Example: Chat with memory using cluttr."""

import asyncio
import json
import os

import boto3

from cluttr import Cluttr

# Database configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "cluttr")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

# AWS/Bedrock configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
LLM_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"


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
            "provider": "bedrock",
            "region": AWS_REGION,
            "model": LLM_MODEL,
            "embedding_model": EMBEDDING_MODEL,
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "aws_session_token": AWS_SESSION_TOKEN,
        },
        "default_user_id": user_id,
        "default_agent_id": agent_id,
    }

    # Create Cluttr memory instance
    memory = Cluttr(config)

    # Create Bedrock client for chat
    bedrock_kwargs = {"region_name": AWS_REGION}
    if AWS_ACCESS_KEY_ID:
        bedrock_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
    if AWS_SECRET_ACCESS_KEY:
        bedrock_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        bedrock_kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    bedrock = boto3.client("bedrock-runtime", **bedrock_kwargs)

    print(f"\nConnected as user '{user_id}' with agent '{agent_id}'")
    print("Type 'quit' to exit\n")

    async with memory:
        messages = []

        while True:
            # Get user input
            user_input = input("You: ").strip()
            if user_input.lower() == "quit":
                break
            if not user_input:
                continue

            # Search for relevant memories
            memories = await memory.search(user_input, k=5)

            # Build context from memories
            memory_context = ""
            if memories:
                memory_lines = [f"- {m.memory.content}" for m in memories]
                memory_context = "Relevant information about this user:\n" + "\n".join(memory_lines)

            # Build system prompt with memory context
            system_prompt = "You are a helpful assistant."
            if memory_context:
                system_prompt += f"\n\n{memory_context}"

            # Add user message to history
            messages.append({"role": "user", "content": user_input})

            # Call LLM
            response = bedrock.invoke_model(
                modelId=LLM_MODEL,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "system": system_prompt,
                    "messages": messages,
                }),
                contentType="application/json",
                accept="application/json",
            )

            response_body = json.loads(response["body"].read())
            assistant_message = response_body["content"][0]["text"]

            # Add assistant response to history
            messages.append({"role": "assistant", "content": assistant_message})

            print(f"Assistant: {assistant_message}\n")

            # Save conversation to memory (only user + assistant, no system)
            added = await memory.add(messages[-2:])
            if added:
                print(f"  [Saved {len(added)} new memory/memories]\n")


if __name__ == "__main__":
    asyncio.run(main())
