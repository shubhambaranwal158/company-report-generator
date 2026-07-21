import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_framework(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated response.
    """

    try:

        print("=" * 80)
        print("Calling Gemini...")
        print("Model: gemini-3.5-flash")
        print()
        print(prompt[:500])      # first 500 characters
        print("=" * 80)

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        print("\nGemini Response Received\n")

        print("Response Length:", len(response.text))

        print(response)

        return response.text

    except Exception as e:

        print("\nFULL ERROR:")
        print(e)

        return f"❌ Gemini Error:\n\n{str(e)}"