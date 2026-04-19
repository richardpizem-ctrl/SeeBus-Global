import asyncio
import json
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

# Jazykové hlásenia (pôvodná logika)
from backend.services.event_dispatcher import EventDispatcher

# Statické GTFS dáta
from backend.gtfs.loader import stops, stop_times

# Nový robustný loader (verzia 2)
from backend.gtfs.gtfs_rt_loader import GTFSRTLoader

# Nové moduly
from backend.gtfs.gtfs_mapper import map_vehicle_basic
from backend.gtfs.event_engine import EventEngine


router = APIRouter(prefix="/stream", tags=["stream"])

# Dispatcher pre jazykové hlásenia
dispatcher = EventDispatcher(stops, stop_times)

# ⭐ PRAHA – GTFS‑RT feed
GTFS_RT_URL = "https://api.golemio.cz/v2/gtfs/vehiclepositions"
GTFS_RT_API_KEY = "SEM_DAJ_TVOJ_API_KLUC"

gtfs_rt = GTFSRTLoader(GTFS_RT_URL, GTFS_RT_API_KEY)
event_engine = EventEngine()


async def event_stream(vehicle_id: str, route: str, lang: str):
    """
    MIGROVANÝ SSE stream:
    - nové GTFS‑RT dáta
    - nové mapovanie
    - nový event engine
    - pôvodné jazykové hlásenia
    """

    while True:
        # 1) Načítame všetky vozidlá
        vehicles = gtfs_rt.fetch_vehicle_positions()

        # 2) Nájdeme konkrétne vozidlo
        v = next((x for x in vehicles if x["vehicle_id"] == vehicle_id), None)

        if v:
            # 3) Namapujeme vozidlo na GTFS statické dáta
            mapped = map_vehicle_basic(
                vehicle=v,
                trips_by_id={},      # zatiaľ prázdne – doplníme v ďalšej verzii
                routes_by_id={},
                stops_by_id=stops,
            )

            # 4) Event engine (ARRIVING / AT_STOP / DEPARTING / IN_TRANSIT)
            event = event_engine.classify_vehicle(mapped)

            # 5) Jazykové hlásenia (pôvodná logika)
            announce = dispatcher.process(vehicle_id, {
                "lat": mapped.lat,
                "lon": mapped.lon,
                "speed": mapped.speed or 0,
                "bearing": mapped.bearing or 0,
                "timestamp": 0
            }, route, lang)

            payload = {
                "vehicle_id": mapped.vehicle_id,
                "route": mapped.route_short_name or route,
                "lat": mapped.lat,
                "lon": mapped.lon,
                "event": event.value,
                "next_stop": mapped.next_stop_name,
                "distance_m": mapped.distance_to_next_stop_m,
                "text": announce.get("text") if announce else "No announcement",
                "state": announce.get("state") if announce else "UNKNOWN",
            }

        else:
            # Vozidlo sa nenašlo
            payload = {
                "vehicle_id": vehicle_id,
                "route": route,
                "lat": None,
                "lon": None,
                "event": "UNKNOWN",
                "next_stop": None,
                "distance_m": None,
                "text": "No data",
                "state": "UNKNOWN",
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
