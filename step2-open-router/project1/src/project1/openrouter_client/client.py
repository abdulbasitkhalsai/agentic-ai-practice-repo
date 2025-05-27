import os
import nest_asyncio
import requests
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

nest_asyncio.apply()

# Constants
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/devstral-small"

def chat_with_openrouter(prompt: str) -> str:
    response = requests.post(
        url=f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        })
    )

    if response.status_code != 200:
        print("Error Response:", response.status_code, response.text)
        return "Error: Failed to get a response from OpenRouter."

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        print("Invalid response format:", response.json())
        return "Error: Unexpected response format."
