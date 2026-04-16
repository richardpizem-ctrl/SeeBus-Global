from pydantic import BaseModel
from typing import Optional

class Trip(BaseModel):
    trip_id: str
    route_id: str
    service_id: str
    shape_id: Optional[str] = None
