import os

from ai.providers.gemini import GeminiProvider
from ai.providers.ollama import OllamaProvider


def get_llm_provider():
    provider_name = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider_name == "gemini":
        return GeminiProvider()

    if provider_name == "ollama":
        return OllamaProvider()

    raise ValueError(
        f"Unsupported LLM provider: {provider_name}"
    )