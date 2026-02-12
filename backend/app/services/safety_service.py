from backend.app.utils.injection_rules import detect_prompt_injection


def run_safety_checks(prompt: str) -> dict:
    injection_detected = detect_prompt_injection(prompt)

    return {
        "injection_detected": injection_detected
    }
