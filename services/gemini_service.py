import os

from dotenv import load_dotenv
from google import genai
from google.genai.types import (GenerateContentConfig, Tool, GoogleSearch)

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
        print("Model: gemini-3.6-flash")
        print()
        print(prompt[:500])      # first 500 characters
        print("=" * 80)

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                max_output_tokens=65535,
                response_mime_type="text/plain",
#                tools=[
#                    Tool(
#                        google_search=GoogleSearch()
#                    )
#                ]
            )
        )

        print("\nGemini Response Received\n")

        candidate = response.candidates[0]

        finish_reason = getattr(candidate, "finish_reason", None)

        if finish_reason:
            print("Finish Reason:", finish_reason)

            if str(finish_reason).endswith("MAX_TOKENS"):
                print("⚠ WARNING: Response was truncated due to max_output_tokens.")

        print("Response Length:", len(response.text))

        print("=" * 80)
        print("Response Preview:")
        print(response.text[:1000])
        print("=" * 80)

        return response.text

    except Exception as e:

        print("\nFULL ERROR:")
        print(e)

        return f"❌ Gemini Error:\n\n{str(e)}"