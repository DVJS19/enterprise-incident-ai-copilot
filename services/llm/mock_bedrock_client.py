class MockBedrockClient:
    """
    Local mock for Bedrock Runtime.

    Purpose:
    - Lets us continue development when AWS Bedrock runtime access is blocked.
    - Returns deterministic JSON that matches InvestigationResult.
    - Allows unit tests without calling AWS.
    """

    def converse(self, prompt: str) -> str:
        return """
{
  "root_cause": "DynamoDB throttling after deployment v1.42 changed the access pattern and disabled cache.",
  "confidence": 0.92,
  "impact_assessment": "Payments API p95 latency exceeded the 500ms SLO and may affect checkout confirmation latency.",
  "recommended_actions": [
    "Re-enable payment-profile-cache.",
    "Review or roll back deployment v1.42.",
    "Temporarily increase DynamoDB read capacity.",
    "Create a follow-up task to optimize the DynamoDB access pattern."
  ],
  "escalation_recommendations": [
    "Notify payments-platform-team.",
    "Escalate to payments-oncall@example.com if latency remains above SLO."
  ]
}
"""