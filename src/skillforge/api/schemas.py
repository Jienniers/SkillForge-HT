"""Validated request and response contracts for the frontend API."""

from typing import Literal

from pydantic import BaseModel, Field


class RoadmapRequest(BaseModel):
    language: Literal["python", "javascript", "java", "c++", "go"]


class PracticeRequest(BaseModel):
    language: Literal["python", "javascript", "java", "c++", "go"]
    roadmap: dict[str, list[str]]


class RoadmapPdfRequest(BaseModel):
    roadmap: dict[str, list[str]]


class EvaluationRequest(BaseModel):
    language: Literal["python", "javascript", "java", "c++", "go"]
    question: str = Field(min_length=1)
    code: str = Field(min_length=1)


class EvaluationResponse(BaseModel):
    feedback: str
    correct: bool
    xp_awarded: int


class HintRequest(BaseModel):
    language: Literal["python", "javascript", "java", "c++", "go"]
    question: str = Field(min_length=1)
    level: Literal[1, 2]
    xp: int = Field(ge=0, default=0)
    already_charged: bool = False


class CompletionRequest(BaseModel):
    day_number: int = Field(ge=1, le=30)
    completed_day_count: int = Field(ge=1, le=30)
    first_bonus_given: bool


class LevelRequest(BaseModel):
    xp: int = Field(ge=0)
