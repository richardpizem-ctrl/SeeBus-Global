from backend.services.stops_service import (
    fetch_stops,
    fetch_stop
)

def get_stops():
    return fetch_stops()

def get_stop(stop_id: str):
    return fetch_stop(stop_id)
