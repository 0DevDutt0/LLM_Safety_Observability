import os
from dotenv import load_dotenv

load_dotenv()


def validate_environment():
    required_vars = [
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "OLLAMA_URL",
        "MODEL_NAME"
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise RuntimeError(f"Missing environment variables: {missing}")
