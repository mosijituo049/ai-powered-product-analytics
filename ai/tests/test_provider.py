from ai.providers.ollama import OllamaProvider


provider = OllamaProvider()

answer = provider.generate(
    "What is product analytics? Answer in 2 sentences."
)

print(answer)