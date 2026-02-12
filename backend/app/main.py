from fastapi import FastAPI
from backend.app.api.routes import router
from backend.app.db.database import engine
from backend.app.db.models import Base
from backend.app.config import validate_environment


# Validate required environment variables
validate_environment()

app = FastAPI(
    title="LLM Safety and Observability Platform",
    version="1.0.0"
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "LLM Safety and Observability Platform is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
