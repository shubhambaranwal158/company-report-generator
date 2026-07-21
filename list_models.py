import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API Key Found:", api_key is not None)

if api_key:
    print("First 10 chars:", api_key[:10])

client = genai.Client(api_key=api_key)

print("\nListing models...\n")

try:
    models = client.models.list()

    for model in models:
        print(model.name)

except Exception as e:
    print("\nERROR:")
    print(e)