import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")
print("API KEY:", api_key)

if not api_key:
    raise ValueError("⚠️ Missing GROQ_API_KEY environment variable.")

# Configure Groq client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def get_response(messages, model="llama-3.3-70b-versatile"):
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )
        return resp.choices[0].message.content

    except Exception as e:
        return f"⚠️ API Error: {e}"