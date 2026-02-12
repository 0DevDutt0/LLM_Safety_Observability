from backend.app.db.database import SessionLocal
from backend.app.db.models import LLMLog
from backend.app.utils.token_counter import estimate_tokens


COST_PER_1K_TOKENS = 0.002  # simulated cost


def create_log(prompt, response, latency_ms, injection_detected, model_name):
    db = SessionLocal()
    try:
        prompt_tokens = estimate_tokens(prompt)
        response_tokens = estimate_tokens(response)

        total_tokens = prompt_tokens + response_tokens
        estimated_cost = (total_tokens / 1000) * COST_PER_1K_TOKENS

        log_entry = LLMLog(
            prompt=prompt,
            response=response,
            latency_ms=latency_ms,
            injection_detected=injection_detected,
            hallucination_score=None,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            estimated_cost=estimated_cost
        )

        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)

        return log_entry.id

    finally:
        db.close()


def update_hallucination_score(log_id, score):
    db = SessionLocal()
    try:
        log_entry = db.query(LLMLog).filter(LLMLog.id == log_id).first()
        if log_entry:
            log_entry.hallucination_score = score
            db.commit()
    finally:
        db.close()
