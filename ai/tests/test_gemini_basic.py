from google import genai

from ai.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say hello in one sentence.",
)

print(response.text)