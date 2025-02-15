from agency_swarm.agents import Agent


class VoiceInputAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VoiceInputAgent",
            description="The VoiceInputAgent is responsible for accurately transcribing voice input and passing the transcribed text to the CodeGeneratorAgent.",
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
