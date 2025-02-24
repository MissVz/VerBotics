@echo off
echo Activating virtual environment...
call .venv\Scripts\activate

echo Running Speech-to-Text processing...
python .scripts\speech_to_command.py

echo Sending command to Sphero...
node .js\sphero_control.js

echo Process complete. Exiting.
pause
