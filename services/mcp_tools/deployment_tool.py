import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEPLOYMENTS_DIR = PROJECT_ROOT / "sample_data" / "deployments"


def get_recent_deployments(service: str) -> list[dict[str, Any]]:
    file_path = DEPLOYMENTS_DIR / f"{service}.json"

    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)