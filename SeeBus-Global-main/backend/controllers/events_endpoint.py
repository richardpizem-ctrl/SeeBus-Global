from fastapi import APIRouter
from pydantic import BaseModel

from ..services.event_dispatcher import EventDispatcher

router = APIRouter()


# -----------------------------
# Model vstupu
# -----------------------------
class VehicleInput(BaseModel):
    vehicle_id: str
    trip_id: str
    lat: float
    lon: float
    speed: float
    route_short_name: str


# -----------------------------
# Endpoint
# -----------------------------
@router.post("/api/events/process")
async def process_event(data: VehicleInput):

    # Vytvoríme objekt VehiclePosition (rovnaký ako používaš v engine)
    class VehiclePosition:
        def __init__(self, trip_id, lat, lon, speed):
            self.trip_id = trip_id
            self.lat = lat
            self.lon = lon
            self.speed = speed

    vehicle = VehiclePosition(
        data.trip_id,
        data.lat,
        data.lon,
        data.speed
    )

    # Dispatcher potrebuje stops a stop_times
    # (v tvojom projekte ich máš načítané v main.py)
    from ..gtfs.loader import stops, stop_times

    dispatcher = EventDispatcher(stops, stop_times)

    result = dispatcher.process(
        data.vehicle_id,
        vehicle,
        data.route_short_name
    )

    if not result:
        return {"event": None}

    return {"event": result}
