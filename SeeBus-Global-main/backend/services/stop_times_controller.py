from backend.services.stop_times_service import (
    fetch_stop_times,
    fetch_stop_times_for_trip
)

def get_stop_times():
    return fetch_stop_times()

def get_stop_times_by_trip(trip_id: str):
    return fetch_stop_times_for_trip(trip_id)
