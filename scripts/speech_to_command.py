import json
import openai
import os
import pyaudio
import re
import wave
from dotenv import load_dotenv

# Define the assets directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")  # Move up one level, then into "assets"
COMMAND_FILE = os.path.join(ASSETS_DIR, "sphero_command.json")  # Save JSON in assets folder

# Ensure the assets directory exists
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)  # Create the folder if it doesn't exist

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper works best with 16kHz
CHUNK = 1024
RECORD_SECONDS = 8  # Adjust for desired recording length

# Define the path to the assets folder (relative to the scripts directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the current script's directory
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")  # Moves up one level and into "assets"
AUDIO_FILE = os.path.join(ASSETS_DIR, "recorded_audio.wav")  # Defines the full path

# Ensure the assets directory exists
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)  # Creates the folder if it doesn't exist

print(f"Recording will be saved to: {AUDIO_FILE}")

def record_audio():
    """ Records audio from the microphone and saves it as a WAV file. """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("Recording... Speak now!")
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(AUDIO_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

def transcribe_audio():
    """ Transcribes recorded audio using OpenAI Whisper. """
    with open(AUDIO_FILE, "rb") as audio_file:
        client = openai.OpenAI(api_key=api_key)
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    return response.text

def process_command(spoken_text):
    """ Converts spoken command into structured JSON using GPT-4o. """
    # prompt = f"Convert the following command into structured JSON for a robot:\n'{spoken_text}'"
    prompt = f"""
    Convert the following command into valid JSON **only**. Do not include any explanations, text, or markdown formatting.
    Output format must strictly follow:

    {{
    "command": "move",
    "parameters": {{
        "angle": 0,   # Integer (0-360 degrees)
        "speed": 100,  # Integer (0-999999)
        "duration": 2  # Duration in seconds
    }}
    }}

    Ensure there is **no additional text, no markdown, and no explanations.** 

    Command: '{spoken_text}'
    """

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use GPT-4o-mini or adjust based on your plan
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    record_audio()
    spoken_text = transcribe_audio()
    print(f"Transcribed Text: {spoken_text}")

    structured_command_str = process_command(spoken_text)
    print("Generated Command:", structured_command_str)

    # Remove Markdown formatting if present
    structured_command_cleaned = re.sub(r"```json|```", "", structured_command_str).strip()

    # Save structured command to a JSON file
    command_file = COMMAND_FILE  # Use the correct path
    try:
        structured_command = json.loads(structured_command_cleaned)  # Ensure valid JSON
        with open(command_file, "w") as file:
            json.dump(structured_command, file, indent=4)
        print(f"Command saved to {command_file}, ready for execution.")
    except json.JSONDecodeError:
        print("Error: GPT-4o-mini did not return valid JSON.")
        print(f"Raw Response:\n{structured_command_str}")