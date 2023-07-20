from pydantic import BaseModel, Field


class ToolBase(BaseModel):
    name: str = Field(description="Tool's name.")
    type: str = Field(description="Tool's type.")
