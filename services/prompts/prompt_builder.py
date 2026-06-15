from pathlib import Path

from services.models.prompt_context import PromptContext

PROMPT_FILE = (
    Path(__file__).parent
    / "coordinator_prompt.txt"
)


def build_investigation_prompt(
    context: PromptContext,
) -> str:
    template = PROMPT_FILE.read_text(
        encoding="utf-8"
    )

    evidence = context.model_dump_json(
        indent=2
    )

    return template.format(
        evidence=evidence
    )