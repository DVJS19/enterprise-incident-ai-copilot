from services.mcp_tools.deployment_tool import get_recent_deployments


def test_get_recent_deployments_returns_sample_deployment() -> None:
    deployments = get_recent_deployments("payments-api")

    assert deployments[0]["version"] == "v1.42"
    assert "Changed DynamoDB access pattern" in deployments[0]["changes"]


def test_get_recent_deployments_returns_empty_list_for_unknown_service() -> None:
    assert get_recent_deployments("unknown-service") == []
