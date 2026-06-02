from litellm import completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer
import json

class JSONPromptExample(APIKeyInitializer):
    def __init__(self):
        super().__init__()

code_spec = {
    'name': 'swap_keys_values',
    'description': 'Swaps the keys and values in a given dictionary',
    'params': {
        'd': 'A dictionary with unique values.'
    }
}

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

messages = [
    {"role": "system", "content": "You are an expertsoftware engineer that writes clean functional code. You always document your funnctions."},
    {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"}
]

if __name__ == "__main__":
    app = JSONPromptExample()
    print(generate_response(messages))
