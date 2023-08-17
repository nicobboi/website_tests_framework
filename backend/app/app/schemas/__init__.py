from .base_schema import BaseSchema, MetadataBaseSchema, MetadataBaseCreate, MetadataBaseUpdate, MetadataBaseInDBBase

# Add here import custom schemas
from .website import (
    WebsiteBase,
    WebsiteCreate,
    WebsiteUpdate,
    WebsiteRun,
    AllWebsiteScores,
    WebsiteReportsScores,
    TestTypes
)
from .report import (
    ReportBase, 
    ReportCreate, 
    ReportUpdate, 
    ReportTool,
    ReportScore,
    ReportScoresOutput, 
    ReportDetails
)
from .schedule import ScheduleBase, ScheduleCreate, ScheduleUpdate, ScheduleOutput
