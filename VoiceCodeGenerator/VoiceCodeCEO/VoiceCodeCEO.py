from agency_swarm.agents import Agent


class VoiceCodeCEO(Agent):
    def __init__(self):
        super().__init__(
            name="VoiceCodeCEO",
            description="The VoiceCodeCEO is responsible for overseeing the entire process of converting voice input into functional code. It coordinates between the VoiceInputAgent, CodeGeneratorAgent, and CodeDebuggerAgent to ensure the final output meets the user's requirements.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
