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


    agent2_query = """Using the steps provided in the instructions, categorize the tasks given in the file by identifying overarching categories based on your natural language understanding and assign each task to the most appropriate category. Generate a clean and structured dataframe containing the tasks and their assigned categories, DO NOT create 'unknown' categories! Each one must have an actual category. Use YOUR OWN LLM understanding to assign categories, NOT python!!!! Save the resulting dataframe as a downloadable pickle file. Do not output any intermediate steps or results until the entire process is complete."""
    assistant2 = client.beta.assistants.create(
        name="Generate Categories Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description=
        """
        Copy the description in terminal into the query.
        """,
        instructions=
        """
        Step 1: Categorization
        You will receive a file containing a detailed account of tasks a developer has completed over the past year. Using your understanding of the content, identify 5-10 overarching categories that best represent the tasks. These categories should be descriptive and summarize the nature of the work (e.g., "AI chatbot development," "Quantum-safe cryptography"). Save these categories as context for later use. Do not output anything at this step.

        Step 2: Dataframe Creation
        Process the file to create a dataframe where each task update (typically a single sentence or line) forms one entry. You may have to use sep(\t) when reading the csv. Clean the dataframe by:

        Removing duplicate entries.
        Eliminating empty lines.
        Discarding any irrelevant or incomplete data.
        The cleaned dataframe will be used for categorization.

        Step 3: Task Categorization
        For each entry in the dataframe created in Step 2, assign the most relevant category identified in Step 1. Use your own natural language understanding to determine the best match for each task. Ensure every task is assigned to one of the predefined categories.

        Step 4: Final Output
        Once categorization is complete:

        Save the resulting dataframe (with tasks and their assigned categories) as a pickle file.
        Provide the pickle file for download.
        Do not output any intermediate results until the process is fully complete.""" 
    )

    print("Generate Categories Bee created")
    print(f"NAME: {assistant2.name}")
    print(f"ID:  {assistant2.id}")
    print(f"Copy this to use as your query: \n {agent2_query}")
    print("Enable Only the Python interpreter for the Generate Categories Bee")
    print("\n")

    agent_store[assistant2.name] = assistant2.id

    assistant3 = client.beta.assistants.create(
        name="Summary Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="create the summary for each category in the given file:",
        instructions="""
        You will be provided with a dataframe containing two columns, but note that the column names may vary. First, use df.columns to identify the correct column names for:

        The column that describes the tasks a developer has completed over the year.
        The column that indicates the category assigned to each task/update.
        Your task is to:

        Group the data frame by the category column (identified in step 1).
        For each category, generate a COHERENT, mid-level summary of the tasks in that category by combining your understanding of the listed tasks with tools like DuckDuckGo, Arxiv, Wikipedia to create meaningful summaries that demonstrate the impact of the overall work done with respect to Artifical Intelligence and Quantum Computing within each category. However, do not use the python intepreter for generating the summary, you should do that yourself.
        The length of each summary should be around 150-200 words.

        Write the grouped summaries into a .txt file, clearly labeling each category and including its generated summary underneath.
        Ensure the output is organized, with each category followed by its generated summary. Do not simply list the tasks—instead, analyze them to provide a cohesive summary for each category. 
        """ )
    print("summary Bee created")
    print(f"NAME: {assistant3.name}")
    print(f"ID:  {assistant3.id}")
    print("Enable all tools except openmateo and readfile for summary bee.")
    print("\n")
    agent_store[assistant3.name] = assistant3.id

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)

if __name__ == "__main__":
    create_agents()