from ai.tool_executor import execute_tool


tool_calls = [
    {
        "name": "get_funnel_metrics",
        "args": {},
    },
    {
        "name": "get_checkout_abandonment",
        "args": {},
    },
]


tool_results = []

for tool_call in tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    result = execute_tool(
        tool_name,
        tool_args,
    )

    tool_results.append(
        (tool_name, result)
    )


print("\nNumber of tool results:", len(tool_results))

for tool_name, result in tool_results:
    print("\nTool:", tool_name)
    print("Result:")
    print(result)