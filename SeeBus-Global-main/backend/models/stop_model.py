from pydantic import BaseModel
from typing import Optional

class Stop(BaseModel):
    stop_id: str
    stop_name: Optional[str] = None
    stop_lat: float
    stop_lon: float
