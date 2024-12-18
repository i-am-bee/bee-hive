from bee_agent import LLM
from bee_agent.memory import TokenMemory
from bee_agent.memory.message import BaseMessage, Role
import math
import asyncio

# Initialize the LLM
llm = LLM()

# Initialize TokenMemory with handlers
memory = TokenMemory(
    llm=llm,
    max_tokens=None,  # Will be inferred from LLM
    capacity_threshold=0.75,
    sync_threshold=0.25,
    handlers={
        "removal_selector": lambda messages: next(
            (msg for msg in messages if msg.role != Role.SYSTEM), messages[0]
        ),
        "estimate": lambda msg: math.ceil((len(msg.role) + len(msg.text)) / 4),
    },
)


async def main():
    try:
        # Add system message
        system_message = BaseMessage.of(
            {"role": Role.SYSTEM, "text": "You are a helpful assistant."}
        )
        await memory.add(system_message)
        print(f"Added system message (hash: {hash(system_message)})")

        # Add user message
        user_message = BaseMessage.of({"role": Role.USER, "text": "Hello world!"})
        await memory.add(user_message)
        print(f"Added user message (hash: {hash(user_message)})")

        # Check initial memory state
        print("\nInitial state:")
        print(f"Is Dirty: {memory.is_dirty}")
        print(f"Tokens Used: {memory.tokens_used}")

        # Sync token counts
        await memory.sync()
        print("\nAfter sync:")
        print(f"Is Dirty: {memory.is_dirty}")
        print(f"Tokens Used: {memory.tokens_used}")

        # Print all messages
        print("\nMessages in memory:")
        for msg in memory.messages:
            print(f"{msg.role}: {msg.text} (hash: {hash(msg)})")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback

        print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())