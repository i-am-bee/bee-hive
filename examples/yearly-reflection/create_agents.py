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

    assistant2 = client.beta.assistants.create(
        name="Generate Categories Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="can you create a few categories that encapsulate the tasks? + file",
        instructions="""
            You will receive a file containing a detailed account of tasks a developer has completed over the past year. Identify about 5-10 overarching categories using the Python Interpreter's counter to identify the most common occuring words, then create categories based on these words that can encapsulate the tasks.
            Generate new, broad groupings that effectively encompass all the tasks described. Your output should consist solely of the categories you create, and make sure that in the categories created, there aren't duplicated words, otherwise just combine the category.
            Note:
            the categories should not be one word, but more so something like 'AI chatbot' or 'bee-hive development' or 'qiskit code assistant'. Something that can encapsulate multiple tasks.
            """ )
    print("Generate Categories Bee created")
    print(f"NAME: {assistant2.name}")
    print(f"ID:  {assistant2.id}")
    print("Enable Only the Python interpreter for the Generate Categories Bee")
    print("\n")

    agent_store[assistant2.name] = assistant2.id

    assistant3 = client.beta.assistants.create(
        name="Create Dataframe Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="can you create a dataframe from this file?",
        instructions="""
            You will receive a file containing a detailed account of tasks a developer has completed over the past year. Create a dataframe,
            and for each update (which should be almost always a new sentence), create an entry for that in the dataframe.

            Then, remove any duplicate entries, empty lines, etc.
            Output a pickle file that I can use to pass in again later.
            """ )
    print("Create Dataframe Bee created")
    print(f"NAME: {assistant3.name}")
    print(f"ID:  {assistant3.id}")
    print("Enable Only the Python interpreter for the Create Dataframes Bee")
    print("\n")
    agent_store[assistant3.name] = assistant3.id

    # assistant4 = client.beta.assistants.create(
    #     name="Category Assigner Bee",
    #     model="meta-llama/llama-3-1-70b-instruct",
    #     description="can you assign a category for each entry in the dataframe?",
    #     instructions="""
    #         You will receive a pickle file containing a dataframe with each entry containing a task a developer has completed over the past year.
    #         You will also be given a list of categories, like ["cat1","cat2", etc]. Create a new column called category and assign the most relevant 
    #         category you think to the entry.

    #         Output a pickle file that I can use to pass in again later.
    #         """ )
    # print("Category Assigner Bee created")
    # print(f"NAME: {assistant4.name}")
    # print(f"ID:  {assistant4.id}")
    # print("Enable Only the Python interpreter for the Category Assigner Bee")
    # print("\n")
    # agent_store[assistant4.name] = assistant4.id

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)

if __name__ == "__main__":
    create_agents()