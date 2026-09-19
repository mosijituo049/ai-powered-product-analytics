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

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    for case in TEST_CASES:

        separator = "=" * 70

        print(f"\n{separator}")
        print(f"TEST CASE {case['id']}: {case['name']}")
        print(separator)

        print(f"\nQuestion:\n{case['question']}")

        file.write(f"\n{separator}\n")
        file.write(f"TEST CASE {case['id']}: {case['name']}\n")
        file.write(f"{separator}\n")
        file.write(f"\nQuestion:\n{case['question']}\n")

        try:
            response, tool_results = run_agent(
                question=case["question"],
                tools=tools,
            )

            print("\nFinal response:")
            print(response.text)

            file.write("\nFinal response:\n")
            file.write(response.text or "")
            file.write("\n")

        except Exception as error:

            print("\nERROR:")
            print(error)

            file.write("\nERROR:\n")
            file.write(str(error))
            file.write("\n")


print(f"\nTest results saved to: {OUTPUT_FILE}")