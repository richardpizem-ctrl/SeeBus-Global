import csv
from dataclasses import dataclass

@dataclass
class Stop:
    stop_id: str
    stop_name: str
    lat: float
    lon: float

def load_stops(path: str) -> dict[str, Stop]:
    stops = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop = Stop(
                stop_id=row["stop_id"],
                stop_name=row["stop_name"],
                lat=float(row["stop_lat"]),
                lon=float(row["stop_lon"]),
            )
            stops[stop.stop_id] = stop
    return stops

def get_stop_by_id(stops: dict[str, Stop], stop_id: str) -> Stop | None:
    return stops.get(stop_id)
