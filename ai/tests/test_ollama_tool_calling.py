from ai.providers.ollama import OllamaProvider


provider = OllamaProvider()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_checkout_abandonment",
            "description": "Return checkout abandonment KPIs from the GA4 dataset.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "What is the checkout abandonment rate?",
    }
]

response = provider.generate_with_tools(
    messages,
    tools,
)

print(response)