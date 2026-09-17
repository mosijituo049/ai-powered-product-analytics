from google import genai
from google.genai import types
#from typing import Any
from ai.prompts import SYSTEM_PROMPT

from ai.config import GEMINI_API_KEY
from ai.tools.definitions import TOOLS


client = genai.Client(api_key=GEMINI_API_KEY)


def ask_with_tools(contents):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "tools": TOOLS,
            "automatic_function_calling": {
                "disable": True,
            },
        },
    )

    print("Response received")
    print(response)

    return response

def extract_function_calls(response):
    """
    Extract all function calls from a Gemini response.
    """
    function_calls = []

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.function_call is not None:
                function_calls.append(part.function_call)

    return function_calls

def run_manual_tool_call(
    question: str,
    max_iterations: int = 3,
):
    """
    Run the manual tool-calling loop with a maximum
    number of iterations.
    """
    from ai.tool_executor import execute_tool

    iteration = 0
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )
    ]

    while iteration < max_iterations:
        iteration += 1

        response = ask_with_tools(contents)

        if response.candidates and response.candidates[0].content is not None:
            contents.append(response.candidates[0].content)

        function_calls = extract_function_calls(response)

        if not function_calls:
            return {
                "type": "final_answer",
                "content": response.text,
            }

        for function_call in function_calls:
            tool_name = function_call.name

            if tool_name is None:
                raise ValueError("Function call does not contain a tool name.")

            tool_args = function_call.args or {}

            tool_result = execute_tool(
                tool_name,
                tool_args,
            )

            print("Tool executed:", tool_name)

            function_response = types.Part.from_function_response(
                name=tool_name,
                response=tool_result if isinstance(tool_result, dict) else {"result": tool_result},
            )

            contents.append(
                types.Content(
                    role="tool",
                    parts=[function_response],
                )
            )

    raise RuntimeError("Maximum tool-calling iterations reached.")
