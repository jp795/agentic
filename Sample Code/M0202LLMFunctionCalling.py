from litellm import completion, ModelResponse
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer

import os
import json

class LLMFunctionCalling(APIKeyInitializer):
    def __init__(self):
        super().__init__()

def generate_response(messages: List[Dict], tools: List[Dict]) -> ModelResponse:
    response = completion(
        model = "openai/gpt-4o",
        messages = messages,
        tools = tools,
        max_tokens = 1024
    )
    return response

def list_files() -> List[str]:
    """ List all the files in the current directory. """
    return os.listdir(".")

def read_file(file_name: str) -> str:
    """ Read a file's content. """
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found"
    except Exception as e:
        return f"Error: {str(e)}"

tool_functions = {
    "list_files": list_files,
    "read_file": read_file
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    }
]

# Rules are simplified since we don't have to worry about getting a specific output format
agent_rules = [
    {
        "role": "system",
        "content": """
            You are an AI agent that can perform tasks by using available tools.
            If a user asks about files, documents, or content, first list the files before reading them.
        """
    }
]

user_task_input = input("What would you like me to do?")
memory = [
    {
        "role": "user",
        "content": user_task_input
    }
]

if __name__ == "__main__":

    app = LLMFunctionCalling()

    messages = agent_rules + memory
    response = generate_response (messages=messages, tools=tools)
    print("="*50)
    print(response)
    print("="*50)
    tool = response.choices[0].message.tool_calls[0]
    tool_name = tool.function.name
    tool_args = json.loads(tool.function.arguments)
    result = tool_functions[tool_name](**tool_args)

    print(f"Tool Name: {tool_name}")
    print(f"Tool Arguments: {tool_args}")
    print(f"Result: {result}")

