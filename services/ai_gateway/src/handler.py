import json
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import boto3

dynamodb = boto3.resource("dynamodb")
INCIDENT_TABLE = os.environ["INCIDENT_STATE_TABLE"]
AUDIT_TABLE = os.environ["AUDIT_LOG_TABLE"]

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
            "x-correlation-id": body.get("correlationId", ""),
        },
        "body": json.dumps(body),
    }

def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    headers = event.get("headers") or {}
    correlation_id = headers.get("x-correlation-id") or headers.get("X-Correlation-Id") or str(uuid.uuid4())

    try:
        body = json.loads(event.get("body") or "{}")
        service = body.get("service")
        severity = body.get("severity", "SEV3")
        description = body.get("description", "")

        if not service or not description:
            return _response(400, {"message": "service and description are required.", "correlationId": correlation_id})

        now = _utc_now()
        incident_id = f"INC-{int(time.time())}-{str(uuid.uuid4())[:8]}"
        ttl = int(time.time()) + 60 * 60 * 24 * 30

        incident_item = {
            "PK": f"INCIDENT#{incident_id}",
            "SK": f"STATE#{now}",
            "incidentId": incident_id,
            "service": service,
            "severity": severity,
            "status": "received",
            "description": description,
            "correlationId": correlation_id,
            "createdAt": now,
            "ttl": ttl,
        }

        audit_item = {
            "PK": "TENANT#default",
            "SK": f"AUDIT#{now}#{correlation_id}",
            "eventType": "incident_received",
            "incidentId": incident_id,
            "correlationId": correlation_id,
            "service": service,
            "createdAt": now,
            "ttl": ttl,
        }

        dynamodb.Table(INCIDENT_TABLE).put_item(Item=incident_item)
        dynamodb.Table(AUDIT_TABLE).put_item(Item=audit_item)

        print(json.dumps({
            "level": "INFO",
            "event": "incident_received",
            "incidentId": incident_id,
            "correlationId": correlation_id,
            "service": service,
            "severity": severity,
        }))

        return _response(202, {
            "incidentId": incident_id,
            "correlationId": correlation_id,
            "status": "received",
            "message": "Incident accepted. Phase 1 stores state only; agents are added later.",
        })

    except json.JSONDecodeError:
        return _response(400, {"message": "Invalid JSON request body.", "correlationId": correlation_id})
    except Exception as exc:
        print(json.dumps({"level": "ERROR", "event": "incident_request_failed", "correlationId": correlation_id, "error": str(exc)}))
        return _response(500, {"message": "Internal server error.", "correlationId": correlation_id})
