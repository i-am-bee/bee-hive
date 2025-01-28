#! /usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys

import yaml
import dotenv
from .step import Step
from .bee_agent import BeeAgent

dotenv.load_dotenv()


class Workflow:
    agents = {}
    steps = {}
    workflow = {}
    def __init__(self, agent_defs, workflow):
        """Execute sequential workflow.
        input:
            agents: array of agent definitions
            workflow: workflow definition
        """
        for agent_def in agent_defs:
            self.agents[agent_def["metadata"]["name"]] = BeeAgent(agent_def)
        self.workflow = workflow


    def run(self):
        """Execute workflow."""

        if (self.workflow["spec"]["strategy"]["type"]  == "sequence"):
            return self._sequence()
        elif (self.workflow["spec"]["strategy"]["type"]  == "condition"):
            return self._condition()
        else:
            print("not supported yet")   

    def _sequence(self):
        prompt = self.workflow["spec"]["prompt"]
        steps = self.workflow["spec"]["steps"]
        for step in steps:
            step_name = step["name"]
            agent_name = step["agent"]
            agent_instance = self.agents.get(agent_name)
            if not agent_instance:
                raise ValueError(f"Agent {agent_name} not found for step {step_name}")
            self.steps[step_name] = Step({"name": step_name, "agent": agent_instance})

        for step_name, step_obj in self.steps.items():
            response = step_obj.run(prompt)  
            prompt = response.get("prompt", prompt)
        return prompt

    def _condition(self):
        prompt = self.workflow["spec"]["template"]["prompt"]
        steps = self.workflow["spec"]["template"]["steps"]
        for step in steps:
            if step["agent"]:
                step["agent"] = self.agents.get(step["agent"])
            self.steps[step["name"]] = Step(step)
        current_step = self.workflow["spec"]["template"]["start"]
        while current_step != "end":
            response = self.steps[current_step].run(prompt)
            prompt = response["prompt"]
            current_step = response["next"]
        return prompt
