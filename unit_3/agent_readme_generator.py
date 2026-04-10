from agent_framework import Agent, Goal, Action, ActionRegistry, Environment, AgentFunctionCallingActionLanguage, generate_response
import os
from typing import List

    
# Define the agent's goals
goals = [
    Goal(priority=1, name="Gather Information", description="Read each python file in the path where you are being executed"
                                                            "You can use list_project_files action to list all the files in a "
                                                            "directory and read_project_file action to read the files"
                                                            "make sure that you read all the files in the path and subdirectories"),
    Goal(priority=1, name="Terminate", description="Call the terminate call when you have read all the files "
                                                    "and provide the content of a README written by you in the terminate message"
                                                    "make sure that you write the README in the correct format and structure in markdown format"
                                                    "Keep the readme short and concise")
]

# Define the agent's language
agent_language = AgentFunctionCallingActionLanguage()

def read_project_file(file_name: str) -> str:
    with open(file_name, "r") as f:
        return f.read()

def list_project_files(path: str) -> List[str]:
    return sorted([file for file in os.listdir(path)])

# Define the action registry and register some actions
action_registry = ActionRegistry()
action_registry.register(Action(
    name="list_project_files",
    function=list_project_files,
    description="Lists all files in the project.",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string"}
        },
        "required": ["path"]
    },
    terminal=False
))
action_registry.register(Action(
    name="read_project_file",
    function=read_project_file,
    description="Reads a file from the project.",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {"type": "string"}
        },
        "required": ["name"]
    },
    terminal=False
))
action_registry.register(Action(
    name="terminate",
    function=lambda message: f"{message}\nTerminating...",
    description="Terminates the session and prints the message to the user.",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": []
    },
    terminal=True
))

# Define the environment
environment = Environment()

# Create an agent instance
agent = Agent(goals, agent_language, action_registry, generate_response, environment)

# Run the agent with user input
user_input = "Write a README for this project."
final_memory = agent.run(user_input)

# Print the final memory
# print(final_memory.get_memories())