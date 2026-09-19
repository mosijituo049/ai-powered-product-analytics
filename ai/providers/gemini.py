from google import genai
from google.genai import types
import os

from ai.config import GEMINI_API_KEY
from ai.providers.base import LLMProvider
from ai.providers.types import LLMResponse, ToolCall


#MODEL_NAME = "gemini-3.6-flash"
MODEL_NAME = "gemini-3.5-flash-lite"

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "gemini-embedding-001",
)

def clean_gemini_schema(schema: dict) -> dict:
    schema = dict(schema)
    schema.pop("additionalProperties", None)
    return schema

class GeminiProvider(LLMProvider):

    embedding_model_name = EMBEDDING_MODEL

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        if response.text is None:
            raise ValueError("Gemini returned an empty response.")

        return response.text

    def generate_with_tools(self, contents, tools) -> LLMResponse:

        # Convert our unified tool schema
        # to Gemini's FunctionDeclaration format.
        function_declarations = []

        for tool in tools:
            function_declarations.append(
                types.FunctionDeclaration(
                    name=tool["name"],
                    description=tool["description"],
                    parameters=types.Schema.model_validate(
                        clean_gemini_schema(tool["parameters"])
                    ),
                )
            )

        gemini_tools = [
            types.Tool(
                function_declarations=function_declarations
            )
        ]

        # Convert our unified messages
        # to Gemini's Content format.
        gemini_contents = []
        system_instruction = None

        for message in contents:

            role = message["role"]

            if role == "system":
                system_instruction = message["content"]

            elif role == "user":
                gemini_contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=message["content"]
                            )
                        ],
                    )
                )

            elif role == "assistant":

                # If this is a previous Gemini response,
                # reuse the original Content object.
                raw_message = message.get("raw_message")

                if raw_message is not None:
                    gemini_contents.append(raw_message)

                elif message.get("content"):
                    gemini_contents.append(
                        types.Content(
                            role="model",
                            parts=[
                                types.Part.from_text(
                                    text=message["content"]
                                )
                            ],
                        )
                    )

            elif role == "tool":

                tool_name = message.get("name")

                if not tool_name:
                    raise ValueError(
                        "Tool message is missing tool name."
                    )

                tool_result = message.get("content")

                gemini_contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=tool_name,
                                response={
                                    "result": tool_result
                                },
                            )
                        ],
                    )
                )

        config = types.GenerateContentConfig(
            tools=gemini_tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        )

        if system_instruction:
            config.system_instruction = system_instruction

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=gemini_contents,
            config=config,
        )

        tool_calls = []

        candidates = response.candidates or []

        for candidate in candidates:

            if candidate.content is None:
                continue

            parts = candidate.content.parts or []

            for part in parts:

                if part.function_call is None:
                    continue

                function_call = part.function_call

                if function_call.name is None:
                    continue

                tool_calls.append(
                    ToolCall(
                        name=function_call.name,
                        arguments=dict(
                            function_call.args or {}
                        ),
                    )
                )

        # Save the model response in our own
        # provider-independent format.
        raw_message = None

        if candidates:
            raw_message = candidates[0].content

        return LLMResponse(
            text=response.text or None,
            tool_calls=tool_calls,
            raw_message=raw_message,
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []

        for text in texts:
            response = self.client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=text)
                    ],
                ),
            )

            if not response.embeddings:
                raise ValueError(
                    "Gemini returned no embedding."
                )

            values = response.embeddings[0].values

            if values is None:
                raise ValueError(
                    "Gemini returned an embedding without values."
                )

            embeddings.append(list(values))

        return embeddings