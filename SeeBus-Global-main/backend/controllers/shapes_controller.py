from backend.services.shapes_service import (
    fetch_shapes,
    fetch_shape_points
)

def get_shapes():
    return fetch_shapes()

def get_shape(shape_id: str):
    return fetch_shape_points(shape_id)
