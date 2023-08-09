from pydantic import BaseModel, Field, UUID4
from typing import Union
from datetime import datetime


class ScheduleBase(BaseModel):
    """
    """
    min: int    = Field(description="Schedule \'min\' for scheduling a task.")
    hour: int   = Field(description="Schedule \'hour\' for scheduling a task.")
    day: int    = Field(description="Schedule \'day\' for scheduling a task.")


class ScheduleCreate(ScheduleBase):
    """
    """
    url: str                = Field(description="Website'url to schedule test tasks.")
    test_types: list[str]   = Field(description="List of test's types to schedule.")

class ScheduleUpdate(ScheduleBase):
    """
    """
    active: bool    = Field(description="")



class ScheduleOutput(BaseModel):
    """
    Validation class to return schedule items via API
    """
    id: UUID4                                   = Field(description="")
    url: str                                    = Field(description="")
    test_type: str                              = Field(description="")
    schedule_info: ScheduleBase                 = Field(description="")
    active: bool                                = Field(description="")
    scheduled_time: datetime                    = Field(description="")
    n_run: int                                  = Field(description="")
    last_time_launched: Union[datetime, None ]  = Field(description="", default = None)

