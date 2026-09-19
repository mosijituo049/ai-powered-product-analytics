import os

from dotenv import load_dotenv


load_dotenv()


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if LLM_PROVIDER == "gemini" and not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set in the environment."
    )