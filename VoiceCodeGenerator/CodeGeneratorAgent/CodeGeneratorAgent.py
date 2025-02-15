from agency_swarm.agents import Agent


class CodeGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CodeGeneratorAgent",
            description="The CodeGeneratorAgent is responsible for transforming transcribed text into code using GPT-4o and passing it to the CodeDebuggerAgent for debugging.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def process_message(self, message):
        prompt = (
            "Generate Python code based on the following description.\n\n"
            f"Description: {message}\n\n"
            "Provide the complete, runnable code with proper comments where necessary."
        )
        response = self.get_completion(prompt)
        return response

