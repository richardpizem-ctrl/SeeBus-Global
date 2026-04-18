from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from backend.services.event_dispatcher import EventDispatcher
from backend.gtfs.loader import stops, stop_times

router = APIRouter(prefix="/events", tags=["events"])

# Globálny dispatcher pre tento endpoint
dispatcher = EventDispatcher(stops, stop_times)


@router.get("/process")
def process_event(
    vehicle_id: str = Query(...),
    route: str = Query(...),
    lat: float = Query(0.0),
    lon: float = Query(0.0),
    lang: str = Query("en")
):
    """
    Príklad:
    /events/process?vehicle_id=123&route=24&lat=48.73&lon=19.15&lang=sk
    """

    vehicle = {
        "lat": lat,
        "lon": lon,
        "timestamp": 0
    }

    result = dispatcher.process(vehicle_id, vehicle, route, lang)

    if not result:
        return JSONResponse({"event": None})

    return JSONResponse(result)
