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


    agent3_query = """Using the provided file, follow the instructions and answer the questions provided.

Each answer must include exactly three bullet points, each of which is at least three full sentences long (longer is encouraged).
The tone of the bullet points should be accomplishment-driven and boastful, reflecting the significance of your contributions.
Every bullet point must provide specific examples of tasks or achievements from the categories of work or tasks identified earlier. Use these examples to highlight accomplishments from the past year. Make sure to answer all the questions!

Key Requirements for Each Bullet Point:
Describe the task or project and your role in it, emphasizing your ownership, leadership, or creativity.
Provide examples of the work, including measurable outcomes, whenever possible (e.g., reduced error rates, increased efficiency, improved integration).
Explain how the task contributes to the company’s broader vision of quantum computing, such as advancing quantum algorithms, enhancing AI integration, or achieving operational efficiency (should focus on this, and can use tools to help).

Additional Notes:

Be precise and data-driven but avoid making up metrics. If measurable outcomes aren’t available, describe the qualitative impact with concrete examples (e.g., fostering collaboration, creating scalable solutions, or overcoming a significant technical challenge).
Focus on crafting responses that not only showcase accomplishments but also align with strategic goals, presenting your work as indispensable to the company's success."""

    assistant3 = client.beta.assistants.create(
        name="Summary Bee",
        model="meta-llama/llama-3-1-70b-instruct",
        description="copy description:",
        instructions="""You will be provided with a dataframe containing two columns, one containing the actual task, the other with the category of the task it is.

Overall, read in the dataframe as context, then use any tools like wikipedia,arXiv (but not necessary) in order to help you determine the most important tasks to answer the following questions specifically in detail. You must answer all these questions in your response, and each response should have 3 bullet points with at least 3 sentences each. So overall, we should have 9 bullet points with multiple sentence reponses.

(1) Share the top 3 Business Outcomes that were driven through these projects with some detailed explanations.
(2) Share the top 3 Skills developed and how they were applied in the projects
(3) Share the top 3 Areas that one can focus on next to continue growth
Since this is for performance eval, make sure to be specific and have examples to support your answers, show potential value. Have at least 3 sentences per bullet point.

One example output for each of the questions:
(1) Accelerated Quantum Adoption through support models: 
Allowing users to have easier time debugging issues in Qiskit and exploring how to convert to post-quantum cryptography.

(2) Retrieval Augmented Generation (allowed me to focus on a specific area, even after data has been trained)

Used RAG to store quantum-specific related documents (which is important because new docs come out every day and we cannot retrain the model). This allows us to access new information, key for new quantum technology.
 
(3) Multi Agent Frameworks
Continue to work on and see if agents can be used to solve problems, specifically in the quantum space where ibm granite has an advantage. I hope to read more research papers.""" )
    print("summary Bee created")
    print(f"NAME: {assistant3.name}")
    print(f"ID:  {assistant3.id}")
    print("Enable all tools except duckduckgo, openmateo and readfile for summary bee.")
    print("\n")
    print(f"Copy this to use as your query: \n {agent3_query}")
    agent_store[assistant3.name] = assistant3.id

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)

if __name__ == "__main__":
    create_agents()