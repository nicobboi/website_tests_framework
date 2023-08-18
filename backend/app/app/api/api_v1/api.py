from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    reports,
    website,
    schedule,
    task
)

api_router = APIRouter()
api_router.include_router(reports.router, prefix="/report", tags=["report"])
api_router.include_router(website.router, prefix="/website", tags=["website"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
