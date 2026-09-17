from google import genai
from pydantic import BaseModel, Field

from ai.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


class ProductAnalysis(BaseModel):
    question: str = Field(description="The original product analytics question.")
    possible_reasons: list[str] = Field(
        description="Possible reasons explaining the user behavior."
    )


def analyze_product_question(question: str) -> ProductAnalysis:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config={
            "response_mime_type": "application/json",
            "response_schema": ProductAnalysis,
        },
    )

    if response.text is None:
        raise ValueError("Gemini returned an empty response.")

    return ProductAnalysis.model_validate_json(response.text)