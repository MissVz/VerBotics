from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Retrieve API Key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API Key loaded successfully!")
else:
    print("Error: API Key not found.")