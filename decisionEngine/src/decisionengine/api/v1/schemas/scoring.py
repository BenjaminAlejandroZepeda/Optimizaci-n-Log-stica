from pydantic import BaseModel
from typing import Optional, List


class ScoringFactorSchema(BaseModel):
    name: str
    value: float
    weight: float
    contribution: float
    description: Optional[str] = None


class ScoringExplainSchema(BaseModel):
    total_score: float
    priority_multiplier: float
    raw_score: float
    factors: List[ScoringFactorSchema]