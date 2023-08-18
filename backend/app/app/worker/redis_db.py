from typing import List, Union
from enum import Enum

from app.core.celery_app import celery_app
from celery.result import AsyncResult


class TaskStatus(str, Enum):
    pending = "PENDING"
    started = "STARTED"
    retry   = "RETRY"
    failure = "FAILURE"
    success = "SUCCESS"

def get_all_tasks(status_filter: Union[TaskStatus, None] = None):
    """
    Return all the task in Redis DB (optional: filtered by status)
    """
    task_results: List[AsyncResult] = []
    for key in celery_app.backend.client.scan_iter("celery-task-meta-*"):
        task_id = str(key).split("celery-task-meta-", 1)[1].replace("'", "")
        task_results.append(AsyncResult(id=task_id, backend=celery_app.backend))

    output = [{
        "task_id": res.id,
        "task_status": res.status,
        "task_kwargs": res.kwargs
    } for res in task_results]

    if status_filter and status_filter in TaskStatus.__members__.values():
        output = [task for task in output if task["task_status"] == status_filter]

    return output

def get_task(task_id: str):
    """
    Return the task by its ID or None if doesn't exist
    """
    task_checked = None
    for task in get_all_tasks():
        if task["task_id"] == task_id:
            task_checked = task
            break

    return task_checked

def get_task_status(task_id: str):
    """
    Return the status of the given task or None if doesn't exist
    """
    task_checked = get_task(task_id=task_id)

    if task_checked: return task_checked["task_status"]
    else: return None

    
