from backend.app.services.llm_service import call_ollama


def score_hallucination(prompt: str, response: str) -> float:
    evaluation_prompt = f"""
    Evaluate the factual correctness of the following answer
    to the user question.

    Question:
    {prompt}

    Answer:
    {response}

    Rate factual correctness from 1 to 10.
    Respond with only a number.
    """

    result = call_ollama(evaluation_prompt)

    try:
        score = float(result["response"].strip())
    except:
        score = None

    return score
