import requests
import json

from ai.providers.base import LLMProvider
from ai.providers.types import LLMResponse, ToolCall


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"


class OllamaProvider(LLMProvider):

    def generate(self, prompt: str) -> str:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    def generate_with_tools(self, contents, tools) -> LLMResponse:

        # Convert our unified tool schema
        # to Ollama's expected tool format.
        ollama_tools = [
            {
                "type": "function",
                "function": tool,
            }
            for tool in tools
        ]

        #print(json.dumps(ollama_tools, indent=2, ensure_ascii=False))

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": contents,
                "tools": ollama_tools,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()
        message = data["message"]

        tool_calls = []

        for tool_call in message.get("tool_calls", []):
            function = tool_call["function"]

            arguments = function.get("arguments", {})

            # Normalize tool arguments returned by the model.
            if arguments is None or arguments == "":
                arguments = {}
            elif isinstance(arguments, str):
                arguments = arguments.strip()

                if not arguments:
                    arguments = {}
                else:
                    arguments = json.loads(arguments)

            if not isinstance(arguments, dict):
                raise ValueError(
                    f"Invalid arguments for tool '{function['name']}': "
                    f"{arguments!r}"
                )

            tool_calls.append(
                ToolCall(
                    name=function["name"],
                    arguments=arguments,
                    id=tool_call.get("id"),
                )
            )

        return LLMResponse(
            text=message.get("content") or None,
            tool_calls=tool_calls,
            raw_message=message,
        )