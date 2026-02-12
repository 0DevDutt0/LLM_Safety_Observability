import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
DEFAULT_MODEL = os.getenv("MODEL_NAME")


class LLMServiceError(Exception):
    pass


def call_ollama(prompt: str, model_name: str = None):
    if not OLLAMA_URL:
        raise LLMServiceError("OLLAMA_URL not configured")

    model = model_name if model_name else DEFAULT_MODEL

    start_time = time.time()

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise LLMServiceError("LLM request timed out")

    except requests.exceptions.RequestException as e:
        raise LLMServiceError(f"LLM request failed: {str(e)}")

    latency_ms = (time.time() - start_time) * 1000

    return {
        "response": response.json().get("response", ""),
        "latency_ms": latency_ms,
        "model_name": model
    }
