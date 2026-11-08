"""
Milestone 1: LLM Connection & Structured Output Sanity Check
Using native google-genai SDK with gemini-3.5-flash.
"""

import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

# 1. Load environment variables from .env
load_dotenv()

# 2. Instantiate native Google GenAI client
# It automatically picks up GEMINI_API_KEY from environment
client = genai.Client()

MODEL_NAME = "gemini-3.5-flash"


def test_basic_generation():
    """Verify basic text generation."""
    print("=" * 60)
    print(f"1. Testing text generation with {MODEL_NAME}...")
    print("=" * 60)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="In one concise sentence, explain why agentic workflows use multi-step planning.",
    )
    print("\n[Model Output]:")
    print(response.text.strip())


# Define a minimal Pydantic model to test Native Structured Output
class HealthCheckResult(BaseModel):
    status: str = Field(description="Operational status, e.g., 'ready'")
    recommended_model: str = Field(description="The primary model being used")
    reason_for_native_sdk: str = Field(description="Brief reason why native SDK is chosen")


def test_structured_output():
    """Verify that Gemini produces schema-guaranteed JSON directly into Pydantic."""
    print("\n" + "=" * 60)
    print(f"2. Testing native structured output (Pydantic schema)...")
    print("=" * 60)

    prompt = (
        "We are building a multi-agent research system in Python using native google-genai. "
        "Confirm our status is ready, list the recommended model as gemini-3.5-flash, "
        "and provide the primary reason for choosing native SDK over wrappers."
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": HealthCheckResult,
        },
    )

    # Validate and parse directly into our Pydantic object
    result = HealthCheckResult.model_validate_json(response.text)
    print("\n[Parsed Pydantic Object]:")
    print(f"Status:                {result.status}")
    print(f"Model:                 {result.recommended_model}")
    print(f"Reason:                {result.reason_for_native_sdk}")


if __name__ == "__main__":
    test_basic_generation()
    test_structured_output()
    print("\n" + "=" * 60)
    print("Sanity check complete! Environment & native Gemini SDK are verified.")
    print("=" * 60)

