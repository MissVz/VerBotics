import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Test API request using available model
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Use "gpt-4o-mini" instead of "gpt-4"
    messages=[{"role": "user", "content": "Hello, can you confirm my OpenAI setup is working?"}]
)

# Print response
print("GPT-4o-mini Response:", response.choices[0].message.content)
