# app.py

import os
import time
from flask import Flask, request, jsonify, render_template
from speech_to_command import transcribe_audio_file, process_spoken_text, validate_command
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color  # In case you need to set LED colors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400

    # Save uploaded audio file
    audio_file = request.files['audio']
    file_path = os.path.join(ASSETS_DIR, 'uploaded.wav')
    audio_file.save(file_path)

    # Transcribe audio and convert spoken text to a command
    spoken_text = transcribe_audio_file(file_path)
    print(f"Transcribed Text: {spoken_text}")

    raw_command = process_spoken_text(spoken_text)
    final_command = validate_command(raw_command)

    # Leverage MiniTest.py logic: scan for the Sphero and, within a with block,
    # execute the command. This ensures we use the context manager.
    if final_command.get("command") == "move":
        # Re-scan for the Sphero Mini every time
        toy = scanner.find_Mini(timeout=5.0)
        if toy is None:
            return jsonify({"error": "No Sphero found"}), 500

        with SpheroEduAPI(toy) as sphero:
            angle = final_command["parameters"]["angle"]
            speed = final_command["parameters"]["speed"]
            duration = final_command["parameters"]["duration"]
            print(f"Rolling Sphero: angle={angle}, speed={speed}, duration={duration}")
            sphero.roll(angle, speed, duration)
            time.sleep(duration)  # Wait for the movement to complete

    return jsonify({
        "transcription": spoken_text,
        "command": final_command
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)