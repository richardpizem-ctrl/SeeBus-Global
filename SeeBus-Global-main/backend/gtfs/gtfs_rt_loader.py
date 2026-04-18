import requests
from dataclasses import dataclass

@dataclass
class VehiclePosition:
    trip_id: str | None
    lat: float
    lon: float
    speed: float | None

def load_gtfs_rt(url: str) -> list[VehiclePosition]:
    """
    Načíta GTFS-RT feed (Vehicle Positions) vo formáte protobuf → JSON.
    Očakáva, že server poskytuje JSON (nie protobuf).
    """
    response = requests.get(url, timeout=5)
    data = response.json()

    vehicles = []

    for entity in data.get("entity", []):
        vp = entity.get("vehicle")
        if not vp:
            continue

        trip = vp.get("trip", {})
        position = vp.get("position", {})

        vehicles.append(
            VehiclePosition(
                trip_id=trip.get("trip_id"),
                lat=position.get("latitude"),
                lon=position.get("longitude"),
                speed=position.get("speed")
            )
        )

    return vehicles
