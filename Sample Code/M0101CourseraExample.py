import os
import sys
import configparser
import litellm

cfg_path = os.path.join(sys.prefix, 'pyvenv.cfg')
print(f"Reading configuration from: {cfg_path}")
config = configparser.ConfigParser()
with open(cfg_path, 'r') as cfg_file:
    configContent = '[DEFAULT]\n' + cfg_file.read()
config.read_string(configContent)
openai_api_key = config.get('DEFAULT', 'OPENAI_API_KEY')
print(f"OPENAI_API_KEY: {openai_api_key}")

os.environ['OPENAI_API_KEY'] = openai_api_key

from litellm import completion
from typing import List, Dict


def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)