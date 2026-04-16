from fastapi import APIRouter
from backend.controllers.calendar_controller import (
    get_calendar,
    get_calendar_item
)

router = APIRouter()

@router.get("/calendar")
def calendar():
    return get_calendar()

@router.get("/calendar/{service_id}")
def calendar_item(service_id: str):
    return get_calendar_item(service_id)
