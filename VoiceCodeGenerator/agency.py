from agency_swarm import Agency, set_openai_key
from CodeDebuggerAgent import CodeDebuggerAgent
from CodeGeneratorAgent import CodeGeneratorAgent
from VoiceInputAgent import VoiceInputAgent
from VoiceCodeCEO import VoiceCodeCEO
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
set_openai_key(api_key)

# Initialize CEO
ceo = VoiceCodeCEO()
voice_input = VoiceInputAgent()
code_generator = CodeGeneratorAgent()
code_debugger = CodeDebuggerAgent()

agency = Agency([ceo, [ceo, voice_input],
                 [ceo, code_generator],
                 [ceo, code_debugger],
                 [voice_input, code_generator]],
                shared_instructions='./agency_manifesto.md',  # shared instructions for all agents
                max_prompt_tokens=25000,  # default tokens in conversation for all agents
                temperature=0.3,  # default temperature for all agents
                )

if __name__ == '__main__':
    agency.demo_gradio()