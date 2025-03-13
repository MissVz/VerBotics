README.md
md
Copy
Edit
# 🎤 Sphero Speech Command App 🚀  

A voice-controlled interface that **converts spoken commands into real-time movements for a Sphero Mini** using **speech-to-text, GPT-based command parsing, and Bluetooth communication**.  

## 🎯 Features  

✅ **Voice Control:** Speak commands like "Move forward for two seconds."  
✅ **AI-Powered Processing:** Converts speech into structured JSON commands.  
✅ **Real-Time Execution:** Sends commands to a Sphero Mini via Bluetooth.  
✅ **Modern UI:** A sleek, futuristic interface for interaction.  

## 🛠 Installation  

### 1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/YOUR-USERNAME/Sphero-Speech-Command.git
cd Sphero-Speech-Command
2️⃣ Set Up a Virtual Environment
sh
Copy
Edit
python -m venv spherov2_env
source spherov2_env/bin/activate  # macOS/Linux
spherov2_env\Scripts\activate     # Windows
3️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up OpenAI API Key
Create a .env file in the root directory and add:

ini
Copy
Edit
OPENAI_API_KEY=your-api-key-here
5️⃣ Run the Flask App
sh
Copy
Edit
python voice/app.py
Then open http://127.0.0.1:5000 in your browser.

🎮 Usage
1️⃣ Press "Record" and speak a command like:

"Move forward for three seconds."
"Turn right at 90 degrees."
2️⃣ Press "Stop" and wait for processing.

3️⃣ See the Transcribed Text & Generated Command.

4️⃣ Sphero Mini Executes the Movement! 🎯

🛠 Tech Stack
🔹 Python – Flask, OpenAI API, PyAudio
🔹 JavaScript – MediaRecorder API
🔹 CSS & HTML – Responsive UI Design
🔹 spherov2 – Sphero BLE Communication

🤝 Contributing
Want to improve the project? Follow these steps:

1️⃣ Fork the repo
2️⃣ Create a new branch: git checkout -b feature-name
3️⃣ Make your changes & commit: git commit -m "Add feature"
4️⃣ Push to your branch: git push origin feature-name
5️⃣ Open a Pull Request

🐞 Troubleshooting
Sphero Not Moving? Ensure it's powered on, in range, and unpaired from mobile apps.
Microphone Access Denied? Allow mic permissions in your browser.
OpenAI API Issues? Verify your API key in .env.
UI Not Loading Properly? Hard refresh (Ctrl + Shift + R).
📜 License
This project is licensed under the MIT License – feel free to use, modify, and contribute!