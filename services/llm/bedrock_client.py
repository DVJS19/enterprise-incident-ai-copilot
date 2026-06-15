import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_REGION = "us-west-2"
#DEFAULT_MODEL_ID = "anthropic.claude-sonnet-4-20250514-v1:0"
DEFAULT_MODEL_ID = "anthropic.claude-haiku-4-5-20251001-v1:0"


def _inference_profile_model_id(model_id: str, region_name: str) -> str:
    if model_id.startswith(("us.", "eu.", "apac.", "global.")):
        return model_id

    if region_name.startswith("us-"):
        return f"us.{model_id}"

    if region_name.startswith("eu-") or region_name == "il-central-1":
        return f"eu.{model_id}"

    if region_name.startswith("ap-"):
        return f"apac.{model_id}"

    return f"global.{model_id}"


class BedrockClient:
    def __init__(
        self,
        model_id: str | None = None,
        region_name: str | None = None,
    ) -> None:
        self.region_name = (
            region_name
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or DEFAULT_REGION
        )

        self.model_id = (
            model_id
            or os.getenv("BEDROCK_MODEL_ID")
            or DEFAULT_MODEL_ID
        )

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.region_name,
        )

    def converse(self, prompt: str) -> str:
        return self._converse(prompt, self.model_id)

    def _converse(self, prompt: str, model_id: str) -> str:
        try:
            response = self.client.converse(
                modelId=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": 1200,
                    "temperature": 0.2,
                },
            )

            return response["output"]["message"]["content"][0]["text"]

        except ClientError as exc:
            error = exc.response.get("Error", {})
            code = error.get("Code", "Unknown")
            message = error.get("Message", str(exc))

            if code == "ValidationException" and "Operation not allowed" in message:
                return self._invoke_model(prompt, model_id)

            profile_model_id = _inference_profile_model_id(model_id, self.region_name)
            if code == "ValidationException" and profile_model_id != model_id:
                return self._converse(prompt, profile_model_id)

            raise RuntimeError(
                f"Bedrock Converse failed for model '{model_id}' "
                f"in region '{self.region_name}': {code}: {message}"
            ) from exc

        except BotoCoreError as exc:
            raise RuntimeError(
                f"Bedrock Converse could not reach AWS: {exc}"
            ) from exc

    def _invoke_model(self, prompt: str, model_id: str) -> str:
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        "max_tokens": 1200,
                        "temperature": 0.2,
                    }
                ),
            )
        except ClientError as exc:
            error = exc.response.get("Error", {})
            code = error.get("Code", "Unknown")
            message = error.get("Message", str(exc))
            profile_model_id = _inference_profile_model_id(model_id, self.region_name)
            if code == "ValidationException" and profile_model_id != model_id:
                return self._invoke_model(prompt, profile_model_id)

            raise RuntimeError(
                f"Bedrock InvokeModel fallback failed for model '{model_id}' "
                f"in region '{self.region_name}': {code}: {message}"
            ) from exc

        except BotoCoreError as exc:
            raise RuntimeError(
                f"Bedrock InvokeModel fallback could not reach AWS: {exc}"
            ) from exc

        payload = json.loads(response["body"].read())
        return payload["content"][0]["text"]
