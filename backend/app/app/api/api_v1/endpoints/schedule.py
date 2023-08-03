from typing import Any
from datetime import datetime
from pydantic import UUID4

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

@router.get("/get-all-active")
def get_all_active_schedules(*, db: Session = Depends(deps.get_db)):
    """
    Get all schedules
    """

    return crud.crontab.get_all_active(db=db)