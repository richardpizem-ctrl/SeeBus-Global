from backend.services.routes_service import (
    fetch_routes,
    fetch_route
)

def get_routes():
    return fetch_routes()

def get_route(route_id: str):
    return fetch_route(route_id)
