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

def terminate(message: str) -> None:
    """ Terminate the agent loop and provide a summary message. """
    print(f"Termination Message: {message}")

tool_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "terminate": terminate
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
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "Terminates the conversation. No further actions or interactions are possible after this. Print the provided message for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
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
            When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.
        """
    }
]

# Initialize agent parameters
iterations = 0
max_iterations = 10

memory: List[Dict] = []

"""memory = [
    {
        "role": "user",
        "content": user_task_input
    }
]"""

if __name__ == "__main__":

    app = LLMFunctionCalling()

    # The agent loop
    while iterations < max_iterations:
        user_task_input = input("What would you like me to do?")
        memory.extend([
            {"role": "user", "content": user_task_input}
        ])
        messages = agent_rules + memory
        response = generate_response (messages=messages, tools=tools)
        print("="*50)
        print(response)
        print("="*50)
        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            tool_name = tool.function.name
            tool_args = json.loads(tool.function.arguments)

            action = {
                "tool_name": tool_name,
                "args": tool_args
            }

            if tool_name == "terminate":
                print(f"Termination message: {tool_args['message']}")
                break
            elif tool_name in tool_functions:
                try:
                    result = {"result": tool_functions[tool_name](**tool_args)}
                except Exception as e:
                    result = {"error": f"Error executing {tool_name}: {str(e)}"}
            else:
                result = {"result": f"Unknown tool: {tool_name}"}

            print(f"Executing: {tool_name} with args {tool_args}")
            print(f"Result: {result}")

            memory.extend([
                {"role": "assistant", "content": json.dumps(action)},
                {"role": "user", "content": json.dumps(result)}
            ])
        else:
            result = response.choices[0].message.content.strip()
            print(f"Response[{iterations}]: {result}")

        iterations += 1
        print(f"Iteration count: {iterations}")
