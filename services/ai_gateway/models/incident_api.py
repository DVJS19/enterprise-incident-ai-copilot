from pydantic import BaseModel


class IncidentInvestigationRequest(BaseModel):
    service: str
    symptom: str = "latency"