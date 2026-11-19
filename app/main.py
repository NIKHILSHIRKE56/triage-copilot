from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.triage import analyze_incident

app = FastAPI(
    title="DNO Cloud Log & API Triage Copilot",
    description="Air-gapped, zero-cost AI triage engine for telecom support teams.",
    version="1.0.0",
)


class TriageRequest(BaseModel):
    incident_log: str
    customer_name: str = "Enterprise Carrier"


@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "air-gapped-local"}


@app.post("/api/v1/triage")
def triage_incident(payload: TriageRequest):
    try:
        return analyze_incident(payload.incident_log, payload.customer_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
