import os
import sys
import configparser
import litellm
from M0100APIKeyInit import APIKeyInitializer

class JPExample(APIKeyInitializer):
    def __init__(self):
        print("Initializing JPExample...")
        super().__init__()


def run():
    try:
        # Make a completion call using litellm
        response = litellm.completion(
            model="gpt-3.5-turbo", # You can choose other OpenAI models like "gpt-4", etc.
            # model="gpt-5.5-2026-04-23", # You can choose other OpenAI models like "gpt-4", etc.
            messages=[
                {"role": "user", "content": "Hello, litellm!"}
            ]
        )

        print("Successfully connected to OpenAI using litellm!")
        print("Response:")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your API key is correct and has access to the chosen model.")

# -- executing the function
# __name__ is a built-in hidden variable that Python automatically creates every time it runs a script.
# "__main__" is the specific value Python assigns to that __name__ variable only if that file is the primary file you are executing.
if __name__ == "__main__":
    # Initialize the API key
    app = JPExample()
    # Run the main function
    run()