from services.mcp_tools.metrics_tool import find_metric_anomalies, get_metrics


def test_get_metrics_returns_sample_metric_points() -> None:
    metrics = get_metrics("payments-api")

    assert len(metrics) == 5
    assert metrics[0]["metric"] == "p95_latency_ms"


def test_find_metric_anomalies_detects_latency_and_throttling() -> None:
    anomalies = find_metric_anomalies("payments-api")

    assert anomalies["max_p95_latency_ms"] == 1900
    assert anomalies["has_latency_spike"] is True
    assert anomalies["has_dynamodb_throttling"] is True


def test_find_metric_anomalies_handles_unknown_service() -> None:
    anomalies = find_metric_anomalies("unknown-service")

    assert anomalies["max_p95_latency_ms"] == 0
    assert anomalies["has_latency_spike"] is False
    assert anomalies["has_dynamodb_throttling"] is False
