from ai.tool_executor import execute_tool


tool_calls = [
    ("get_funnel_metrics", {}),
    ("get_checkout_abandonment", {}),
]


tool_results = []

for tool_name, tool_args in tool_calls:
    result = execute_tool(tool_name, tool_args)

    tool_results.append(
        (tool_name, result)
    )


for tool_name, result in tool_results:
    print("\nTool:", tool_name)
    print("Result:")
    print(result)