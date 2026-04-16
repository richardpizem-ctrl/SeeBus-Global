from pydantic import BaseModel

class ShapePoint(BaseModel):
    shape_id: str
    shape_pt_lat: float
    shape_pt_lon: float
    shape_pt_sequence: int
