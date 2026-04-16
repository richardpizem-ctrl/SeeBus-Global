from fastapi import APIRouter
from backend.controllers.trips_controller import (
    get_trips_data,
    get_trip,
    get_trips_for_route
)

router = APIRouter()

@router.get("/trips")
def trips():
    return get_trips_data()

@router.get("/trips/{trip_id}")
def trip_by_id(trip_id: str):
    return get_trip(trip_id)

@router.get("/routes/{route_id}/trips")
def trips_by_route(route_id: str):
    return get_trips_for_route(route_id)
