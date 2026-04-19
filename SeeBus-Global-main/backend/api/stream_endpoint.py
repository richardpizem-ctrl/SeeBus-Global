import asyncio
import json
from pathlib import Path
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

# Jazykové hlásenia (pôvodná logika)
from backend.services.event_dispatcher import EventDispatcher

# Statické GTFS dáta (pôvodné stops + stop_times)
from backend.gtfs.loader import stops, stop_times

# Nový robustný loader (verzia 2)
from backend.gtfs.gtfs_rt_loader import GTFSRTLoader

# Nové moduly
from backend.gtfs.gtfs_mapper import map_vehicle_basic
from backend.gtfs.event_engine import EventEngine

# Static loader – nový modul
from backend.gtfs.static_loader import load_routes, load_trips, load_stop_times


router = APIRouter(prefix="/stream", tags=["stream"])

# Dispatcher pre jazykové hlásenia
dispatcher = EventDispatcher(stops, stop_times)

# ⭐ PRAHA – GTFS‑RT feed
GTFS_RT_URL = "https://api.golemio.cz/v2/gtfs/vehiclepositions"
GTFS_RT_API_KEY = "SEM_DAJ_TVOJ_API_KLUC"

gtfs_rt = GTFSRTLoader(GTFS_RT_URL, GTFS_RT_API_KEY)
event_engine = EventEngine()

# ⭐ STATIC GTFS – načítanie routes, trips, stop_times
GTFS_DIR = Path("backend/gtfs/static")  # uprav podľa tvojej štruktúry

routes_by_id = load_routes(GTFS_DIR)
trips_by_id = load_trips(GTFS_DIR)
stop_times_by_trip = load_stop_times(GTFS_DIR)


async def event_stream(vehicle_id: str, route: str, lang: str):
    """
    MIGROVANÝ SSE stream:
    - nové GTFS‑RT dáta
    - nové mapovanie (routes, trips, stops)
    - nový event engine
    - ETA + DELAY
    - pôvodné jazykové hlásenia
    """

    while True:
        # 1) Načítame všetky vozidlá
        vehicles = gtfs_rt.fetch_vehicle_positions()

        # 2) Nájdeme konkrétne vozidlo
        v = next((x for x in vehicles if x["vehicle_id"] == vehicle_id), None)

        if v:
            # 3) Namapujeme vozidlo na GTFS statické dáta + ETA + DELAY
            mapped = map_vehicle_basic(
                vehicle=v,
                trips_by_id=trips_by_id,
                routes_by_id=routes_by_id,
                stops_by_id=stops,
                stop_times_by_trip=stop_times_by_trip,
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

                # STOP-SEQUENCE + ETA + DELAY
                "next_stop": mapped.next_stop_name,
                "next_stop_sequence": mapped.next_stop_sequence,
                "distance_m": mapped.distance_to_next_stop_m,
                "eta_seconds": mapped.eta_seconds,
                "scheduled_arrival": mapped.scheduled_arrival,
                "delay_seconds": mapped.delay_seconds,

                # Jazykové hlásenia
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
                "next_stop_sequence": None,
                "distance_m": None,
                "eta_seconds": None,
                "scheduled_arrival": None,
                "delay_seconds": None,

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
