
from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    service: str
    symptom: str

    metrics_evidence: dict = Field(default_factory=dict)
    deployment_evidence: list[dict] = Field(default_factory=list)
    incident_evidence: list[dict] = Field(default_factory=list)
    ownership_evidence: dict = Field(default_factory=dict)

    runbook_text: str = ""