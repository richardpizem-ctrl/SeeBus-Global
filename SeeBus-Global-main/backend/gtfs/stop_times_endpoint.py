from fastapi import APIRouter
from backend.controllers.stop_times_controller import (
    get_stop_times,
    get_stop_times_by_trip
)

router = APIRouter()

@router.get("/stop_times")
def stop_times():
    return get_stop_times()

@router.get("/stop_times/{trip_id}")
def stop_times_for_trip(trip_id: str):
    return get_stop_times_by_trip(trip_id)
