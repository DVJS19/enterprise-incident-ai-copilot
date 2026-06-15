from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError, ProxyConnectionError

from services.llm.bedrock_client import (
    DEFAULT_MODEL_ID,
    DEFAULT_REGION,
    BedrockClient,
)


def test_bedrock_client_uses_foundation_model_by_default() -> None:
    with patch("services.llm.bedrock_client.boto3.client") as boto3_client:
        client = BedrockClient()

    assert client.model_id == DEFAULT_MODEL_ID
    assert client.region_name == DEFAULT_REGION
    boto3_client.assert_called_once_with("bedrock-runtime", region_name=DEFAULT_REGION)


def test_bedrock_client_reads_aws_default_region(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-west-1")
    monkeypatch.setenv("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID)

    with patch("services.llm.bedrock_client.boto3.client"):
        client = BedrockClient()

    assert client.region_name == "eu-west-1"
    assert client.model_id == DEFAULT_MODEL_ID


def test_bedrock_client_keeps_explicit_foundation_model_id() -> None:
    with patch("services.llm.bedrock_client.boto3.client"):
        client = BedrockClient(
            model_id=DEFAULT_MODEL_ID,
            region_name="us-west-2",
        )

    assert client.model_id == DEFAULT_MODEL_ID


def test_converse_returns_text_from_response() -> None:
    bedrock = BedrockClient.__new__(BedrockClient)
    bedrock.model_id = DEFAULT_MODEL_ID
    bedrock.region_name = DEFAULT_REGION
    bedrock.client = Mock()
    bedrock.client.converse.return_value = {
        "output": {
            "message": {
                "content": [{"text": '{"ok": true}'}],
            }
        }
    }

    assert bedrock.converse('Return only this JSON: {"ok": true}') == '{"ok": true}'


def test_converse_wraps_bedrock_client_errors() -> None:
    bedrock = BedrockClient.__new__(BedrockClient)
    bedrock.model_id = DEFAULT_MODEL_ID
    bedrock.region_name = DEFAULT_REGION
    bedrock.client = Mock()
    bedrock.client.converse.side_effect = ClientError(
        {
            "Error": {
                "Code": "ValidationException",
                "Message": "Use an inference profile ID for this model.",
            }
        },
        "Converse",
    )

    with pytest.raises(RuntimeError, match="ValidationException"):
        bedrock.converse("hello")


def test_converse_falls_back_to_invoke_model_when_operation_not_allowed() -> None:
    bedrock = BedrockClient.__new__(BedrockClient)
    bedrock.model_id = DEFAULT_MODEL_ID
    bedrock.region_name = DEFAULT_REGION
    bedrock.client = Mock()
    bedrock.client.converse.side_effect = ClientError(
        {
            "Error": {
                "Code": "ValidationException",
                "Message": "Operation not allowed",
            }
        },
        "Converse",
    )
    bedrock.client.invoke_model.return_value = {
        "body": Mock(read=Mock(return_value=b'{"content": [{"text": "{\\"ok\\": true}"}]}'))
    }

    assert bedrock.converse('Return only this JSON: {"ok": true}') == '{"ok": true}'
    bedrock.client.invoke_model.assert_called_once()


def test_converse_retries_with_inference_profile_after_validation_error() -> None:
    bedrock = BedrockClient.__new__(BedrockClient)
    bedrock.model_id = DEFAULT_MODEL_ID
    bedrock.region_name = DEFAULT_REGION
    bedrock.client = Mock()
    bedrock.client.converse.side_effect = [
        ClientError(
            {
                "Error": {
                    "Code": "ValidationException",
                    "Message": "Use an inference profile ID for this model.",
                }
            },
            "Converse",
        ),
        {
            "output": {
                "message": {
                    "content": [{"text": '{"ok": true}'}],
                }
            }
        },
    ]

    assert bedrock.converse('Return only this JSON: {"ok": true}') == '{"ok": true}'
    assert bedrock.client.converse.call_args_list[0].kwargs["modelId"] == DEFAULT_MODEL_ID
    assert bedrock.client.converse.call_args_list[1].kwargs["modelId"] == (
        f"us.{DEFAULT_MODEL_ID}"
    )


def test_converse_wraps_bedrock_transport_errors() -> None:
    bedrock = BedrockClient.__new__(BedrockClient)
    bedrock.model_id = DEFAULT_MODEL_ID
    bedrock.region_name = DEFAULT_REGION
    bedrock.client = Mock()
    bedrock.client.converse.side_effect = ProxyConnectionError(
        proxy_url="http://127.0.0.1:9",
        error="connection refused",
    )

    with pytest.raises(RuntimeError, match="could not reach AWS"):
        bedrock.converse("hello")
