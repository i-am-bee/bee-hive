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
        name="Yearly Review Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="Retrieve your own updates for the year.",
        instructions="""
        Using the provided file, extract all updates from [name]. These updates will appear multiple times, as they are part of a weekly meeting format. Each update is located in the section of text between [name] and the next listed participant, [name2].

        Refer to the template below to identify the sequence of participants. Scan the entire document, record all updates attributed to [name], and write them to a .txt file.

        Template Example:

        [Angelo]
        [Mariam]
        [Aki]
        [Alex]
        [George]
        [Karla]
        [Max]
        [Nigel]
        [Paul]
        """ )

    print("Yearly Review Bee created")
    print(f"NAME: {assistant1.name}")
    print(f"ID:  {assistant1.id}")
    print("Enable Only the Python interpreter for the Yearly Review Bee")
    print("\n")

    agent_store[assistant1.name] = assistant1.id

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)

if __name__ == "__main__":
    create_agents()