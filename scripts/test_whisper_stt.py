import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Open audio file and transcribe using Whisper
audio_file_path = "test_audio.m4a"  # Change to your actual audio file name

with open(audio_file_path, "rb") as audio_file:
    client = openai.OpenAI(api_key=api_key)  # Initialize OpenAI client
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print("Transcription:", transcript.text)
