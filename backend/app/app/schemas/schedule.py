from pydantic import BaseModel, Field


class ScheduleBase(BaseModel):
    info: str = Field(description="Schedule info for scheduling a task.")


class ScheduleCreate(ScheduleBase):
    url: str = Field(description="Website'url to schedule test tasks.")
    test_types: list[str] = Field(description="List of test's types to schedule.")

