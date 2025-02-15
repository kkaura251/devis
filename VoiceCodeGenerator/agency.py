from agency_swarm import Agency, set_openai_key
from CodeDebuggerAgent.CodeDebuggerAgent import CodeDebuggerAgent
from CodeGeneratorAgent.CodeGeneratorAgent import CodeGeneratorAgent
from VoiceInputAgent.VoiceInputAgent import VoiceInputAgent
from VoiceCodeCEO.VoiceCodeCEO import VoiceCodeCEO
import os
from dotenv import load_dotenv
import gradio as gr

# Load environment variables and set API key
load_dotenv()
set_openai_key(os.getenv('OPENAI_API_KEY'))

# Initialize agents
ceo = VoiceCodeCEO()
voice_input = VoiceInputAgent()
code_generator = CodeGeneratorAgent()
code_debugger = CodeDebuggerAgent()

# Create agency
agency = Agency(
    [ceo, [ceo, voice_input],
     [voice_input, code_generator],
     [ceo, code_debugger],
     ],
    shared_instructions='./agency_manifesto.md',
    max_prompt_tokens=25000,
    temperature=0.3,
)

if __name__ == '__main__':
    with gr.Blocks() as interface:
        gr.Markdown("# Voice Code Generator")
        with gr.Row():
            # Voice input section
            with gr.Column(scale=1):
                audio_recorder, transcription = voice_input.create_gradio_interface()
                send_button = gr.Button("Send to Agents")
            
            # Agency chat section
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="Agent Conversation",
                    height=500
                )
                
                def send_to_agents(text, history):
                    if not text:
                        return history
                    
                    # Send the transcribed text to the agency and get response
                    response = agency.get_completion(text)
                    
                    # Update chat history
                    history = history or []
                    history.append((text, response))
                    return history
                
                # Connect send button to chatbot
                send_button.click(
                    fn=send_to_agents,
                    inputs=[transcription, chatbot],
                    outputs=[chatbot]
                )
    
    interface.launch(share=True)