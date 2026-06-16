from fastapi import APIRouter

from services.ai_gateway.models.incident_api import IncidentInvestigationRequest
from services.workflows.investigation_workflow import InvestigationWorkflow

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.post("/investigate")
def investigate(request: IncidentInvestigationRequest):
    workflow = InvestigationWorkflow()

    return workflow.execute(
        service=request.service,
        symptom=request.symptom,
    )