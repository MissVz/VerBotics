import openai
import os
import pyaudio
import wave
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper works best with 16kHz
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust for desired recording length
AUDIO_FILE = "recorded_audio.wav"

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
    prompt = f"Convert the following command into structured JSON for a robot:\n'{spoken_text}'"

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

    structured_command = process_command(spoken_text)
    print("Generated Command:", structured_command)

    # Step 3: Send structured command to Sphero API (To be implemented)
    print("Ready to send to Sphero:", structured_command)