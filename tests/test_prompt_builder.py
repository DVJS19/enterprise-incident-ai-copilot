# tests/test_prompt_builder.py

from services.models.prompt_context import PromptContext
from services.prompts.prompt_builder import build_investigation_prompt


def test_build_investigation_prompt_includes_evidence() -> None:
    context = PromptContext(
        service="payments-api",
        symptom="latency",
        metrics_evidence={"has_latency_spike": True},
        deployment_evidence=[{"version": "v1.42"}],
    )

    prompt = build_investigation_prompt(context)

    assert "senior enterprise incident response engineer" in prompt
    assert "payments-api" in prompt
    assert "v1.42" in prompt
    assert "has_latency_spike" in prompt