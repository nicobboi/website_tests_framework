from pydantic import BaseModel, Field


class TypeBase(BaseModel):
    name: str = Field(description="Type's name.")
    type: str = Field(description="Type of the tool used.")

