#! /usr/bin/env python3
import json
import os
from pprint import pprint
import dotenv
from openai import OpenAI, BaseModel

dotenv.load_dotenv()

def create_agents():
    client = OpenAI(base_url=f'{os.getenv("BEE_API")}/v1', api_key=os.getenv("BEE_API_KEY"))

    agent_store = {}

    assistant1 = client.beta.assistants.create(
        name="Current Affairs Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="Get the current weather",
        instructions="Get the current temperature for the location provided by the user. Return results in Fahrenheit."
    )

    print("Current Affairs Bee created")
    print(f"NAME: {assistant1.name}")
    print(f"ID:  {assistant1.id}")
    print("Enable the OpenMateo, ReadFile, and FileSearch tools for the Current Affairs Bee")
    print("\n")

    agent_store[assistant1.name] = assistant1.id

    assistant2 = client.beta.assistants.create(
        name="Hot Or Not Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="Is the current temperature hotter than usual?",
        tools=[{"type": "code_interpreter"}],
        instructions="The user will give you a temperature in Fahrenheit and a location. Use the OpenMateo weather tool to find the average monthly temperature for the location. Answer if the temperature provided by the user is hotter or colder than the average found by the tool."
    )

    print("Hot Or Not Bee created")
    print(f"NAME: {assistant2.name}")
    print(f"ID:  {assistant2.id}")
    print("Enable the OpenMateo tool for the Hot Or Not Bee")

    agent_store[assistant2.name] = assistant2.id

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)

if __name__ == "__main__":
    create_agents()