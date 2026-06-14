import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INCIDENTS_DIR = PROJECT_ROOT / "sample_data" / "incidents"


def search_similar_incidents(service: str, symptom: str) -> list[dict[str, Any]]:
    matches = []

    for file_path in INCIDENTS_DIR.glob("*.json"):
        with file_path.open("r", encoding="utf-8") as file:
            incident = json.load(file)

        same_service = incident.get("service") == service
        symptom_match = symptom.lower() in incident.get("symptom", "").lower()

        if same_service and symptom_match:
            matches.append(incident)

    return matches