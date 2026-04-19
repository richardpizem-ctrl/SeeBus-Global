import asyncio
import json
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

# Jazykové hlásenia
from backend.services.event_dispatcher import EventDispatcher

# Pôvodné stops + stop_times (pre jazykové hlásenia)
from backend.gtfs.loader import stops, stop_times

# GTFS‑RT loader
from backend.gtfs.gtfs_rt_loader import GTFSRTLoader

# Mapovanie + event engine
from backend.gtfs.gtfs_mapper import map_vehicle_basic
from backend.gtfs.event_engine import EventEngine

# GTFS CACHE – routes, trips, stop_times
from backend.gtfs.gtfs_cache import get_routes, get_trips, get_stop_times


router = APIRouter(prefix="/stream", tags=["stream"])

# Dispatcher pre jazykové hlásenia
dispatcher = EventDispatcher(stops, stop_times)

# ⭐ PRAHA – GTFS‑RT feed
GTFS_RT_URL = "https://api.golemio.cz/v2/gtfs/vehiclepositions"
GTFS_RT_API_KEY = "SEM_DAJ_TVOJ_API_KLUC"

gtfs_rt = GTFSRTLoader(GTFS_RT_URL, GTFS_RT_API_KEY)
event_engine = EventEngine()

# ⭐ STATIC GTFS – cez CACHE
routes_by_id = get_routes()
trips_by_id = get_trips()
stop_times_by_trip = get_stop_times()


async def event_stream_all(lang: str):
    """
    SSE stream pre VŠETKY vozidlá naraz.
    Každú sekundu:
    - načíta všetky GTFS‑RT vozidlá
    - namapuje ich na GTFS statické dáta
    - vypočíta ETA + DELAY
    - určí event (ARRIVING / AT_STOP / DEPARTING / IN_TRANSIT)
    - vygeneruje jazykové hlásenia
    - pošle pole vozidiel
    """

    while True:
        vehicles = gtfs_rt.fetch_vehicle_positions()
        result_list = []

        for v in vehicles:
            mapped = map_vehicle_basic(
                vehicle=v,
                trips_by_id=trips_by_id,
                routes_by_id=routes_by_id,
                stops_by_id=stops,
                stop_times_by_trip=stop_times_by_trip,
            )

            event = event_engine.classify_vehicle(mapped)

            announce = dispatcher.process(mapped.vehicle_id, {
                "lat": mapped.lat,
                "lon": mapped.lon,
                "speed": mapped.speed or 0,
                "bearing": mapped.bearing or 0,
                "timestamp": 0
            }, mapped.route_short_name or "", lang)

            result_list.append({
                "vehicle_id": mapped.vehicle_id,
                "route": mapped.route_short_name,
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
            })

        payload = {"vehicles": result_list}

        yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
        await asyncio.sleep(1)


@router.get("/events/all")
async def stream_events_all(
    lang: str = Query("en")
):
    generator = event_stream_all(lang)
    return StreamingResponse(generator, media_type="text/event-stream")
