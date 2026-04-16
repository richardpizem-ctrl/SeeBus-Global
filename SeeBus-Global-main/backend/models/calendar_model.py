from pydantic import BaseModel
from typing import Optional

class Calendar(BaseModel):
    service_id: str
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int
    sunday: int
    start_date: str
    end_date: str
