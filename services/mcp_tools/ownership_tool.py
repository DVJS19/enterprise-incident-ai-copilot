import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_CATALOG_DIR = PROJECT_ROOT / "sample_data" / "service_catalog"


def get_service_owner(service: str) -> dict[str, Any]:
    file_path = SERVICE_CATALOG_DIR / f"{service}.json"

    if not file_path.exists():
        return {}

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)