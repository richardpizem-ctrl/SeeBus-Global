from backend.services.trips_service import (
    fetch_trips,
    fetch_trip_by_id,
    fetch_trips_by_route
)

def get_trips_data():
    return fetch_trips()

def get_trip(trip_id: str):
    return fetch_trip_by_id(trip_id)

def get_trips_for_route(route_id: str):
    return fetch_trips_by_route(route_id)
