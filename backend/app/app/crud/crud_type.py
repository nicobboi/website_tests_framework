from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Type
from app.schemas.type import TypeBase


class CRUDType(CRUDBase[Type, TypeBase, TypeBase]):
    # return a Type item by its name
    def get_by_name(self, db: Session, *, name: str) -> Type:
        return db.query(Type).filter(Type.name == name).first()
    
type = CRUDType(Type)