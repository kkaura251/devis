from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define your API key and endpoint
api_key = os.getenv("OPENAI_API_KEY")
whisper_api_url = "https://api.openai.com/v1/whisper/transcriptions"

class WhisperTranscriptionTool(BaseTool):
    """
    This tool interfaces with the OpenAI Whisper API to transcribe voice input into text.
    It handles audio input, sends it to the Whisper API, and returns the transcribed text.
    """

    audio_file_path: str = Field(
        ..., description="The file path of the audio file to be transcribed."
    )

    def run(self):
        """
        Sends audio data to the Whisper API and receives the transcription result.
        Handles exceptions and errors gracefully, providing meaningful error messages if the transcription fails.
        """
        try:
            # Open the audio file in binary mode
            with open(self.audio_file_path, 'rb') as audio_file:
                files = {
                    'file': (self.audio_file_path, audio_file, 'audio/wav')
                }
                headers = {
                    'Authorization': f'Bearer {api_key}'
                }

                # Send the request to the Whisper API
                response = requests.post(whisper_api_url, headers=headers, files=files)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the JSON response
                    transcription_result = response.json()
                    return transcription_result.get('text', 'No transcription text found.')
                else:
                    return f"Error: Received status code {response.status_code} - {response.text}"

        except FileNotFoundError:
            return "Error: The specified audio file was not found."
        except requests.exceptions.RequestException as e:
            return f"Error: An error occurred while making the request to the Whisper API - {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"