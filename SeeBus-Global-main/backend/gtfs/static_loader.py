import csv
from pathlib import Path
from typing import Dict, List, Any


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    """
    Načíta CSV súbor a vráti zoznam riadkov ako dict.
    Bezpečne ignoruje neexistujúci súbor.
    """
    rows: List[Dict[str, Any]] = []
    if not path.exists():
        return rows

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def load_routes(gtfs_dir: Path) -> Dict[str, Dict[str, Any]]:
    """
    Načíta routes.txt a vráti dict: route_id -> route_row
    """
    routes_path = gtfs_dir / "routes.txt"
    routes_list = _read_csv(routes_path)

    routes_by_id: Dict[str, Dict[str, Any]] = {}
    for r in routes_list:
        route_id = r.get("route_id")
        if route_id:
            routes_by_id[route_id] = r

    return routes_by_id


def load_trips(gtfs_dir: Path) -> Dict[str, Dict[str, Any]]:
    """
    Načíta trips.txt a vráti dict: trip_id -> trip_row
    """
    trips_path = gtfs_dir / "trips.txt"
    trips_list = _read_csv(trips_path)

    trips_by_id: Dict[str, Dict[str, Any]] = {}
    for t in trips_list:
        trip_id = t.get("trip_id")
        if trip_id:
            trips_by_id[trip_id] = t

    return trips_by_id


def load_stop_times(gtfs_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    """
    Načíta stop_times.txt a vráti dict: trip_id -> zoznam stop_time riadkov
    (zoradené podľa stop_sequence).
    """
    stop_times_path = gtfs_dir / "stop_times.txt"
    st_list = _read_csv(stop_times_path)

    stop_times_by_trip: Dict[str, List[Dict[str, Any]]] = {}

    for st in st_list:
        trip_id = st.get("trip_id")
        if not trip_id:
            continue

        stop_times_by_trip.setdefault(trip_id, []).append(st)

    # zoradenie podľa stop_sequence
    for trip_id, items in stop_times_by_trip.items():
        items.sort(
            key=lambda x: int(x.get("stop_sequence", "0")) if x.get("stop_sequence") else 0
        )

    return stop_times_by_trip
