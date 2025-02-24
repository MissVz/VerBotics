import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Get the absolute path to the assets folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")  # Move up one level, then into "assets"
AUDIO_FILE_PATH = os.path.join(ASSETS_DIR, "test_audio.m4a")

# Debugging output
print(f"Using audio file path: {AUDIO_FILE_PATH}")

# Open and transcribe the file
try:
    with open(AUDIO_FILE_PATH, "rb") as audio_file:
        client = openai.OpenAI(api_key=api_key)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    print("Transcription:", transcript.text)

except FileNotFoundError:
    print(f"Error: File not found at {AUDIO_FILE_PATH}. Check the path and try again.")