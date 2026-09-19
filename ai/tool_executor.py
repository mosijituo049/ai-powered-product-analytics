import inspect

from ai.tools.definitions import TOOLS


def get_tool_by_name(name: str):
    for tool in TOOLS:
        if tool.__name__ == name:
            return tool

    raise ValueError(f"Unknown tool: {name}")


def validate_arguments(tool, args: dict) -> dict:
    signature = inspect.signature(tool)

    valid_parameters = set(signature.parameters.keys())

    # 1. Check for unexpected arguments
    unexpected_arguments = set(args.keys()) - valid_parameters

    if unexpected_arguments:
        raise ValueError(
            f"Invalid arguments for tool '{tool.__name__}'. "
            f"Unexpected arguments: {sorted(unexpected_arguments)}. "
            f"Expected parameters: {sorted(valid_parameters)}."
        )

    # 2. Check required arguments
    for parameter_name, parameter in signature.parameters.items():
        if (
            parameter.default is inspect.Parameter.empty
            and parameter_name not in args
        ):
            raise ValueError(
                f"Invalid arguments for tool '{tool.__name__}'. "
                f"Missing required argument: '{parameter_name}'."
            )

    # 3. Normalize argument types
    normalized_args = {}

    for parameter_name, value in args.items():
        parameter = signature.parameters[parameter_name]
        expected_type = parameter.annotation

        if expected_type is inspect.Parameter.empty:
            normalized_args[parameter_name] = value
            continue

        try:
            if expected_type is int and isinstance(value, str):
                normalized_args[parameter_name] = int(value)

            elif expected_type is float and isinstance(value, str):
                normalized_args[parameter_name] = float(value)

            elif expected_type is bool and isinstance(value, str):
                normalized_args[parameter_name] = value.lower() == "true"

            else:
                normalized_args[parameter_name] = value

        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid type for argument '{parameter_name}' "
                f"in tool '{tool.__name__}'. "
                f"Expected {expected_type.__name__}, "
                f"got {type(value).__name__}."
            )

    return normalized_args


def execute_tool(name: str, args: dict):
    tool = get_tool_by_name(name)

    validated_args = validate_arguments(tool, args)

    return tool(**validated_args)