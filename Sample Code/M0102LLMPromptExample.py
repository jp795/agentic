from litellm import completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer

class PromptExample(APIKeyInitializer):
    def __init__(self):
        print("Initializing PromptExample...")
        super().__init__()

# function expecting a list of messages (dictionaries) as input and returning a string response
def generate_response(messages: List[Dict] = None) -> str:
    print("Running PromptExample...")
    """Call LLM to get response"""
    if messages is None:
        messages = [{"role": "user", "content": "What is the capital of France?"}]
    response = completion(model="openai/gpt-4o", 
                          messages=messages,
                          max_tokens=1024
                          )
    return response.choices[0].message.content

# define the messages
messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

if __name__ == "__main__":
    # Initialize the example
    app = PromptExample()
    # Run the main function
    response = generate_response(messages=messages)
    print(response)
