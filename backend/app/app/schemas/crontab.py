from pydantic import BaseModel


class CrontabBase(BaseModel):
    info: str

class CrontabCreate(CrontabBase):
    url: str
    test_types: list[str]