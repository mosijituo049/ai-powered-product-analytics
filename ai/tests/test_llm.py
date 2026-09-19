from ai.llm import get_llm_provider


provider = get_llm_provider()

print("Provider:", provider.__class__.__name__)

answer = provider.generate(
    "What is product analytics? Answer in 2 sentences."
)

print(answer)