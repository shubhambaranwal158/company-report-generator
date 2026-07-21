import os
import traceback

from dotenv import load_dotenv
from google import genai

print("Step 1")

load_dotenv()

print("Step 2")

api_key = os.getenv("GEMINI_API_KEY")
print("API key loaded:", api_key[:10])

client = genai.Client(api_key=api_key)

print("Step 3")

try:
    print("Calling Gemini...")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Say hello in one sentence."
    )

    print("Step 4")
    print(type(response))
    print(response)
    print("TEXT:")
    print(response.text)

except Exception:
    print("\nEXCEPTION OCCURRED\n")
    traceback.print_exc()