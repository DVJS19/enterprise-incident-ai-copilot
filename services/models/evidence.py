from pydantic import BaseModel


class MetricsEvidence(BaseModel):
    max_p95_latency_ms: int
    has_latency_spike: bool
    has_dynamodb_throttling: bool


class DeploymentEvidence(BaseModel):
    version: str
    timestamp: str


class OwnershipEvidence(BaseModel):
    owner: str
    tier: str
    