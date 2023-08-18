from fastapi import APIRouter

from app.worker import redis_db


router = APIRouter()

@router.get("/get-all")
def get_all():
    """
    Get all tasks in the Redis DB
    """
    return redis_db.get_all_tasks()

@router.get("/status")
def get_task(task_id: str):
    """
    Get task status by its ID
    """
    return redis_db.get_task(task_id=task_id)