from ai.llm import get_llm_provider
from ai.providers.types import LLMResponse
from ai.tool_executor import execute_tool
from ai.prompts import SYSTEM_PROMPT


def run_agent(
    question: str,
    tools,
    max_iterations: int = 3,
):
    """
    Run the agent loop using the configured LLM provider.
    """
    provider = get_llm_provider()

    contents = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    # Store tool results so Streamlit can use structured data
    tool_results = []

    for iteration in range(max_iterations):
        print(f"\n--- Agent iteration {iteration + 1} ---")

        response: LLMResponse = provider.generate_with_tools(
            contents,
            tools,
        )

        # No tool call -> final answer
        if not response.tool_calls:
            return response, tool_results

        # Keep assistant's original tool-call message.
        if response.raw_message is not None:
            contents.append(
                {
                    "role": "assistant",
                    "raw_message": response.raw_message,
                }
            )

        for tool_call in response.tool_calls:
            print(
                "Tool requested:",
                tool_call.name,
                tool_call.arguments,
            )

            try:
                tool_result = execute_tool(
                    tool_call.name,
                    tool_call.arguments,
                )

                print("Tool executed successfully.")

                tool_results.append(
                    {
                        "tool_name": tool_call.name,
                        "result": tool_result,
                    }
                )

            except Exception as error:
                print(
                    "Tool execution failed:",
                    error,
                )

                return (LLMResponse(
                    text=(
                        "I could not retrieve the required analytics data "
                        "because the data tool failed. "
                        f"Tool error: {error}"
                    )
                    ),
                    tool_results,
                )

            contents.append(
                {
                    "role": "tool",
                    "name": tool_call.name,
                    "content": str(tool_result),
                }
            )

    raise RuntimeError("Maximum agent iterations reached.")