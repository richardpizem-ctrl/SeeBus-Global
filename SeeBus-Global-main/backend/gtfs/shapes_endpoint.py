from fastapi import APIRouter
from backend.controllers.shapes_controller import (
    get_shapes,
    get_shape
)

router = APIRouter()

@router.get("/shapes")
def shapes():
    return get_shapes()

@router.get("/shapes/{shape_id}")
def shape_points(shape_id: str):
    return get_shape(shape_id)
