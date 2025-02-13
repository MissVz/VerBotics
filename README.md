# **VerBotics Project - README**

## **Project Overview**

The VerBotics project integrates **OpenAI’s Whisper (Speech-to-Text)** and **GPT-4o-mini (Natural Language Processing)** with the **Sphero Mini robot** to enable **voice-controlled robotic navigation**. The system converts **spoken commands** into **structured movement instructions** and executes them on the **Sphero Mini** using **Sphero API V2**.

⚠️ **IMPORTANT:** All users must create their own OpenAI account at [Platform.OpenAI.com](https://platform.openai.com), generate their own **Project API Key**, and set it in their `.env` file as `OPENAI_API_KEY`. API calls to OpenAI’s Whisper and GPT-4o-mini will **consume credits and charge the linked OpenAI account**, so each user must ensure they are using their own API key to avoid billing issues.

---

## **Current Progress**

### **1️⃣ Speech-to-Text Processing (Whisper)** ✅ **Complete**

- Implemented **`test_whisper_stt.py`** to transcribe voice commands using OpenAI’s Whisper API.
- Verified transcription accuracy with **`test_audio.m4a`**.

### **2️⃣ Command Interpretation (GPT-4o-mini)** ✅ **Complete**

- **`speech_to_command.py`** processes Whisper’s output and converts it into structured JSON commands using GPT-4o-mini.
- Ensures output matches Sphero’s required format:
  ```json
  {"direction": 0, "speed": 100, "duration": 2}
  ```
- Saves the command to **`sphero_command.json`** for execution.

### **3️⃣ Sphero API Integration** ✅ **Complete**

- **`sphero_control.js`** reads commands from `sphero_command.json` and executes them using `spherov2.js`.
- Successfully tested basic movement commands on **Sphero Mini**.

### **4️⃣ Automated Execution Pipeline** ✅ **Complete**

- Created batch/script files (`run_verbotics.bat` for Windows, `run_verbotics.sh` for Linux/macOS) to:
  1. Convert voice input → text (Whisper)
  2. Process text → command (GPT-4o-mini)
  3. Send command → Sphero execution (Sphero API V2)

---

## **Next Steps**

### **1️⃣ Improve Command Processing Accuracy** 🔄 **In Progress**

- Fine-tune GPT-4o-mini prompt to ensure **speed, duration, and direction values** match Sphero API constraints.
- Handle ambiguous commands (e.g., “Turn slightly left” → Convert to an exact degree value).

### **2️⃣ Implement Real-Time Execution** ⏳ **Planned**

- Currently, commands are saved in `sphero_command.json` and executed separately.
- **Goal:** Eliminate manual script execution by directly sending **live GPT-4o-mini commands to Sphero API**.
- Possible approach: Use **WebSockets or a FastAPI backend** to process commands in real time.

### **3️⃣ Expand Movement Capabilities** 🔄 **Planned**

- Add support for:
  - **Complex movement sequences** (e.g., “Move in a square pattern”).
  - **Stopping and reversing** commands.
  - **Conditional commands** (e.g., “Move forward unless there’s an obstacle”).

### **4️⃣ Test Edge Computing Deployment** 🚀 **Future Work**

- Investigate **running GPT-4o-mini inference locally** to reduce API dependency.
- Explore **edge-based NLP models** (e.g., quantized LLaMA) for on-device command processing.

---

## **How to Run the Current System**

### **Windows:**

1. Activate the virtual environment:
   ```powershell
   .venv\Scripts\Activate
   ```
2. Install required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the automated script:
   ```powershell
   ./run_verbotics.bat
   ```

### **Linux/macOS:**

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the automated script:
   ```bash
   ./run_verbotics.sh
   ```

---

## **Updated ********************`run_verbotics.bat`******************** Script**

```bat
@echo off

echo Activating virtual environment...
call .venv\Scripts\activate

:: Ensure dependencies are installed
echo Installing required Python dependencies...
pip install -r requirements.txt

:: Run Speech-to-Text processing
echo Running Speech-to-Text processing...
python speech_to_command.py

:: Execute movement command with Sphero
echo Sending command to Sphero...
node sphero_control.js

echo Process complete. Exiting.
pause
```

---

## **Final Notes**

- Ensure the **Sphero Mini is charged and connected** before running `sphero_control.js`.
- If issues arise, check **error logs in `speech_to_command.py` and `sphero_control.js`**.

OpenAI. (2024). _Assistance with README documentation for VerBotics project._ ChatGPT (Version 4o) [Large language model]. https://platform.openai.com/
