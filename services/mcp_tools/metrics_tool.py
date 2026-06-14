import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
METRICS_DIR = PROJECT_ROOT / "sample_data" / "metrics"


def get_metrics(service: str) -> list[dict[str, Any]]:
    file_path = METRICS_DIR / f"{service}.json"

   
    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_metric_anomalies(service: str) -> dict[str, Any]:
    metrics = get_metrics(service)

    latency_points = [
        item for item in metrics
        if item.get("metric") == "p95_latency_ms"
    ]

    throttling_points = [
        item for item in metrics
        if item.get("metric") == "dynamodb_throttled_requests"
    ]

    max_latency = max(
        [point["value"] for point in latency_points],
        default=0
    )

    has_latency_spike = max_latency > 500
    has_dynamodb_throttling = any(
        point["value"] > 0 for point in throttling_points
    )

    return {
        "service": service,
        "max_p95_latency_ms": max_latency,
        "has_latency_spike": has_latency_spike,
        "has_dynamodb_throttling": has_dynamodb_throttling,
        "evidence": metrics,
    }