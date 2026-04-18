from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

from ..services.event_dispatcher import EventDispatcher
from ..gtfs.loader import stops, stop_times


router = APIRouter()


# -----------------------------------
# SSE generator
# -----------------------------------
async def event_stream(dispatcher, vehicle_id, route_short_name, get_vehicle_position):
    """
    dispatcher: EventDispatcher
    vehicle_id: ID vozidla
    route_short_name: napr. "21"
    get_vehicle_position: funkcia, ktorá vráti VehiclePosition
    """

    while True:
        vehicle = get_vehicle_position()

        result = dispatcher.process(vehicle_id, vehicle, route_short_name)

        if result:
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"

        await asyncio.sleep(1)  # stream každú sekundu


# -----------------------------------
# Endpoint /api/events/stream
# -----------------------------------
@router.get("/api/events/stream")
async def stream_events(vehicle_id: str, route_short_name: str):
    """
    Real-time SSE stream pre frontend.
    Frontend dostáva eventy každú sekundu.
    """

    dispatcher = EventDispatcher(stops, stop_times)

    # Importujeme model VehiclePosition z event endpointu
    from ..api.events_endpoint import VehicleInput

    # Tu si frontend musí dodať aktuálnu polohu vozidla.
    # Zatiaľ spravíme placeholder funkciu, ktorú neskôr nahradíme.
    def get_vehicle_position():
        # Sem neskôr doplníme reálne dáta z MHD API
        return VehicleInput(
            vehicle_id=vehicle_id,
            trip_id="",
            lat=0.0,
            lon=0.0,
            speed=0.0,
            route_short_name=route_short_name
        )

    return StreamingResponse(
        event_stream(dispatcher, vehicle_id, route_short_name, get_vehicle_position),
        media_type="text/event-stream"
    )
