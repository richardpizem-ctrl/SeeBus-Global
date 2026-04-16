from pydantic import BaseModel

class StopTime(BaseModel):
    trip_id: str
    arrival_time: str
    departure_time: str
    stop_id: str
    stop_sequence: int
