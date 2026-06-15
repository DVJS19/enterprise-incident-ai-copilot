from fastapi import FastAPI

from services.ai_gateway.api.incident_routes import router as incident_router

app = FastAPI(
    title="Enterprise Incident Response Copilot",
    version="0.3.0",
)

app.include_router(incident_router)


@app.get("/health")
def health():
    return {"status": "ok"}