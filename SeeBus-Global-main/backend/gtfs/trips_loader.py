import csv
from dataclasses import dataclass

@dataclass
class Trip:
    trip_id: str
    route_id: str
    service_id: str
    trip_headsign: str | None = None

def load_trips(path: str) -> dict[str, Trip]:
    trips = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip = Trip(
                trip_id=row["trip_id"],
                route_id=row["route_id"],
                service_id=row["service_id"],
                trip_headsign=row.get("trip_headsign")
            )
            trips[trip.trip_id] = trip

    return trips

def get_trip(trips: dict[str, Trip], trip_id: str) -> Trip | None:
    return trips.get(trip_id)
