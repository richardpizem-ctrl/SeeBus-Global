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
    distance_to_next_stop_m: Optional[float] = None


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Jednoduchý výpočet vzdialenosti medzi dvoma bodmi v metroch.
    Stačí na základné mapovanie vozidla k najbližšej zastávke.
    """
    R = 6371000.0  # polomer Zeme v metroch

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def map_vehicle_basic(
    vehicle: Dict[str, Any],
    trips_by_id: Dict[str, Dict[str, Any]],
    routes_by_id: Dict[str, Dict[str, Any]],
    stops_by_id: Dict[str, Dict[str, Any]],
) -> MappedVehicle:
    """
    Základné mapovanie:
    - doplní informácie o linke (route_short_name, route_long_name)
    - nájde najbližšiu zastávku (bez ohľadu na poradie v tripe – to príde v ďalšej verzii)
    """
    vehicle_id = vehicle.get("vehicle_id")
    trip_id = vehicle.get("trip_id")
    route_id = vehicle.get("route_id")
    lat = vehicle["lat"]
    lon = vehicle["lon"]
    bearing = vehicle.get("bearing")
    speed = vehicle.get("speed")

    route_short_name: Optional[str] = None
    route_long_name: Optional[str] = None

    # 1) Mapovanie route_id → routes.txt
    if route_id and route_id in routes_by_id:
        route = routes_by_id[route_id]
        route_short_name = route.get("route_short_name")
        route_long_name = route.get("route_long_name")

    # 2) Najbližšia zastávka (hrubý základ – bez poradia v tripe)
    next_stop_id: Optional[str] = None
    next_stop_name: Optional[str] = None
    distance_to_next_stop_m: Optional[float] = None

    min_dist: Optional[float] = None

    for stop_id, stop in stops_by_id.items():
        stop_lat = stop.get("stop_lat")
        stop_lon = stop.get("stop_lon")
        if stop_lat is None or stop_lon is None:
            continue

        dist = haversine_distance_m(lat, lon, stop_lat, stop_lon)

        if min_dist is None or dist < min_dist:
            min_dist = dist
            next_stop_id = stop_id
            next_stop_name = stop.get("stop_name")
            distance_to_next_stop_m = dist

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
        distance_to_next_stop_m=distance_to_next_stop_m,
    )


def map_vehicles_batch(
    vehicles: List[Dict[str, Any]],
    trips_by_id: Dict[str, Dict[str, Any]],
    routes_by_id: Dict[str, Dict[str, Any]],
    stops_by_id: Dict[str, Dict[str, Any]],
) -> List[MappedVehicle]:
    """
    Batch verzia – prejde všetky vozidlá z GTFS-RT loadera a namapuje ich
    na základné statické GTFS dáta.
    """
    mapped: List[MappedVehicle] = []

    for v in vehicles:
        mv = map_vehicle_basic(
            vehicle=v,
            trips_by_id=trips_by_id,
            routes_by_id=routes_by_id,
            stops_by_id=stops_by_id,
        )
        mapped.append(mv)

    return mapped
