from unittest.mock import patch

from google.genai import types

from ai.tool_calling import run_manual_tool_call
from ai.tool_executor import execute_tool


class FakeGemini:
    def __init__(self):
        self.call_count = 0

    def __call__(self, contents):
        self.call_count += 1

        print(f"\n--- Fake Gemini call {self.call_count} ---")

        if self.call_count == 1:
            print("Gemini decides to call:")
            print("get_checkout_abandonment")

            return types.GenerateContentResponse(
                candidates=[
                    types.Candidate(
                        content=types.Content(
                            role="model",
                            parts=[
                                types.Part.from_function_call(
                                    name="get_checkout_abandonment",
                                    args={},
                                )
                            ],
                        )
                    )
                ]
            )

        if self.call_count == 2:
            print("Gemini received the first tool result.")
            print("Gemini decides to call:")
            print("get_funnel_metrics")

            return types.GenerateContentResponse(
                candidates=[
                    types.Candidate(
                        content=types.Content(
                            role="model",
                            parts=[
                                types.Part.from_function_call(
                                    name="get_funnel_metrics",
                                    args={},
                                )
                            ],
                        )
                    )
                ]
            )

        print("Gemini received tool result.")
        print("Gemini returns final answer.")

        return types.GenerateContentResponse(
            candidates=[
                types.Candidate(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text="The checkout abandonment rate is 56.33%."
                            )
                        ],
                    )
                )
            ]
        )


fake_gemini = FakeGemini()


with patch(
    "ai.tool_calling.ask_with_tools",
    side_effect=fake_gemini,
):
    result = run_manual_tool_call(
        "What's the capital of France?"
    )


print("\nFinal result:")
print(result)