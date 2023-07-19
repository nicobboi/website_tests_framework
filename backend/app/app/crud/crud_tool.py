from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Tool, Type
from app.schemas.tool import ToolBase


class CRUDTool(CRUDBase[Tool, ToolBase, ToolBase]):
    # return a Tool item by its name
    def get_by_name(self, db: Session, *, name: str) -> Tool:
        return db.query(Tool).filter(Tool.name == name).first()
    
    # return the number of tools stored in the db by a given type
    def get_no_tool_by_type(self, db: Session, *, type: str) -> int:
        return len(db.query(Tool).filter(Tool.type.has(name=type)).all())
    
tool = CRUDTool(Tool)