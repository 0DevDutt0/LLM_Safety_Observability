from sqlalchemy import Column, Integer, Text, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class LLMLog(Base):
    __tablename__ = "llm_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(Text)

    prompt = Column(Text)
    response = Column(Text)
    latency_ms = Column(Float)
    injection_detected = Column(Boolean)

    hallucination_score = Column(Float, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    response_tokens = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

