from fastapi import APIRouter
from backend.controllers.stops_controller import (
    get_stops,
    get_stop
)

router = APIRouter()

@router.get("/stops")
def stops():
    return get_stops()

@router.get("/stops/{stop_id}")
def stop(stop_id: str):
    return get_stop(stop_id)
