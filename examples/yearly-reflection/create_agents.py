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

    assistant4 = client.beta.assistants.create(
        name="Category Assigner Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="given the categories of ['AI Chatbot', 'Research Development','Demos', and 'Paper Summarizer'] could you assign each entry in the dataframe one of them based on your judgement?",
        instructions="""
            Given a pickle file containing a dataframe with each entry representing a task a developer has completed over the past year, Use the list of categories from the prompt query, which will be based like ["cat1","cat2", etc] to MANUALLY ASSIGN each entry in the dataframe to one of the given categories based on your own interpretation, WITHOUT using any tools or Python. Compare the tokens and choose the most similar one out of the given categories. Do not have any unknown values, you must choose one out of the given categories.
            If there are empty or null entries, you can just remove the entry entirely. You should end up creating a separate column in the dataframe to store your assignment.
            Output a pickle file that I can use to pass in again later.    
            """ )
    print("Category Assigner Bee created")
    print(f"NAME: {assistant4.name}")
    print(f"ID:  {assistant4.id}")
    print("Enable Only the Python interpreter for the Category Assigner Bee, and remove the description as it causes errors.")
    print("\n")
    agent_store[assistant4.name] = assistant4.id

    assistant5 = client.beta.assistants.create(
        name="Summary Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="create the summary for each category in the given file:",
        instructions="""
            You will be provided with a dataframe containing two columns, but note that the column names may vary. First, use df.columns to identify the correct column names for:

            The column that describes the tasks a developer has completed over the year.
            The column that indicates the category assigned to each task/update.
            Your task is to:

            Group the data frame by the category column (identified in step 1).
            For each category, generate a written, high-level summary of the tasks in that category by combining your understanding of the listed tasks with tools like DuckDuckGo, Arxiv, Wikipedia to create meaningful summaries that demonstrate the impact of the overall work done with respect to Artifical Intelligence and Quantum Computing within each category. However, do not use the python intepreter for generating the summary, you should do that yourself.
            The length of each summary should be around 150-200 words.

            Write the grouped summaries into a .txt file, clearly labeling each category and including its generated summary underneath.
            Ensure the output is organized, with each category followed by its generated summary. Do not simply list the tasks—instead, analyze them to provide a cohesive summary for each category. 
            """ )
    print("summary Bee created")
    print(f"NAME: {assistant5.name}")
    print(f"ID:  {assistant5.id}")
    print("Enable all tools except openmateo and readfile for summary bee.")
    print("\n")
    agent_store[assistant5.name] = assistant5.id

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)

if __name__ == "__main__":
    create_agents()