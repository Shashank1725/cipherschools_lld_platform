from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Problem(Base):
    __tablename__ = "problems"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    level: Mapped[str] = mapped_column(String(30), nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    constraints: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="problem", cascade="all, delete-orphan")

class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    problem_id: Mapped[str] = mapped_column(ForeignKey("problems.id"), nullable=False, index=True)
    learner_id: Mapped[str] = mapped_column(String(80), nullable=False, default="demo-learner", index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="submitted")
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    classes: Mapped[list] = mapped_column(JSON, nullable=False)
    relationships_text: Mapped[str] = mapped_column(Text, nullable=False)
    patterns: Mapped[str] = mapped_column(Text, nullable=False, default="")
    tradeoffs: Mapped[str] = mapped_column(Text, nullable=False, default="")
    edge_cases: Mapped[str] = mapped_column(Text, nullable=False, default="")
    feedback: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    problem: Mapped[Problem] = relationship(back_populates="attempts")
