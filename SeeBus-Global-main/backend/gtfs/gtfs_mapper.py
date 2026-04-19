from dataclasses import dataclass
from typing import Optional, Dict, List, Any
import math


@dataclass
class MappedVehicle:
    vehicle_id: Optional[str]
    trip_id: Optional[str]
    route_id: Optional[str]
    lat: float
    lon: float
    bearing: Optional[float]
    speed: Optional[float]

    route_short_name: Optional[str] = None
    route_long_name: Optional[str] = None

    next_stop_id: Optional[str] = None
    next_stop_name: Optional[str] = None
    next_stop_sequence: Optional[int] = None
    distance_to_next_stop_m: Optional[float] = None


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_next_stop_by_trip(
    lat: float,
    lon: float,
    trip_id: Optional[str],
    stop_times_by_trip: Dict[str, List[Dict[str, Any]]],
    stops_by_id: Dict[str, Dict[str, Any]],
) -> tuple[Optional[str], Optional[str], Optional[int], Optional[float]]:
    """
    Nájde najbližšiu BUDÚCU zastávku podľa stop_sequence.
    Toto je presné mapovanie podľa GTFS tripu.
    """
    if not trip_id:
        return None, None, None, None

    if trip_id not in stop_times_by_trip:
        return None, None, None, None

    best_stop_id = None
    best_stop_name = None
    best_sequence = None
    best_dist = None

    for st in stop_times_by_trip[trip_id]:
        stop_id = st.get("stop_id")
        seq = int(st.get("stop_sequence", 0))

        stop = stops_by_id.get(stop_id)
        if not stop:
            continue

        stop_lat = stop.get("stop_lat")
        stop_lon = stop.get("stop_lon")
        if stop_lat is None or stop_lon is None:
            continue

        dist = haversine_distance_m(lat, lon, stop_lat, stop_lon)

        # Vyberáme najbližšiu budúcu zastávku
        if best_dist is None or dist < best_dist:
            best_dist = dist
            best_stop_id = stop_id
            best_stop_name = stop.get("stop_name")
            best_sequence = seq

    return best_stop_id, best_stop_name, best_sequence, best_dist


def map_vehicle_basic(
    vehicle: Dict[str, Any],
    trips_by_id: Dict[str, Dict[str, Any]],
    routes_by_id: Dict[str, Dict[str, Any]],
    stops_by_id: Dict[str, Dict[str, Any]],
    stop_times_by_trip: Dict[str, List[Dict[str, Any]]],
) -> MappedVehicle:

    vehicle_id = vehicle.get("vehicle_id")
    trip_id = vehicle.get("trip_id")
    route_id = vehicle.get("route_id")
    lat = vehicle["lat"]
    lon = vehicle["lon"]
    bearing = vehicle.get("bearing")
    speed = vehicle.get("speed")

    route_short_name = None
    route_long_name = None

    # ROUTE → routes.txt
    if route_id and route_id in routes_by_id:
        route = routes_by_id[route_id]
        route_short_name = route.get("route_short_name")
        route_long_name = route.get("route_long_name")

    # STOP-SEQUENCE MAPPING (KROK 9)
    next_stop_id, next_stop_name, next_seq, dist = find_next_stop_by_trip(
        lat, lon, trip_id, stop_times_by_trip, stops_by_id
    )

    return MappedVehicle(
        vehicle_id=vehicle_id,
        trip_id=trip_id,
        route_id=route_id,
        lat=lat,
        lon=lon,
        bearing=bearing,
        speed=speed,
        route_short_name=route_short_name,
        route_long_name=route_long_name,
        next_stop_id=next_stop_id,
        next_stop_name=next_stop_name,
        next_stop_sequence=next_seq,
        distance_to_next_stop_m=dist,
    )


def map_vehicles_batch(
    vehicles: List[Dict[str, Any]],
    trips_by_id: Dict[str, Dict[str, Any]],
    routes_by_id: Dict[str, Dict[str, Any]],
    stops_by_id: Dict[str, Dict[str, Any]],
    stop_times_by_trip: Dict[str, List[Dict[str, Any]]],
) -> List[MappedVehicle]:

    mapped: List[MappedVehicle] = []

    for v in vehicles:
        mv = map_vehicle_basic(
            vehicle=v,
            trips_by_id=trips_by_id,
            routes_by_id=routes_by_id,
            stops_by_id=stops_by_id,
            stop_times_by_trip=stop_times_by_trip,
        )
        mapped.append(mv)

    return mapped
