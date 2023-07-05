from pydantic import BaseModel


class ToolBase(BaseModel):
    name: str
    type: str



