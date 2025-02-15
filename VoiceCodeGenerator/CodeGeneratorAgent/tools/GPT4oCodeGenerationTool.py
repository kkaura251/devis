from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define your API key and endpoint
api_key = os.getenv("GPT4O_API_KEY")
gpt4o_api_url = "https://api.openai.com/v1/gpt-4o/code-generation"

class GPT4oCodeGenerationTool(BaseTool):
    """
    This tool interfaces with the GPT-4o API to generate code from transcribed text.
    It accepts text input, sends it to the GPT-4o API, and returns the generated code.
    """

    text_input: str = Field(
        ..., description="The transcribed text input to be converted into code."
    )

    def run(self):
        """
        Sends text data to the GPT-4o API and receives the generated code.
        Handles exceptions and errors gracefully, providing meaningful error messages if the code generation fails.
        """
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'prompt': self.text_input,
                'max_tokens': 150  # Adjust the max tokens as needed
            }

            # Send the request to the GPT-4o API
            response = requests.post(gpt4o_api_url, headers=headers, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                code_generation_result = response.json()
                return code_generation_result.get('choices', [{}])[0].get('text', 'No code generated.')
            else:
                return f"Error: Received status code {response.status_code} - {response.text}"

        except requests.exceptions.RequestException as e:
            return f"Error: An error occurred while making the request to the GPT-4o API - {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"