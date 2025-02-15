from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define your API key and endpoint
api_key = os.getenv("GPT4O_API_KEY")
gpt4o_api_url = "https://api.openai.com/v1/gpt-4o/debugging"

class GPT4oDebuggingTool(BaseTool):
    """
    This tool interfaces with the GPT-4o API to provide debugging assistance for code.
    It accepts code input, sends it to the GPT-4o API, and returns debugging suggestions or corrections.
    """

    code_input: str = Field(
        ..., description="The code input to be debugged."
    )

    def run(self):
        """
        Sends code data to the GPT-4o API and receives debugging suggestions.
        Handles exceptions and errors gracefully, providing meaningful error messages if the debugging assistance fails.
        """
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'prompt': f"Debug the following code:\n{self.code_input}",
                'max_tokens': 150  # Adjust the max tokens as needed
            }

            # Send the request to the GPT-4o API
            response = requests.post(gpt4o_api_url, headers=headers, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                debugging_result = response.json()
                return debugging_result.get('choices', [{}])[0].get('text', 'No debugging suggestions provided.')
            else:
                return f"Error: Received status code {response.status_code} - {response.text}"

        except requests.exceptions.RequestException as e:
            return f"Error: An error occurred while making the request to the GPT-4o API - {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"