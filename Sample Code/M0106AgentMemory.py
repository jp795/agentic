from litellm import completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer

class AgentMemory(APIKeyInitializer):
    def __init__(self):
        super().__init__()

def generate_response(messages: List[Dict]) -> str:
    """
    Generate a response based on the conversation history.
    Args:
        messages (List[Dict]): A list of message dictionaries, each containing 'role' and 'content'.
    Returns:
        str: The generated response from the agent.
    """
    response = completion (
        model = "openai/gpt-4o",
        messages=messages,
        max_tokens = 1024
    )

    return response.choices[0].message.content

messages_v1 = [
    {"role": "system", "content": "You are an expert softweare engineer that prefers functional programming"},
    {"role": "user", "content": "Write a function in python to swap the keys and values in a given dictionary"},
]

messages_v1_1 = [
    {"role": "user", "content": "Update the code to include documentation"}
]

if __name__ == "__main__":
    app = AgentMemory()
    response_1 = generate_response(messages_v1)
    print(f"Response v1: {response_1}")
    print("\n---\n")
    print("Now LLM call to update documentation without assistant role included...")
    print("\n---\n")
    response_1_1 = generate_response(messages_v1_1)
    print(f"Response v2: {response_1_1}")    
    print("\n---\n")
    print("Now LLM call with assistant role included...")

    messages_v2 = [
        {"role": "system", "content": "You are an expert softweare engineer that prefers functional programming"},
        {"role": "user", "content": "Write a function in python to swap the keys and values in a given dictionary"},
        {"role": "assistant", "content": response_1},
        {"role": "user", "content": "Update the code to include documentation"}
    ]

    print("\n---\n")
    response_2 = generate_response(messages_v2)
    print(f"Response v2: {response_2}")
