from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from backend.app.services.safety_service import run_safety_checks
from backend.app.services.llm_service import call_ollama
from backend.app.services.logging_service import (
    create_log,
    update_hallucination_score
)
from backend.app.services.evaluation_service import score_hallucination


router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str
    model_name: str | None = None
    compare_with: str | None = None


def background_scoring(log_id, prompt, response):
    score = score_hallucination(prompt, response)
    update_hallucination_score(log_id, score)


@router.post("/generate")
async def generate(request: GenerateRequest, background_tasks: BackgroundTasks):
    prompt = request.prompt

    safety_result = run_safety_checks(prompt)

    if safety_result["injection_detected"]:
        raise HTTPException(
            status_code=400,
            detail="Prompt injection detected"
        )

    results = []

    # Primary model
    primary = call_ollama(prompt, request.model_name)

    log_id = create_log(
        prompt=prompt,
        response=primary["response"],
        latency_ms=primary["latency_ms"],
        injection_detected=safety_result["injection_detected"],
        model_name=primary["model_name"]
    )

    background_tasks.add_task(
        background_scoring,
        log_id,
        prompt,
        primary["response"]
    )

    results.append(primary)

    # Comparison model (optional)
    if request.compare_with:
        secondary = call_ollama(prompt, request.compare_with)

        log_id_2 = create_log(
            prompt=prompt,
            response=secondary["response"],
            latency_ms=secondary["latency_ms"],
            injection_detected=safety_result["injection_detected"],
            model_name=secondary["model_name"]
        )

        background_tasks.add_task(
            background_scoring,
            log_id_2,
            prompt,
            secondary["response"]
        )

        results.append(secondary)

    return {
        "results": results,
        "message": "Background scoring running"
    }
