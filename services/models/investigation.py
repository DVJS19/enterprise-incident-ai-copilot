from pydantic import BaseModel, Field


class InvestigationResult(BaseModel):
    root_cause: str = Field(
        description="Most likely root cause"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

    impact_assessment: str = Field(
        description="Business impact analysis"
    )

    recommended_actions: list[str] = Field(
        default_factory=list
    )

    escalation_recommendations: list[str] = Field(
        default_factory=list
    )