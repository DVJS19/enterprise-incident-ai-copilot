import json

from pydantic import ValidationError

from services.llm.bedrock_client import BedrockClient
from services.models.investigation import InvestigationResult
from services.models.prompt_context import PromptContext
from services.prompts.prompt_builder import build_investigation_prompt


class InvestigationAgent:
    def __init__(self, bedrock_client: BedrockClient | None = None) -> None:
        self.bedrock_client = bedrock_client or BedrockClient()

    def analyze(self, context: PromptContext) -> InvestigationResult:
        prompt = build_investigation_prompt(context)
        response_text = self.bedrock_client.converse(prompt)

        try:
            payload = json.loads(response_text)
            return InvestigationResult.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(
                f"Bedrock response was not valid InvestigationResult JSON: {response_text}"
            ) from exc