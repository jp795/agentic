import os
import json
from litellm import completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer
from M0100LLMResponseSchema import LLMResponseSchema

class AgentWithTools(APIKeyInitializer):

    # definne a class level attribute to store the responses
    responses: List[LLMResponseSchema] = None

    def __init__(self):
        super().__init__()

    def addResponse(self, response: LLMResponseSchema):
        if self.responses is None:
            self.responses = []
        self.responses.append(response)
        print(f"Response list length is now {len(self.responses)}")

    def generate_response(self, messages: List[Dict]) -> str:
        response = completion(
            model = "openai/gpt-4o",
            messages= messages,
            # https://docs.litellm.ai/docs/completion/json_mode
            # response_format={
            #    "type": "json_object"
            #},
            # response_format= LLMResponseSchema,
            max_tokens = 1024
        )
        print(f"Response choice length is {len(response.choices)}")
        response_raw_content = response.choices[0].message.content
        print("=" * 50)
        print(f"Raw Response: {response}")
        print("=" * 50)
        print(f"Raw Message Content String: {response_raw_content}")
        print("=" * 50)
        # load the raw JSON formatted data from LiteLLM into the LLMResponseSchema pydantic model for validation and parsing
        """response_parsed = LLMResponseSchema.model_validate_json(response_raw_content)
        self.addResponse(response_parsed)
        # displaying each field of the response separately for clarity
        print(f"Conversation Introduction:\n {response_parsed.conv_intro}\n")
        print("=" * 50)
        print(f"LLM Final Response:\n {response_parsed.llm_response}\n")
        print("=" * 50)
        print(f"Programming Language: {response_parsed.programming_language}\n")
        print("=" * 50)
        print(f"Conversation Outro:\n {response_parsed.conv_outro}\n")
        print("=" * 50)
        """
        return response_raw_content.strip()

    def list_files(self) -> List[str]:
        """ List files in the current directory. """
        return os.listdir(".")
    
    def read_file(self, file_name: str) -> str:
        """ Read a file's contents. """
        try:
            with open(file_name, "r") as file:
                return file.read()
        except FileNotFoundError:
            return f"Error: {file_name} not found."
        except Exception as e:
            return f"Error: {str(e)}"

    """ Example code provided """
    def extract_markdown_block(self, response: str, block_type: str = "json") -> str:
        """Extract code block from response"""

        if not '```' in response:
            return response

        code_block = response.split('```')[1].strip()

        if code_block.startswith(block_type):
            code_block = code_block[len(block_type):].strip()

        return code_block

    def parse_action(self, response: str) -> Dict:
        """Parse the LLM response into a structured action dictionary."""
        try:
            response = self.extract_markdown_block(response, "action")
            response_json = json.loads(response)
            if "tool_name" in response_json and "args" in response_json:
                return response_json
            else:
                return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
        except json.JSONDecodeError:
            return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}

# Fine system instructions, which includes Agent Tools and Rules
# OpenAIException - Invalid value: 'User'. Supported values are: 'system', 'assistant', 'user', 'function', 'tool', and 'developer'.
agent_rules = [
    {
        "role": "system",
        "content": """
            You are an AI agent that can perform tasks by using available tools.
            Available Tools:
            ```json
            {
                "list_files": {
                    "description": "Lists all files in the current directory.",
                    "parameters": {}
                }
                "read_file": {
                    "description": "Reads the content of a file.",
                    "parameters": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file to read."
                        }
                    }
                }
                "terminate": {
                    "description": "Ends the agent loop and provides a summary of the task.",
                    "parameters": {
                        "message": {
                            "type": "string",
                            "description": "Summary message to return to the user."
                        }
                    }
                }
            }
            ```
            if a user asks about files, documents, or content, first list the files before reading them.
            When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.
            Important!!! Every response MUST have an action.
            You must always respond in this format:
            <Stop and think step by step. Parameters map to args. Insert a rich description of your step by step throughs here.>
            ```action
            {
                "tool_name": "insert tool name",
                "args": {...fill in any required arguments here...}
            }
            ```
        """
    }
]

# Initialze agent parameters
iterations = 0
max_iterations = 10

if __name__ == "__main__":
    app = AgentWithTools()

    user_task = input("what would you like me to do?")
    memory = [{"role": "user", "content": user_task}]

    # The agent loop
    while iterations < max_iterations:
        # 1. Construct the prompt: Combine agent rules with memory
        prompt = agent_rules + memory

        # 2. Generate response from LLM
        print("Agent thinking...")
        response = app.generate_response(prompt)
        print(f"Agent response: {response}")

        # 3. Parse response to determine action
        action = app.parse_action(response)
        result = "Action executed."

        if action["tool_name"] == "list_files":
            result = {"result": app.list_files()}
        elif action["tool_name"] == "read_file":
            result = {"result": app.read_file(action["args"]["file_name"])}
        elif action["tool_name"] == "error":
            result = {"error": action["args"]["message"]}
        elif action["tool_name"] == "terminate":
            print(action["args"]["message"])
            break
        else:
            result = {"error": "Unknown action: " + action["tool_name"]}

        print(f"Action result: {result}")

        # 5. Update memory with response and results
        memory.extend([
            {"role": "assistant", "content": response},
            {"role": "user", "content": json.dumps(result)}
        ])

        # 6. Check termination condition
        if action["tool_name"] == "terminate":
            break

        iterations += 1