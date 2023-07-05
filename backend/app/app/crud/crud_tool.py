from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Tool
from app.schemas.tool import ToolBase


class CRUDTool(CRUDBase[Tool, ToolBase, ToolBase]):
    # return a Tool item by its name
    def get_by_name(self, db: Session, *, name: str) -> Tool:
        return db.query(Tool).filter(Tool.name == name).first()
    
tool = CRUDTool(Tool)