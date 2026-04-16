from fastapi import APIRouter
from backend.controllers.routes_controller import (
    get_routes,
    get_route
)

router = APIRouter()

@router.get("/routes")
def routes():
    return get_routes()

@router.get("/routes/{route_id}")
def route(route_id: str):
    return get_route(route_id)
