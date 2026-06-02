from litellm import ModelResponse, completion
from typing import List, Dict
from M0100APIKeyInit import APIKeyInitializer
from M0100LLMResponseSchema import LLMResponseSchema

class QuasiAgent(APIKeyInitializer):

    # definne a class level attribute to store the responses
    responses: List[LLMResponseSchema]  = None

    def __init__(self):
        super().__init__()

    """
        When you call a method on an object instance (like my_instance.generate_response(messages)), Python automatically and silently passes the instance itself as the very first argument.
        So, even though you only typed one argument (messages), Python is actually executing:
        generate_response(my_instance, messages) — which counts as 2 positional arguments.
        Because your current function definition only expects 1 argument (messages), Python throws an error.

        If generate_response doesn't actually need to use any data from the class instance (it doesn't use self.something), 
        you can also fix this by turning it into a static method by adding the @staticmethod decorator above it and leaving self out.

        when defined as a function of the class, include the paramter self or mark the method as static if it doesn't need to access instance attributes.
    """
    def generate_response(self, messages: List[Dict]) -> str:
        print("Sending request to Open AI through LiteLLM...")
        response = completion (
            model = "openai/gpt-4o",
            messages=messages,
            # https://docs.litellm.ai/docs/completion/json_mode
            # response_format={
            #    "type": "json_object"
            #},
            response_format=LLMResponseSchema,
            max_tokens=1024
        )
        print(f"Response choice length is {len(response.choices)}")
        response_raw_content = response.choices[0].message.content
        print("=" * 50)
        print(f"Raw Response: {response}")
        print("=" * 50)
        print(f"Raw Message Content String: {response_raw_content}")
        print("=" * 50)
        # load the raw JSON formatted data from LiteLLM into the LLMResponseSchema pydantic model for validation and parsing
        response_parsed = LLMResponseSchema.model_validate_json(response_raw_content)
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

        return response_raw_content
    
    def addResponse(self, response: LLMResponseSchema):
        if self.responses is None:
            self.responses = []
        self.responses.append(response)
        print(f"Response list length is now {len(self.responses)}")

    def firstPrompt(self):
        print("Running the first prompt ... ")
        user_input = input ("Provide a description of the python function you want to create:")
        # example: Create a python function prompting user for a word and to check if the entered word is a palindrome.
        messages = [
            {"role": "system", "content": "You are an expert software engineering assistant who loves functional programming and generates python functions."},
            {"role": "system", "content": "You must adhere perfectly to the requested JSON response format"},
            {"role": "user", "content": user_input}
        ]
        response = self.generate_response(messages)
        print(response)

    def secondPrompt(self):
        print("Running the second prompt ... ")
        messages = [
            {"role": "assistant", "content": self.responses[0].llm_response},
            {"role": "user", "content": "Update the code provided by adding comprehensive documentation to the code without the triple character markup, including Function description, Parameter descriptions, Return value description, Example usage, and Edge cases."}
        ]
        response = self.generate_response(messages=messages)
        print(response)

    def thirdPrompt(self):
        print("Running the third prompt ... ")
        messages = [
            {"role": "assistant", "content": self.responses[1].llm_response},
            {"role": "system", "content": "You are an expert software test engineer."},
            {"role": "user", "content": "For the python code provided, add test cases using Python's unittest frmework and the tests should cover Basic functionality, Edge cases, Error cases, and Various input scenarios."}
        ]
        response = self.generate_response(messages=messages)
        print(response)

if __name__ == "__main__":
    app = QuasiAgent()
    app.firstPrompt()
    app.secondPrompt()
    app.thirdPrompt()
