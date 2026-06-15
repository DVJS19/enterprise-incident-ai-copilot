from services.llm.investigation_agent import InvestigationAgent
from services.llm.mock_bedrock_client import MockBedrockClient
from services.models.prompt_context import PromptContext


def test_investigation_agent_returns_structured_result_with_mock_client() -> None:
    context = PromptContext(
        service="payments-api",
        symptom="latency",
        metrics_evidence={
            "max_p95_latency_ms": 1900,
            "has_latency_spike": True,
            "has_dynamodb_throttling": True,
        },
        deployment_evidence=[
            {
                "version": "v1.42",
                "changes": [
                    "Changed DynamoDB access pattern",
                    "Disabled payment-profile-cache",
                ],
            }
        ],
        incident_evidence=[
            {
                "root_cause": "DynamoDB throttling after inefficient query pattern",
            }
        ],
        ownership_evidence={
            "owner": "payments-platform-team",
            "tier": "critical",
        },
        runbook_text=(
            "Re-enable payment-profile-cache. "
            "Roll back latest deployment. "
            "Temporarily increase DynamoDB read capacity."
        ),
    )

    agent = InvestigationAgent(
        bedrock_client=MockBedrockClient()
    )

    result = agent.analyze(context)

    assert result.confidence == 0.92
    assert "DynamoDB throttling" in result.root_cause
    assert len(result.recommended_actions) > 0
    assert len(result.escalation_recommendations) > 0