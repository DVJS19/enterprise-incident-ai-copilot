from services.agents.coordinator import investigate_incident
from services.llm.investigation_agent import InvestigationAgent
from services.llm.mock_bedrock_client import MockBedrockClient
from services.mcp_tools.knowledge_tool import find_known_fix
from services.models.prompt_context import PromptContext
from time import perf_counter
from services.observability.cloudwatch_publisher import (
    CloudWatchMetricsPublisher,
)

class InvestigationWorkflow:
    def __init__(self) -> None:
        self.agent = InvestigationAgent(
            bedrock_client=MockBedrockClient()
        )
        self.publisher = CloudWatchMetricsPublisher()

    def execute(self, service: str, symptom: str) -> dict:
        start_time = perf_counter()
        known_fix = find_known_fix(
            service=service,
            symptom=symptom,
            min_score=0.05,

        )
       
        if known_fix and known_fix["confidence"] >= 0.2:
            workflow_duration_ms = round((perf_counter() - start_time) * 1000, 2)
            self._publish_metrics(
            workflow_duration_ms=workflow_duration_ms,
            retrieval_hits=1,
            llm_invoked=False,
            )


            return {
                "source": "knowledge_base",
                "routing_decision": "known_fix_found_no_llm_called",
                "confidence": known_fix["confidence"],
                "document_name": known_fix["document_name"],
                "recommended_actions": known_fix["recommended_actions"],
                "metrics": {
                     "llm_invoked": False,
                     "retrieval_hits": 1
                },
                "workflow_duration_ms": workflow_duration_ms
            }

        evidence = investigate_incident(
            service=service,
            symptom=symptom,
        )

        context = PromptContext(
            service=service,
            symptom=symptom,
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

        result = self.agent.analyze(context)
        workflow_duration_ms = round((perf_counter() - start_time) * 1000, 2)
        self._publish_metrics(
            workflow_duration_ms=workflow_duration_ms,
            retrieval_hits=1,
            llm_invoked=False,
            )

        return {
            "source": "llm",
            "routing_decision": "evidence_analysis_required",
            **result.model_dump(),
             "metrics": {
                "llm_invoked": True,
                "retrieval_hits": len(
                    evidence.get("knowledge_results", [])
        ),
        },
        "workflow_duration_ms": workflow_duration_ms
    }

    def _publish_metrics(
        self,
        workflow_duration_ms: float,
        retrieval_hits: int,
        llm_invoked: bool,
    ) -> None:
        self.publisher.publish(
            "WorkflowDurationMs",
            workflow_duration_ms,
        )

        self.publisher.publish(
            "RetrievalHits",
            retrieval_hits,
        )

        self.publisher.publish(
            "LLMInvoked",
            1 if llm_invoked else 0,
        )