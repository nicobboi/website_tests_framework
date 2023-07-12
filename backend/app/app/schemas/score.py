from pydantic import BaseModel, Field


class ScoreBase(BaseModel):
    name: str = Field(description="Score's name.")
    score: int = Field(description="One of the score of the report.")