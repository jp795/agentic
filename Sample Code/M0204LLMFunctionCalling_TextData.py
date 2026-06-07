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

def list_files(path: str) -> List[str]:
    """ List all the files in the current directory. """
    """
        Should try one of these methods below
        import glob
        files = glob.glob('/your/directory/**', recursive=False)
    
        Or even simpler with pathlib:
        pythonfiles = [str(p.resolve()) for p in pathlib.Path('/your/directory').iterdir()]
        
        But the single cleanest one-liner with no list comprehension is: pythonimport os
        files = [os.path.abspath(f) for f in os.scandir('/your/directory')]

        The most idiomatic single function call is actually:
        pythonfiles = [entry.path for entry in os.scandir('/your/directory')]
    """
    return os.listdir(path)

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
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory and interprets it if asked by the user.",
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
            You are a helpful AI agent with access to tools that let you 
            explore and read files on the local filesystem.

            Use your tools as needed to fully answer the user's request.
            When you have gathered enough information to give a complete 
            answer, call terminate with your summary.

            Do not terminate before you have actually used the tools 
            necessary to answer the question.
        """
    }
]

# Initialize agent parameters
iterations = 0
max_iterations = 10
user_task_input = input("What would you like me to do?")

memory = [{"role": "user", "content": user_task_input}]
# """Read all the files in "Y://Courses//Vanderbilt-Agentic AI with Python//Projects//Sample Code//text_data" and tell me what they are"""
# """List all the files in the directory "Y://Courses//Vanderbilt-Agentic AI with Python//Projects//Sample Code//text_data" with their absolute path, then read all of them at once and tell me what type of information is in those files"""
# final prompt that worked "read all the files in the current directory and return the type of information contained in those files"

if __name__ == "__main__":

    app = LLMFunctionCalling()

    messages = agent_rules + memory
    # The agent loop
    while iterations < max_iterations:
        response = generate_response (messages=messages, tools=tools)
        print("="*50)
        print(response)
        print("="*50)
        if response.choices[0].message.tool_calls:
            
            # Step 1: Appending the assistant message first (contains the tool_call array)
            # response.choices[0].message is a Pydantic object, not a plain dict and needs to be converted.
            # Pydantic object was being stored raw, may not serialize correctly. convert to plain dict so agent_rules + memory concatenation works
            # Original code: messages.append(response.choices[0].message)
            messages.append(response.choices[0].message.model_dump(exclude_unset=True))

            # Step 2: loop and append each tool result
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)


                if tool_name == "terminate":
                    print(f"Termination message: {tool_args['message']}")
                    exit()
                
                if tool_name in tool_functions:
                    try:
                        result = {"result": tool_functions[tool_name](**tool_args)}
                    except Exception as e:
                        result = {"error": f"Error executing {tool_name}: {str(e)}"}
                else:
                    result = {"result": f"Unknown tool: {tool_name}"}

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps({"result": result})
                    }
                )
                print(f"Executing: {tool_name} with args {tool_args}")
                print(f"Result: {result}")
                """
                tool = response.choices[0].message.tool_calls[0]
                tool_name = tool.function.name
                tool_args = json.loads(tool.function.arguments)

                action = {
                    "tool_name": tool_name,
                    "args": tool_args
                }

                memory.extend([
                    {"role": "assistant", "content": json.dumps(action)},
                    {"role": "user", "content": json.dumps(result)}
                ])
                """
        else:
            result = response.choices[0].message.content.strip()
            print(f"Response[{iterations}]: {result}")

        iterations += 1
        print(f"Iteration count: {iterations}")
