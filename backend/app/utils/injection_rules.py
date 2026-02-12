INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "override safety",
    "bypass restrictions",
    "act as system",
    "developer mode"
]


def detect_prompt_injection(prompt: str) -> bool:
    prompt_lower = prompt.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in prompt_lower:
            return True
    return False
