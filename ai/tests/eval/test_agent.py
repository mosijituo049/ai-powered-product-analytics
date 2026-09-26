import json
import re
from pathlib import Path
from ai.config import LLM_PROVIDER
from datetime import datetime

from ai.tool_calling import run_agent
from ai.tools.schemas import TOOL_SCHEMAS


tools = list(TOOL_SCHEMAS.values())


# ============================================================
# Project root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ============================================================
# Load evaluation cases
# ============================================================

EVAL_CASES_FILE = (
    PROJECT_ROOT
    / "ai"
    / "tests"
    / "eval"
    / "eval_cases.json"
)

with open(EVAL_CASES_FILE, "r", encoding="utf-8") as file:
    TEST_CASES = json.load(file)


# ============================================================
# Output file
# ============================================================

OUTPUT_DIR = PROJECT_ROOT / "outputs/agent_tests"
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_FILE = (
    OUTPUT_DIR
    / f"{LLM_PROVIDER}_{timestamp}.txt"
)


# ============================================================
# Helper functions
# ============================================================

def get_actual_tools(tool_results):
    """Return the names of tools actually called."""

    return [
        result["tool_name"]
        for result in tool_results
    ]


def response_contains(response_text, value):
    """Check whether a value appears in the final response."""

    if response_text is None:
        return False

    text = str(response_text).lower()
    value_str = str(value).lower()

    return value_str in text


def response_contains_number(response_text, value):
    """
    Check whether a numerical value appears in the response.

    Accepts:
    56.33
    56.33%
    57.2
    57.20
    """

    if not response_text:
        return False

    text = str(response_text)

    value_float = float(value)

    patterns = [
        rf"\b{value_float:.2f}\b",
        rf"\b{value_float:.1f}\b",
        rf"\b{value_float:g}\b",
    ]

    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


def check_required_tools(expected_tools, actual_tools):
    """Check that all expected tools were called."""

    missing_tools = [
        tool
        for tool in expected_tools
        if tool not in actual_tools
    ]

    if missing_tools:
        return False, f"Missing tools: {missing_tools}"

    return True, "All expected tools were called"


# ============================================================
# Case-specific evaluation
# ============================================================

def evaluate_case(case, response, tool_results):

    case_id = case["id"]

    response_text = response.text or ""

    actual_tools = get_actual_tools(tool_results)

    checks = []

    # --------------------------------------------------------
    # Case 1
    # --------------------------------------------------------

    if case_id == 1:

        passed, reason = check_required_tools(
            ["get_checkout_abandonment"],
            actual_tools,
        )

        checks.append((passed, reason))

        checks.append((
            response_contains_number(response_text, 56.33),
            "Overall abandonment rate = 56.33%"
        ))

    # --------------------------------------------------------
    # Case 2
    # --------------------------------------------------------

    elif case_id == 2:

        passed, reason = check_required_tools(
            [
                "get_abandonment_by_device",
                "get_checkout_abandonment",
            ],
            actual_tools,
        )

        checks.append((passed, reason))

        checks.append((
            response_contains(response_text, "tablet"),
            "Identifies tablet as highest abandonment device"
        ))

        checks.append((
            response_contains_number(response_text, 57.20),
            "Tablet abandonment = 57.20%"
        ))

        checks.append((
            response_contains_number(response_text, 56.33),
            "Overall abandonment = 56.33%"
        ))

    # --------------------------------------------------------
    # Case 3
    # --------------------------------------------------------

    elif case_id == 3:

        passed, reason = check_required_tools(
            ["get_abandonment_by_channel"],
            actual_tools,
        )

        checks.append((passed, reason))

        expected_values = {
            "Newsletter": 100.0,
            "Partner": 100.0,
            "Referral": 100.0,
            "YouTube": 100.0,
            "Direct": 65.95,
            "Other": 65.63,
            "Google": 52.82,
            "Unknown": 43.16,
        }

        for channel, value in expected_values.items():

            checks.append((
                response_contains(response_text, channel),
                f"Reports {channel}"
            ))

            checks.append((
                response_contains_number(response_text, value),
                f"{channel} abandonment = {value}%"
            ))

    # --------------------------------------------------------
    # Case 4
    # --------------------------------------------------------

    elif case_id == 4:

        # Definition question should not require analytics tools.
        analytics_tools = [
            "get_checkout_abandonment",
            "get_abandonment_by_device",
            "get_abandonment_by_channel",
            "get_purchase_prediction",
            "get_funnel_metrics",
        ]

        unexpected_tools = [
            tool
            for tool in actual_tools
            if tool in analytics_tools
        ]

        checks.append((
            not unexpected_tools,
            "No unnecessary analytics tools called"
        ))

        checks.append((
            "begin checkout" in response_text.lower(),
            "Definition references Begin Checkout"
        ))

        checks.append((
            "purchase" in response_text.lower(),
            "Definition references purchase completion"
        ))

    # --------------------------------------------------------
    # Case 5
    # --------------------------------------------------------

    elif case_id == 5:

        text = response_text.lower()

        causal_phrases = [
            "caused",
            "causes",
            "because",
            "due to",
            "the reason is",
            "contributing factor",
            "lead to abandonment",
            "leads to abandonment",
        ]

        insufficient_phrases = [
            "insufficient",
            "cannot determine",
            "can't determine",
            "do not provide causal",
            "does not provide causal",
            "not enough data",
            "causal evidence",
            "cannot establish causality",
        ]

        has_causal_claim = any(
            phrase in text
            for phrase in causal_phrases
        )

        acknowledges_limitations = any(
            phrase in text
            for phrase in insufficient_phrases
        )

        checks.append((
            acknowledges_limitations,
            "Clearly states causal evidence is insufficient"
        ))

        checks.append((
            not has_causal_claim,
            "Does not make unsupported causal claims"
        ))

    # --------------------------------------------------------
    # Case 6
    # --------------------------------------------------------

    elif case_id == 6:

        passed, reason = check_required_tools(
            [
                "search_project_knowledge",
                "get_checkout_abandonment",
            ],
            actual_tools,
        )

        checks.append((passed, reason))

        checks.append((
            response_contains_number(response_text, 56.33),
            "Overall abandonment = 56.33%"
        ))

        checks.append((
            "begin checkout" in response_text.lower(),
            "Uses project definition"
        ))

    # --------------------------------------------------------
    # Case 7
    # --------------------------------------------------------

    elif case_id == 7:

        passed, reason = check_required_tools(
            [
                "get_abandonment_by_device",
                "search_project_knowledge",
            ],
            actual_tools,
        )

        checks.append((passed, reason))

        expected_values = {
            "Tablet": 57.20,
            "Desktop": 56.86,
            "Mobile": 55.52,
        }

        for device, value in expected_values.items():

            checks.append((
                response_contains(response_text, device),
                f"Reports {device}"
            ))

            checks.append((
                response_contains_number(response_text, value),
                f"{device} abandonment = {value}%"
            ))

        checks.append((
            "begin checkout" in response_text.lower(),
            "Uses project definition"
        ))

    # --------------------------------------------------------
    # Case 8
    # --------------------------------------------------------

    elif case_id == 8:

        passed, reason = check_required_tools(
            ["get_purchase_prediction"],
            actual_tools,
        )

        checks.append((passed, reason))

        checks.append((
            "false" in response_text.lower(),
            "Reports prediction = False"
        ))

        checks.append((
            response_contains_number(response_text, 0.4157)
            or response_contains_number(response_text, 41.57),
            "Reports purchase probability = 0.4157 / 41.57%"
        ))

        # Prevent the known grounding error.
        checks.append((
            not response_contains(response_text, "checkout ratio: 2.0"),
            "Does not report checkout_ratio = 2.0"
        ))

    # --------------------------------------------------------
    # Case 9
    # --------------------------------------------------------

    elif case_id == 9:

        passed, reason = check_required_tools(
            ["get_purchase_prediction"],
            actual_tools,
        )

        checks.append((passed, reason))

        # Authoritative tool value.
        checks.append((
            response_contains_number(response_text, 0.0),
            "Uses checkout_ratio = 0.0"
        ))

        # Known regression failure.
        checks.append((
            not re.search(
                r"checkout ratio.{0,20}2\.0",
                response_text.lower(),
            ),
            "Does not recalculate checkout_ratio as 2.0"
        ))

        # Prevent unsupported recalculation language.
        checks.append((
            not (
                "begin_checkout / add_to_cart" in response_text.lower()
                or "begin checkout / add to cart" in response_text.lower()
            ),
            "Does not independently recalculate checkout_ratio"
        ))

    # --------------------------------------------------------
    # Case 10
    # --------------------------------------------------------

    elif case_id == 10:

        # If the prediction tool was called, that is acceptable.
        # If the tool itself reports "not found", the final answer
        # should not hallucinate a prediction.

        checks.append((
            not response_contains(response_text, "purchase probability"),
            "Does not invent purchase probability"
        ))

        checks.append((
            not re.search(
                r"prediction\s*[:=]\s*(true|false)",
                response_text.lower(),
            ),
            "Does not invent prediction"
        ))

        unavailable_phrases = [
            "not found",
            "not available",
            "could not retrieve",
            "unable to retrieve",
            "does not exist",
            "no data",
        ]

        checks.append((
            any(
                phrase in response_text.lower()
                for phrase in unavailable_phrases
            ),
            "Clearly states session data is unavailable"
        ))

    # --------------------------------------------------------
    # Case 11
    # --------------------------------------------------------

    elif case_id == 11:

        text = response_text.lower()

        # No Japan abandonment percentage.
        checks.append((
            not re.search(
                r"japan.{0,40}\d+(\.\d+)?%",
                text,
            ),
            "Does not invent a Japan abandonment rate"
        ))

        # Must explain unsupported country-level metric.
        unsupported_phrases = [
            "not available",
            "not supported",
            "cannot provide",
            "can't provide",
            "do not provide",
            "does not provide",
            "no country",
            "country-level",
            "country level",
        ]

        checks.append((
            any(
                phrase in text
                for phrase in unsupported_phrases
            ),
            "Explains country-level metric is unsupported"
        ))

    # --------------------------------------------------------
    # Case 12
    # --------------------------------------------------------

    elif case_id == 12:

        passed, reason = check_required_tools(
            [
                "get_abandonment_by_device",
                "get_abandonment_by_channel",
            ],
            actual_tools,
        )

        checks.append((passed, reason))

        expected_values = [
            57.20,
            56.86,
            55.52,
            100.0,
            65.95,
            65.63,
            52.82,
            43.16,
        ]

        for value in expected_values:

            checks.append((
                response_contains_number(response_text, value),
                f"Reports expected value {value}%"
            ))

    # --------------------------------------------------------
    # Case 13
    # --------------------------------------------------------

    elif case_id == 13:

        passed, reason = check_required_tools(
            ["get_funnel_metrics"],
            actual_tools,
        )

        checks.append((passed, reason))

        checks.append((
            "add to cart" in response_text.lower(),
            "Identifies Add to Cart as largest drop-off"
        ))

        checks.append((
            response_contains_number(response_text, 80.17),
            "Reports drop-off = 80.17%"
        ))

    # --------------------------------------------------------
    # Case 14
    # --------------------------------------------------------

    elif case_id == 14:

        passed, reason = check_required_tools(
            ["search_project_knowledge"],
            actual_tools,
        )

        checks.append((passed, reason))

        checks.append((
            "why do users abandon" in response_text.lower(),
            "Uses the project's main business question"
        ))

        checks.append((
            "high-intent" in response_text.lower()
            or "high intent" in response_text.lower(),
            "Mentions high-intent users"
        ))

    # --------------------------------------------------------
    # Case 15
    # --------------------------------------------------------

    elif case_id == 15:

        text = response_text.lower()

        # Must not provide a worldwide benchmark.
        checks.append((
            not re.search(
                r"(worldwide|global).{0,80}\d+(\.\d+)?%",
                text,
            ),
            "Does not invent worldwide benchmark"
        ))

        unsupported_phrases = [
            "not available",
            "not provided",
            "not in the project",
            "not available in",
            "cannot determine",
            "can't determine",
            "unsupported",
        ]

        checks.append((
            any(
                phrase in text
                for phrase in unsupported_phrases
            ),
            "Distinguishes project knowledge from external benchmark"
        ))

        # Prevent invented tool names.
        checks.append((
            "data.sampled_metrics" not in text,
            "Does not invent unsupported tool names"
        ))

    # --------------------------------------------------------
    # Unknown case
    # --------------------------------------------------------

    else:

        checks.append((
            False,
            f"No evaluator implemented for Case {case_id}"
        ))

    # ========================================================
    # Final result
    # ========================================================

    passed = all(
        result[0]
        for result in checks
    )

    return passed, checks


# ============================================================
# Run evaluation
# ============================================================

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

            # ------------------------------------------------
            # Final response
            # ------------------------------------------------

            print("\nFinal response:")
            print(response.text)

            file.write("\nFinal response:\n")
            file.write(response.text or "")
            file.write("\n")

            # ------------------------------------------------
            # Tools called
            # ------------------------------------------------

            actual_tools = get_actual_tools(tool_results)

            print("\nTools called:")

            if actual_tools:
                for tool_name in actual_tools:
                    print(f"- {tool_name}")
            else:
                print("- None")

            file.write("\nTools called:\n")

            if actual_tools:
                for tool_name in actual_tools:
                    file.write(f"- {tool_name}\n")
            else:
                file.write("- None\n")

            # ------------------------------------------------
            # Evaluation
            # ------------------------------------------------

            passed, checks = evaluate_case(
                case,
                response,
                tool_results,
            )

            print("\nEvaluation:")

            for check_passed, reason in checks:

                symbol = "✓" if check_passed else "✗"

                print(
                    f"{symbol} {reason}"
                )

                file.write(
                    f"{symbol} {reason}\n"
                )

            if passed:

                print("\nSTATUS: PASS")
                file.write("\nSTATUS: PASS\n")

                passed_cases += 1

            else:

                print("\nSTATUS: FAIL")
                file.write("\nSTATUS: FAIL\n")

                failed_cases += 1

        except Exception as error:

            error_message = str(error)

            print("\nERROR:")
            print(error_message)

            file.write("\nERROR:\n")
            file.write(error_message)
            file.write("\n")

            if (
                "RESOURCE_EXHAUSTED" in error_message
                or "429" in error_message
            ):

                status = "ERROR - API QUOTA"

            else:

                status = "ERROR"

            print(f"STATUS: {status}")

            file.write(
                f"STATUS: {status}\n"
            )

            error_cases += 1


# ============================================================
# Summary
# ============================================================

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

    file.write(f"\nPASS: {passed_cases}\n")
    file.write(f"FAIL: {failed_cases}\n")
    file.write(f"ERROR: {error_cases}\n")
    file.write(f"TOTAL: {total_cases}\n")

print(
    f"\nTest results saved to: {OUTPUT_FILE}"
)