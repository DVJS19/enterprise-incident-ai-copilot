from pydantic import BaseModel


class InvestigationRequest(BaseModel):
    service: str
    symptom: str