import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define audio file path
audio_file_path = "test_audio.mp3"  # Change this to your actual file

# Step 1: Convert Speech to Text using Whisper
with open(audio_file_path, "rb") as audio_file:
    client = openai.OpenAI(api_key=api_key)
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

spoken_text = transcript.text
print(f"Transcribed Text: {spoken_text}")

# Step 2: Process Command with GPT-4
prompt = f"Convert the following command into structured JSON for a robot:\n'{spoken_text}'"

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Use GPT-4o-mini or adjust based on your plan
    messages=[{"role": "user", "content": prompt}]
)

structured_command = response.choices[0].message.content
print("Generated Command:", structured_command)

# Step 3: Prepare Command for Sphero API (Placeholder)
# Here, you can format the command to match Sphero API V2 requirements
# Example: Convert structured_command into a format suitable for Sphero

print("Ready to send to Sphero:", structured_command)
