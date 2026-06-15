from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "sample_data" / "knowledge_base"


def search_knowledge_base(query: str, service: str | None = None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    query_terms = {
        term.lower()
        for term in query.replace("-", " ").split()
        if len(term) > 2
    }

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        searchable_text = f"{file_path.name} {content}".lower()

        if service and service.lower() not in searchable_text:
            continue

        score = sum(
            1 for term in query_terms
            if term in searchable_text
        )

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