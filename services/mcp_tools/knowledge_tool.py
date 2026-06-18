from pathlib import Path
from typing import Any
import re
from services.rag.rag_service import rag_service


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "sample_data" / "knowledge_base"


def search_knowledge_base(
    query: str,
    service: str | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    query_terms = {
        term.lower()
        for term in query.replace("-", " ").split()
        if len(term) > 2
    }

    fix_terms = [
        "fix",
        "mitigation",
        "resolution",
        "known issue",
        "postmortem",
        "runbook",
        "rollback",
        "re-enable",
    ]

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        searchable_text = f"{file_path.name} {content}".lower()

        if service and service.lower() not in searchable_text:
            continue

        score = sum(1 for term in query_terms if term in searchable_text)

        boost = 0

        for term in fix_terms:
            if term in searchable_text:
                boost += 2

        if "architecture" in file_path.name.lower():
            boost -= 2

        score += boost

        if score > 0:
            results.append(
                {
                    "document_name": file_path.name,
                    "score": score,
                    "content_preview": content[:800],
                }
            )

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )

def extract_recommended_actions(content: str) -> list[str]:
    match = re.search(
        r"### Recommended Fix(.*)",
        content,
        flags=re.DOTALL,
    )

    if not match:
        return []

    section = match.group(1)

    actions = []

    for line in section.splitlines():
        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():
            actions.append(
                line.split(".", 1)[1].strip()
            )

    return actions

def find_known_fix(
    service: str,
    symptom: str,
    min_score: float = 0.05,
) -> dict | None:
    query = f"{service} {symptom} fix mitigation resolution rollback re-enable"

    results = rag_service.search(
        query=query,
        top_k=5,
    )

    for result in results:
        if result.score < min_score:
            continue

        actions = extract_recommended_actions(result.text)

        if not actions:
            continue

        return {
            "match_type": "known_fix",
            "confidence": round(min(result.score * 10, 1.0), 2),
            "document_name": result.document_name,
            "recommended_actions": actions,
            "score": result.score,
        }

    return None