from ai.tools.definitions import TOOLS


def get_tool_by_name(name: str):
    """
    Find a registered Python tool by its function name.
    """
    for tool in TOOLS:
        if tool.__name__ == name:
            return tool

    raise ValueError(f"Unknown tool: {name}")

def execute_tool(name: str, args: dict):
    """
    Execute a registered tool with the arguments provided by the model.
    """
    tool = get_tool_by_name(name)

    return tool(**args)