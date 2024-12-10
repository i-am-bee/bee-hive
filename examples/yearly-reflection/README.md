# Weather-Checker Example
A multi-agent workflow using Bee-Hive to get your yearly contributions.
## Getting Started
* Run a local instance of the Bee Stack
* Install dependencies: `pip install -r bee-hive/requirements.txt`
* Configure environmental variables: `cp example.env .env`
* Create the agents: `./create_agents.py` -- note you'll need to enable some tools in the UI ( http://localhost:3000 )

TODO:
* Figure out how to save the data file generated from first agent, then pass into the next agent.
* Run the workflow: `./hive workflow.yaml` (to run for a different city, change the `prompt` field in `workflow.yaml`)