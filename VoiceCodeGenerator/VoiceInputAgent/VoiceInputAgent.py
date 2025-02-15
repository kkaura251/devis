from agency_swarm.agents import Agent
import gradio as gr
import speech_recognition as sr
import numpy as np
import soundfile as sf
import io


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
        self.recognizer = sr.Recognizer()

    def process_voice(self, audio_data):
        try:
            if audio_data is None:
                return ""
                
            # Convert numpy array to audio data
            sample_rate, audio_numpy = audio_data
            
            # Convert to mono if stereo
            if len(audio_numpy.shape) > 1:
                audio_numpy = audio_numpy.mean(axis=1)
            
            # Create an AudioData object
            byte_io = io.BytesIO()
            sf.write(byte_io, audio_numpy, sample_rate, format='wav')
            byte_io.seek(0)
            
            with sr.AudioFile(byte_io) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
                
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"
        except Exception as e:
            return f"Error processing audio: {str(e)}"

    def create_gradio_interface(self):
        with gr.Group():
            gr.Markdown("### Voice Input")
            
            # Create audio recorder with mic input
            audio_recorder = gr.Audio(
                sources=["microphone"],
                type="numpy",
                label="Voice Recording",
                interactive=True
            )
            
            # Create transcription output
            transcription = gr.Textbox(
                label="Transcribed Text",
                placeholder="Transcription will appear here...",
                interactive=True  # Make it interactive so user can edit if needed
            )

            # When audio changes, process the voice
            audio_recorder.change(
                fn=self.process_voice,
                inputs=[audio_recorder],
                outputs=[transcription]
            )

        return [audio_recorder, transcription]

    def process_message(self, message):
        # Process the transcribed message and pass it to other agents
        return f"Processing voice command: {message}"

    def get_interface(self):
        return self.create_gradio_interface()

    def response_validator(self, message):
        return message
