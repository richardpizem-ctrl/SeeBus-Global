from fastapi import APIRouter
from backend.gtfs.loader import stops, stop_times

router = APIRouter(prefix="/stops", tags=["stops"])

@router.get("/{trip_id}")
def get_stops_for_trip(trip_id: str):
    """
    Vráti všetky zastávky pre daný trip_id v správnom poradí.
    """

    if trip_id not in stop_times:
        return []

    stop_list = stop_times[trip_id]

    result = []
    for entry in stop_list:
        stop_id = entry["stop_id"]
        sequence = entry["stop_sequence"]

        stop_info = stops.get(stop_id)
        if not stop_info:
            continue

        result.append({
            "stop_id": stop_id,
            "name": stop_info["stop_name"],
            "lat": stop_info["stop_lat"],
            "lon": stop_info["stop_lon"],
            "sequence": sequence
        })

    result.sort(key=lambda x: x["sequence"])
    return result
