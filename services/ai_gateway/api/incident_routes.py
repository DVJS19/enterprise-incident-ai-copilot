from fastapi import APIRouter

from services.agents.coordinator import investigate_incident
from services.llm.investigation_agent import InvestigationAgent
from services.llm.mock_bedrock_client import MockBedrockClient
from services.models.prompt_context import PromptContext
from services.ai_gateway.models.incident_api import IncidentInvestigationRequest

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.post("/investigate")
def investigate(request: IncidentInvestigationRequest):
    evidence = investigate_incident(
        service=request.service,
        symptom=request.symptom,
    )

    context = PromptContext(
        service=request.service,
        symptom=request.symptom,
        metrics_evidence=evidence["metrics"],
        deployment_evidence=evidence["deployments"],
        incident_evidence=evidence["similar_incidents"],
        ownership_evidence=evidence["ownership"],
        runbook_text=(
    evidence["runbook_preview"]
    + "\n\nKnowledge Base Results:\n"
    + str(evidence.get("knowledge_results", []))
        ),
    )

    agent = InvestigationAgent(
        bedrock_client=MockBedrockClient()
    )

    result = agent.analyze(context)

    return result.model_dump()