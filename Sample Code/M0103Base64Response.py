from litellm import completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer
import base64

class Base64Response(APIKeyInitializer):
    def __init__(self):
        super().__init__()

def generate_response(messages: List[Dict]) -> str:
    print("Running Base64Response...")
    """Call LLM to get response"""
    if messages is None:
        messages = [{"role": "user", "content": "What is the capital of France?"}]
    response = completion(model="openai/gpt-4o", 
                          messages=messages,
                          max_tokens=1024
                          )
    return response.choices[0].message.content

messages = [
    {"role": "system", "content": "You are an expert AI system capable of responding with base64 encoded data strings."},
    {"role": "user", "content": "please provide two responses, the first, your name and the second your name as a base64 encoded string."}
]

# execute the function
if __name__ == "__main__":
    app = Base64Response()
    response = generate_response(messages=messages)
    print(response)
    print(f"Base64 Encoded Response: is {base64.b64encode(b"OpenAI Assistant").decode()}")

    