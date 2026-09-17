from google import genai

from ai.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    if response.text is None:
        raise ValueError("Gemini returned an empty response.")

    return response.text