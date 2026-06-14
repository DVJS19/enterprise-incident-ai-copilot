from services.mcp_tools.ownership_tool import get_service_owner


def test_get_service_owner_returns_sample_owner() -> None:
    ownership = get_service_owner("payments-api")

    assert ownership["owner"] == "payments-platform-team"
    assert ownership["tier"] == "critical"
    assert ownership["escalation"] == "payments-oncall@example.com"


def test_get_service_owner_returns_empty_dict_for_unknown_service() -> None:
    assert get_service_owner("unknown-service") == {}
