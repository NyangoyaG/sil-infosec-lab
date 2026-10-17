from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
from guardrails import inspect_input, inspect_output

app = FastAPI(
    title="SIL Infosec Assessment API",
    description="Two sample APIs for the API Gateway and AI Guardrails lab",
    version="1.0.0",
)


@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """Return the service health status."""
    return {
        "status": "healthy",
        "service": "sil-assessment-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/reports/summary", tags=["Reports"])
def reports_summary():
    """Return a summary using synthetic demonstration data."""
    return {
        "report_id": "DEMO-001",
        "period": "2026-Q3",
        "total_cases": 120,
        "open_cases": 18,
        "closed_cases": 102,
        "data_classification": "synthetic-demo-data",
    }
    from fastapi import HTTPException
from pydantic import BaseModel, Field


class AIInspectRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


@app.post("/api/v1/ai/inspect", tags=["AI Guardrails"])
def inspect_ai_request(request: AIInspectRequest):
    """Inspect text using the demonstration AI guardrails."""
    input_result = inspect_input(request.text)

    if not input_result.allowed:
        raise HTTPException(
            status_code=400,
            detail="Request blocked by AI security policy",
        )

    # Simulated response only; no live AI model is called.
    simulated_response = (
        f"Demo response received for: {input_result.sanitized_text}"
    )

    output_result = inspect_output(simulated_response)

    return {
        "status": "processed",
        "input": input_result.sanitized_text,
        "response": output_result.sanitized_text,
        "input_guardrail": input_result.reason,
        "output_guardrail": output_result.reason,
    }
