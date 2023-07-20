from pydantic import BaseModel, Field


class CrontabBase(BaseModel):
    info: str = Field(description="Crontab info for scheduling a task.")


class CrontabCreate(CrontabBase):
    url: str = Field(description="Website'url to schedule test tasks.")
    test_types: list[str] = Field(description="List of test's types to schedule.")
