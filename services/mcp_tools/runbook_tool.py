from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNBOOKS_DIR = PROJECT_ROOT / "sample_data" / "runbooks"


def get_runbook(service: str, incident_type: str = "latency") -> str:
    file_path = RUNBOOKS_DIR / f"{service}-{incident_type}.md"

    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8")