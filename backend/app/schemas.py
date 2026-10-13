from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator

class ClassInput(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    responsibility: str = Field(min_length=8, max_length=500)

    @field_validator("name", "responsibility")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Value cannot be blank")
        return value.strip()

class AttemptCreate(BaseModel):
    problem_id: str = Field(min_length=1, max_length=60)
    learner_id: str = Field(default="demo-learner", min_length=1, max_length=80)
    classes: list[ClassInput] = Field(min_length=2, max_length=20)
    relationships_text: str = Field(min_length=12, max_length=3000)
    patterns: str = Field(default="", max_length=1500)
    tradeoffs: str = Field(min_length=12, max_length=2000)
    edge_cases: str = Field(min_length=12, max_length=2000)

    @field_validator("problem_id")
    @classmethod
    def valid_problem_id(cls, value: str) -> str:
        return value.strip()

    @field_validator("relationships_text", "tradeoffs", "edge_cases")
    @classmethod
    def meaningful_text(cls, value: str) -> str:
        if len(value.strip()) < 12:
            raise ValueError("Please provide at least 12 non-whitespace characters")
        return value.strip()

class ProblemOut(BaseModel):
    id: str
    title: str
    level: str
    estimated_minutes: int
    summary: str
    requirements: list[str]
    constraints: list[str]
    model_config = ConfigDict(from_attributes=True)

class AttemptOut(BaseModel):
    id: int
    problem_id: str
    learner_id: str
    status: str
    submitted_at: datetime
    classes: list[dict]
    relationships_text: str
    patterns: str
    tradeoffs: str
    edge_cases: str
    feedback: dict | None
    score: int | None
    error_message: str | None
    model_config = ConfigDict(from_attributes=True)
