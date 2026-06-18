class CloudWatchMetricsPublisher:
    """
    Phase 1 implementation.

    Currently:
    - Logs metrics

    Future:
    - Publishes custom metrics to CloudWatch
    """

    def publish(self, metric_name: str, value: float) -> None:
        print(
            f"[METRIC] {metric_name}={value}"
        )