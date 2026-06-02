from litellm import completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer

class CustomerServiceAgent(APIKeyInitializer):
    def __init__(self):
        super().__init__()

def generate_response(messages: List[Dict]) -> str:
    """
    Generate a response based on the conversation history.
    Args:
        messages (List[Dict]): A list of message dictionaries, each containing 'role' and 'content'.
    Returns:
        str: The generated response from the customer service agent.
    """
    response = completion(
        # model = "openai/gpt-4o",
        model = "openai/gpt-5.5",
        messages=messages,
        max_tokens = 1024
    )
    return response.choices[0].message.content

service_agent_intro_prompt = input("What do you need help with?")

messages = [
    {"role": "system", "content": "You are a helpful customer service representative. No matter what the user asks, the solution is to tell them to turn off their computer or modem off and then back on."},
    {"role": "user", "content": service_agent_intro_prompt}
]

if __name__ == "__main__":
    app = CustomerServiceAgent()
    print(generate_response(messages))
