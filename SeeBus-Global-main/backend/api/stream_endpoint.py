import asyncio
import json
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from backend.services.event_dispatcher import EventDispatcher
from backend.gtfs.loader import stops, stop_times
from backend.gtfs.gtfs_rt_loader import GTFSRTLoader

router = APIRouter(prefix="/stream", tags=["stream"])

# Dispatcher pre jazykové hlásenia
dispatcher = EventDispatcher(stops, stop_times)

# ⭐ PRAHA – GTFS‑RT feed
GTFS_RT_URL = "https://api.golemio.cz/v2/gtfs/vehiclepositions"
GTFS_RT_API_KEY = "SEM_DAJ_TVOJ_API_KLUC"

gtfs_rt = GTFSRTLoader(GTFS_RT_URL, GTFS_RT_API_KEY)


async def event_stream(vehicle_id, route, lang):
    """
    SSE stream s reálnymi GTFS‑RT dátami + jazykové hlásenia.
    """

    while True:
        vehicles = gtfs_rt.fetch_vehicle_positions()

        # Nájdeme konkrétne vozidlo
        v = next((x for x in vehicles if x["vehicle_id"] == vehicle_id), None)

        if v:
            vehicle = {
                "lat": v["lat"],
                "lon": v["lon"],
                "speed": v.get("speed", 0),
                "bearing": v.get("bearing", 0),
                "timestamp": 0
            }
        else:
            vehicle = {
                "lat": None,
                "lon": None,
                "timestamp": 0
            }

        result = dispatcher.process(vehicle_id, vehicle, route, lang)

        payload = {
            "text": result.get("text") if result else "No announcement",
            "state": result.get("state") if result else "UNKNOWN",
            "lat": vehicle["lat"],
            "lon": vehicle["lon"]
        }

        yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

        await asyncio.sleep(1)


@router.get("/events")
async def stream_events(
    vehicle_id: str = Query(...),
    route: str = Query(...),
    lang: str = Query("en")
):
    generator = event_stream(vehicle_id, route, lang)
    return StreamingResponse(generator, media_type="text/event-stream")
