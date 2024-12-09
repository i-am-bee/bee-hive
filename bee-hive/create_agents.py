#! /usr/bin/env python3

import json
import os
from pprint import pprint
import sys

import dotenv
from openai import OpenAI, BaseModel
import yaml

dotenv.load_dotenv()


def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        yaml_data = list(yaml.safe_load_all(file))
    return yaml_data


def create_agent(agent):
    client = OpenAI(base_url=f'{os.getenv("BEE_API")}/v1', api_key=os.getenv("BEE_API_KEY"))

    agent_name = agent["metadata"]["name"]
    agent_model = agent["spec"]["model"]
    agent_desc = agent["spec"]["description"]
    agent_instr = agent["spec"]["instructions"]
    agent_tool = agent["spec"]["tools"][0]

    assistant = client.beta.assistants.create(
        name=agent_name,
        model=agent_model,
        description=agent_desc,
        tools=[{"type": agent_tool }],
        instructions=agent_instr
    )

    return assistant.id


def create_agents(agents_yaml):
    agent_store = {}
    for agent in agents_yaml:
        agentid = create_agent(agent)
        print(agentid)
        agent_store[agent["metadata"]["name"]] = agentid

    with open("agent_store.json", "w") as f:
        json.dump(agent_store, f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python create_agents.py <yaml_file>')
        sys.exit(1)

    file_path = sys.argv[1]
    agents_yaml = parse_yaml(file_path)
    try:
        create_agents(agents_yaml)
    except Exception as excep:
        raise RuntimeError("Unable to create agents") from excep
