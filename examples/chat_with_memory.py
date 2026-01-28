"""Example: Chat with memory using cluttr."""

import asyncio
import json
import os

import boto3

from cluttr import MemoryConfig


async def main():
    # Get user and agent IDs
    user_id = input("Enter user ID (or press Enter for 'default_user'): ").strip()
    user_id = user_id or "default_user"

    agent_id = input("Enter agent ID (or press Enter for 'default_agent'): ").strip()
    agent_id = agent_id or "default_agent"

    # Get database connection string
    db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cluttr")

    # Configure and connect
    config = MemoryConfig.from_connection_string(
        db_url,
        default_user_id=user_id,
        default_agent_id=agent_id,
    )

    # Create Bedrock client for chat
    bedrock = boto3.client("bedrock-runtime", region_name=config.bedrock.region_name)

    print(f"\nConnected as user '{user_id}' with agent '{agent_id}'")
    print("Type 'quit' to exit\n")

    async with await config.connect() as client:
        messages = []

        while True:
            # Get user input
            user_input = input("You: ").strip()
            if user_input.lower() == "quit":
                break
            if not user_input:
                continue

            # Search for relevant memories
            memories = await client.search(user_input, k=5, user_id=user_id, agent_id=agent_id)

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
                modelId=config.bedrock.llm_model_id,
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

            # Save conversation to memory
            added = await client.add(messages[-2:], user_id=user_id, agent_id=agent_id)
            if added:
                print(f"  [Saved {len(added)} new memory/memories]\n")


if __name__ == "__main__":
    asyncio.run(main())
