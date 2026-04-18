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

# GTFS‑RT feed (sem vložíš URL dopravného podniku)
GTFS_RT_URL = "https://URL_TVOJHO_GTFS_RT_FEEDU"
gtfs_rt = GTFSRTLoader(GTFS_RT_URL)


async def event_stream(vehicle_id, route, lang):
    """
    SSE stream s reálnymi GTFS‑RT dátami + jazykové hlásenia.
    """

    while True:
        # 1) Načítaj reálne polohy vozidiel
        vehicles = gtfs_rt.fetch_vehicle_positions()

        # 2) Nájdeme konkrétne vozidlo
        v = next((x for x in vehicles if x["vehicle_id"] == vehicle_id), None)

        if v:
            # Reálne GPS súradnice
            vehicle = {
                "lat": v["lat"],
                "lon": v["lon"],
                "speed": v.get("speed", 0),
                "bearing": v.get("bearing", 0),
                "timestamp": 0
            }
        else:
            # Vozidlo sa nenašlo – fallback
            vehicle = {
                "lat": None,
                "lon": None,
                "timestamp": 0
            }

        # 3) Jazykové hlásenie cez EventDispatcher
        result = dispatcher.process(vehicle_id, vehicle, route, lang)

        # 4) Spojíme GTFS‑RT + hlásenie
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
    """
    SSE endpoint:
    /stream/events?vehicle_id=123&route=24&lang=sk
    """
    generator = event_stream(vehicle_id, route, lang)
    return StreamingResponse(generator, media_type="text/event-stream")
