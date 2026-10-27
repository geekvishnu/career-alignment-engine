from typing import Literal

from pydantic import BaseModel, Field


class SkillIn(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    level: Literal["beginner", "intermediate", "advanced"] = "intermediate"


class AnalyzeRequest(BaseModel):
    skills: list[SkillIn] = Field(min_length=1, max_length=60)
    interests: list[str] = Field(default_factory=list, max_length=10)
    cgpa: float | None = Field(default=None, ge=0, le=10)    # shown as context only; never used in scoring
    target_career: str | None = None


class JDRequest(BaseModel):
    text: str = Field(min_length=20, max_length=20000)
    skills: list[SkillIn] = Field(default_factory=list, max_length=60)
