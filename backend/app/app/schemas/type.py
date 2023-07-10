from pydantic import BaseModel


class TypeBase(BaseModel):
    name: str
    type: str

