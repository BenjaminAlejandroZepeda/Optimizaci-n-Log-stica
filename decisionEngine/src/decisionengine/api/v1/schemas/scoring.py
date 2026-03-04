
from pydantic import BaseModel
from typing import Optional


class ScoringFactorSchema(BaseModel):
    name: str
    value: float
    weight: float
    contribution: float
    description: Optional[str] = None
