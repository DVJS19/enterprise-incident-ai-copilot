from services.mcp_tools.deployment_tool import get_recent_deployments
from services.mcp_tools.incident_tool import search_similar_incidents
from services.mcp_tools.metrics_tool import find_metric_anomalies
from services.mcp_tools.ownership_tool import get_service_owner
from services.mcp_tools.runbook_tool import get_runbook
from services.mcp_tools.knowledge_tool import search_knowledge_base


def investigate_incident(service: str, symptom: str = "latency") -> dict:
    metrics = find_metric_anomalies(service)
    deployments = get_recent_deployments(service)
    similar_incidents = search_similar_incidents(service, symptom)
    ownership = get_service_owner(service)
    runbook = get_runbook(service, symptom)

    knowledge_results = search_knowledge_base(
    query=f"{service} {symptom}",
    service=service,
    )

    return {
        "service": service,
        "symptom": symptom,
        "metrics": metrics,
        "deployments": deployments,
        "similar_incidents": similar_incidents,
        "ownership": ownership,
        "runbook_found": bool(runbook),
        "runbook_preview": runbook[:500],
        "likely_root_cause": _infer_root_cause(metrics, deployments, similar_incidents),
        "recommended_actions": _recommend_actions(metrics, deployments, similar_incidents),
        "knowledge_results": knowledge_results,
    }


def _infer_root_cause(metrics: dict, deployments: list, similar_incidents: list) -> str:
    if (
        metrics.get("has_latency_spike")
        and metrics.get("has_dynamodb_throttling")
        and deployments
    ):
        return "Likely DynamoDB throttling after recent deployment changed access pattern."

    if similar_incidents:
        return similar_incidents[0].get("root_cause", "Similar incident found.")

    return "Insufficient evidence to determine root cause."


def _recommend_actions(metrics: dict, deployments: list, similar_incidents: list) -> list[str]:
    actions = []

    if deployments:
        actions.append("Review or roll back the latest deployment.")

    if metrics.get("has_dynamodb_throttling"):
        actions.append("Temporarily increase DynamoDB read capacity or investigate hot partitions.")

    if metrics.get("has_latency_spike"):
        actions.append("Re-enable cache if disabled and monitor p95 latency.")

    if similar_incidents:
        actions.append("Review prior incident resolution and compare symptoms.")

    actions.append("Notify the service owner and document findings.")

    return actions