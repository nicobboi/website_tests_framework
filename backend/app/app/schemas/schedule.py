from pydantic import BaseModel, Field, UUID4
from typing import Union
from datetime import datetime, time


class ScheduleBase(BaseModel):
    """
    Base class for Schedule model validation
    """
    time_info: time     = Field(description="Schedule \'time\' for scheduling a task.")
    days: list[str]     = Field(description="Schedule \'day\' for scheduling a task.")

class ScheduleCreate(ScheduleBase):
    """
    Class to handle creation of Report model
    """
    url: str                = Field(description="Website'url to schedule test tasks.")
    test_types: list[str]   = Field(description="List of test's types to schedule.")

class ScheduleUpdate(BaseModel):
    """
    Class to handle update of Report model
    """
    time_info: Union[time, None]                    = Field(description="Schedule \'time\' for scheduling a task.")
    days: Union[list[str], None]                    = Field(description="Schedule \'day\' for scheduling a task.")
    active: Union[bool, None]                       = Field(description="Schedule status")
    last_time_launched: Union[datetime, None]       = Field(description="Last time the schedule has been launched")



class ScheduleOutput(BaseModel):
    """
    Validation class to return schedule items via API
    """
    id: UUID4                                   = Field(description="Schedule ID")
    url: str                                    = Field(description="Url tested")
    test_type: str                              = Field(description="Test type")
    schedule_info: ScheduleBase                 = Field(description="Crontab info for scheduling")
    active: bool                                = Field(description="Schedule status")
    scheduled_time: datetime                    = Field(description="When this schedule has been created")
    n_run: int                                  = Field(description="How many run has done")
    last_time_launched: Union[datetime, None ]  = Field(description="Last time the schedule has been launched", default = None)

