from services.mcp_tools.runbook_tool import get_runbook


def test_get_runbook_returns_matching_runbook_text() -> None:
    runbook = get_runbook("payments-api", "latency")

    assert "# Payments API Latency Runbook" in runbook
    assert "Re-enable payment-profile-cache" in runbook


def test_get_runbook_returns_empty_string_for_missing_runbook() -> None:
    assert get_runbook("unknown-service", "latency") == ""
