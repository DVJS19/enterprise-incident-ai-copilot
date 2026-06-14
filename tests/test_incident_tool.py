from services.mcp_tools.incident_tool import search_similar_incidents


def test_search_similar_incidents_matches_service_and_symptom() -> None:
    incidents = search_similar_incidents("payments-api", "latency")

    assert len(incidents) == 1
    assert incidents[0]["incident_id"] == "INC-1001"
    assert incidents[0]["root_cause"] == "DynamoDB throttling after inefficient query pattern"


def test_search_similar_incidents_returns_empty_list_for_unknown_service() -> None:
    assert search_similar_incidents("unknown-service", "latency") == []
