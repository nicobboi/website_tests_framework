from .base_schema import BaseSchema, MetadataBaseSchema, MetadataBaseCreate, MetadataBaseUpdate, MetadataBaseInDBBase
from .msg import Msg
from .token import (
    RefreshTokenCreate,
    RefreshTokenUpdate,
    RefreshToken,
    Token,
    TokenPayload,
    MagicTokenPayload,
    WebToken,
)
from .user import User, UserCreate, UserInDB, UserUpdate, UserLogin
from .emails import EmailContent, EmailValidation
from .totp import NewTOTP, EnableTOTP

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
from .report import ReportBase, ReportCreate, ReportUpdate, ReportScores, ReportDetails
from .tool import ToolBase
from .score import ScoreBase
from .type import TypeBase
from .schedule import ScheduleBase, ScheduleCreate, ScheduleUpdate, ScheduleOutput
