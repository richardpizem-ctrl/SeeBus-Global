import csv
from dataclasses import dataclass

@dataclass
class StopTime:
    trip_id: str
    stop_id: str
    stop_sequence: int

def load_stop_times(path: str) -> dict[str, list[StopTime]]:
    stop_times_by_trip = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            st = StopTime(
                trip_id=row["trip_id"],
                stop_id=row["stop_id"],
                stop_sequence=int(row["stop_sequence"])
            )

            if st.trip_id not in stop_times_by_trip:
                stop_times_by_trip[st.trip_id] = []

            stop_times_by_trip[st.trip_id].append(st)

    # Každý trip zoradíme podľa poradia zastávok
    for trip_id in stop_times_by_trip:
        stop_times_by_trip[trip_id].sort(key=lambda x: x.stop_sequence)

    return stop_times_by_trip

def get_stops_for_trip(stop_times_by_trip: dict[str, list[StopTime]], trip_id: str):
    return stop_times_by_trip.get(trip_id, [])
