import json
from pathlib import Path
from ai.config import LLM_PROVIDER
from datetime import datetime

from ai.tool_calling import run_agent
from ai.tools.schemas import TOOL_SCHEMAS


tools = list(TOOL_SCHEMAS.values())


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]


# Load evaluation cases
EVAL_CASES_FILE = (
    PROJECT_ROOT
    / "ai"
    / "tests"
    / "eval"
    / "eval_cases.json"
)

with open(EVAL_CASES_FILE, "r", encoding="utf-8") as file:
    TEST_CASES = json.load(file)


# Output file
OUTPUT_DIR = PROJECT_ROOT / "outputs/agent_tests"
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_FILE = (
    OUTPUT_DIR
    / f"{LLM_PROVIDER}_{timestamp}.txt"
)


def evaluate_tools(case, tool_results):

    actual_tools = [
        result["tool_name"]
        for result in tool_results
    ]

    expected_tools = case.get("expected_tools", [])

    missing_tools = [
        tool
        for tool in expected_tools
        if tool not in actual_tools
    ]

    if missing_tools:
        return False, f"Missing tools: {missing_tools}"

    return True, "All expected tools were called"


passed_cases = 0
failed_cases = 0
error_cases = 0


with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    for case in TEST_CASES:

        separator = "=" * 70

        print(f"\n{separator}")
        print(f"TEST CASE {case['id']}: {case['name']}")
        print(separator)

        print(f"\nQuestion:\n{case['question']}")

        file.write(f"\n{separator}\n")
        file.write(
            f"TEST CASE {case['id']}: {case['name']}\n"
        )
        file.write(f"{separator}\n")
        file.write(
            f"\nQuestion:\n{case['question']}\n"
        )

        try:

            response, tool_results = run_agent(
                question=case["question"],
                tools=tools,
            )

            # --------------------------------
            # Final response
            # --------------------------------

            print("\nFinal response:")
            print(response.text)

            file.write("\nFinal response:\n")
            file.write(response.text or "")
            file.write("\n")

            # --------------------------------
            # Tools called
            # --------------------------------

            actual_tools = [
                result["tool_name"]
                for result in tool_results
            ]

            print("\nTools called:")

            for tool_name in actual_tools:
                print(f"- {tool_name}")

            file.write("\nTools called:\n")

            for tool_name in actual_tools:
                file.write(f"- {tool_name}\n")

            # --------------------------------
            # Evaluation
            # --------------------------------

            passed, reason = evaluate_tools(
                case,
                tool_results,
            )

            print("\nEvaluation:")

            if passed:
                print("PASS")
                print(reason)
                passed_cases += 1
            else:
                print("FAIL")
                print(reason)
                failed_cases += 1

            file.write("\nEvaluation:\n")

            if passed:
                file.write("PASS\n")
            else:
                file.write("FAIL\n")

            file.write(f"{reason}\n")

        except Exception as error:

            error_message = str(error)

            print("\nERROR:")
            print(error_message)

            file.write("\nERROR:\n")
            file.write(error_message)
            file.write("\n")

            if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                status = "ERROR - API QUOTA"

            else:
                status = "ERROR"

            print(f"Status: {status}")

            file.write(f"Status: {status}\n")

            error_cases += 1


# --------------------------------
# Summary
# --------------------------------

total_cases = len(TEST_CASES)

print("\n" + "=" * 70)
print("EVALUATION SUMMARY")
print("=" * 70)

print(f"\nPASS: {passed_cases}")
print(f"FAIL: {failed_cases}")
print(f"ERROR: {error_cases}")
print(f"TOTAL: {total_cases}")

with open(OUTPUT_FILE, "a", encoding="utf-8") as file:

    file.write("\n" + "=" * 70 + "\n")
    file.write("EVALUATION SUMMARY\n")
    file.write("=" * 70 + "\n")

    file.write(
        f"\nResult: {passed_cases}/{total_cases} PASS\n"
    )

    file.write(f"PASS: {passed_cases}\n")
    file.write(f"FAIL: {failed_cases}\n")


print(f"\nTest results saved to: {OUTPUT_FILE}")