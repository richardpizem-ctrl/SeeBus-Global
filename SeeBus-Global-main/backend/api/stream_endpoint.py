import asyncio
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from backend.services.event_dispatcher import EventDispatcher
from backend.gtfs.loader import stops, stop_times

router = APIRouter(prefix="/stream", tags=["stream"])

# Globálny dispatcher
dispatcher = EventDispatcher(stops, stop_times)


async def event_stream(vehicle_id, route, lang):
    """
    Generuje SSE stream s jazykovými hláseniami.
    """

    while True:
        # Simulované vozidlo (v reálnej verzii príde z GTFS-RT)
        vehicle = {
            "lat": 0,
            "lon": 0,
            "timestamp": 0
        }

        result = dispatcher.process(vehicle_id, vehicle, route, lang)

        if result:
            yield f"data: {result}\n\n"

        await asyncio.sleep(1)


@router.get("/events")
async def stream_events(
    vehicle_id: str = Query(...),
    route: str = Query(...),
    lang: str = Query("en")
):
    """
    SSE endpoint:
    /stream/events?vehicle_id=123&route=24&lang=sk
    """

    generator = event_stream(vehicle_id, route, lang)
    return StreamingResponse(generator, media_type="text/event-stream")
