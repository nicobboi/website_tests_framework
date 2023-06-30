from pydantic import BaseModel


class ScoreBase(BaseModel):
    name: str
    score: int