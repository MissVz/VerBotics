# speech_to_command.py

import json
import openai
import os
import pyaudio
import re
import wave
from dotenv import load_dotenv

# Load API key and setup assets directory
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")
AUDIO_FILE = os.path.join(ASSETS_DIR, "recorded_audio.wav")
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Audio configuration constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 8

def transcribe_audio_file(filepath: str) -> str:
    """Transcribes the audio file at 'filepath' using OpenAI Whisper."""
    with open(filepath, "rb") as audio_file:
        client = openai.OpenAI(api_key=api_key)
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

def process_spoken_text(spoken_text: str) -> dict:
    """Converts the spoken text into a structured JSON command using GPT-4o."""
    prompt = f"""
    Convert the following command into valid JSON **only**. Do not include any explanations, text, or markdown formatting.

    - If "quickly", "fast", "rapidly" appear, set speed **between 100-150**.
    - If "slowly", "gently", "cautiously" appear, set speed **between 50-100**.
    - If "reverse", "backward", "back up" appear:
      - If no direction, set speed to **negative (-50 to -150)**.
      - If direction is included, adjust the angle accordingly.
    - Ensure **angle is between 0-360**, **speed between -150 and 150**, and **duration between 1 and 10 seconds**.

    Output format:
    {{
        "command": "move",
        "parameters": {{
            "angle": 0,
            "speed": 100,
            "duration": 2
        }}
    }}

    Command: '{spoken_text}'
    """
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    # Assuming the GPT response text is valid JSON
    return json.loads(response.choices[0].message.content)

def validate_command(command: dict) -> dict:
    """Ensures the command parameters are within valid ranges for Sphero Mini."""
    angle = command["parameters"].get("angle", 0)
    speed = command["parameters"].get("speed", 100)
    duration = command["parameters"].get("duration", 2)

    if angle < 0 or angle >= 360:
        angle = 0
    if speed < -150:
        speed = -150
    elif speed > 150:
        speed = 150
    if duration < 1:
        duration = 1
    elif duration > 10:
        duration = 10

    command["parameters"]["angle"] = angle
    command["parameters"]["speed"] = speed
    command["parameters"]["duration"] = duration
    return command