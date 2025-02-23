from agency_swarm.agents import Agent


class CodeDebuggerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CodeDebuggerAgent",
            description="The CodeDebuggerAgent is responsible for debugging the code generated by the CodeGeneratorAgent to ensure it functions correctly and meets the user's requirements.",
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
