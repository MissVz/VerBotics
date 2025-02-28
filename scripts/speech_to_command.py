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

def validate_command(command):
    """Ensures angle, speed, and duration values stay within Sphero Mini's valid range."""

    # Extract parameters safely
    angle = command["parameters"].get("angle", 0)
    speed = command["parameters"].get("speed", 100)
    duration = command["parameters"].get("duration", 2)

    # 🛑 Ensure angle is between 0-360
    if angle < 0 or angle >= 360:
        print(f"⚠️ Invalid angle {angle}, resetting to 0°.")
        angle = 0  # Default to forward

    # 🛑 Ensure speed is within -150 to 150
    if speed < -150:
        print(f"⚠️ Speed {speed} too low, setting to -150.")
        speed = -150
    elif speed > 150:
        print(f"⚠️ Speed {speed} too high, setting to 150.")
        speed = 150

    # 🛑 Ensure duration is between 1 and 10 seconds
    if duration < 1:
        print(f"⚠️ Duration {duration} too short, setting to 1s.")
        duration = 1
    elif duration > 10:
        print(f"⚠️ Duration {duration} too long, setting to 10s.")
        duration = 10

    # Update command with validated values
    command["parameters"]["angle"] = angle
    command["parameters"]["speed"] = speed
    command["parameters"]["duration"] = duration

    return command


def process_command(spoken_text):
    """ Converts spoken command into structured JSON using GPT-4o. """
    prompt = f"""
    Convert the following command into valid JSON **only**. Do not include any explanations, text, or markdown formatting.

    - If "quickly", "fast", "rapidly" appear, set speed **between 100-150**.
    - If "slowly", "gently", "cautiously", appear, set speed **between 50-100**.
    - If "reverse", "backward", "back up" appear:
      - If no direction (e.g., "Move backward"), set speed to **negative (-50 to -150)**.
      - If direction included (e.g., "Move backward left"), adjust **angle (e.g., 135° for back-left, 225° for back-right)** and keep speed **positive**.
    - Ensure **angle is between 0-360** and **speed is between -150 and 150**.
    - Ensure **duration is between 1 and 10 seconds**.

    Output format:
    {{
        "command": "move",
        "parameters": {{
            "angle": 0,   # Integer (0-360 degrees)
            "speed": 100,  # Integer (-150 to 150)
            "duration": 2  # Duration in seconds
        }}
    }}

    Command: '{spoken_text}'
    """

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
        validated_command = validate_command(structured_command)  # Validate values

        with open(command_file, "w") as file:
            json.dump(validated_command, file, indent=4)
        
        print(f"✅ Command validated and saved: {validated_command}")

    except json.JSONDecodeError:
        print("❌ Error: GPT-4o-mini did not return valid JSON.")
        print(f"Raw Response:\n{structured_command_str}")
