import logging
from typing import List, Dict, Any, Optional

import requests
from google.transit import gtfs_realtime_pb2


logger = logging.getLogger(__name__)


class GTFSRTLoader:
    def __init__(self, url: str, timeout: float = 5.0):
        self.url = url
        self.timeout = timeout

    def fetch_vehicle_positions(self) -> List[Dict[str, Any]]:
        """
        Načíta GTFS-RT feed a vráti zoznam vozidiel v bezpečnom, validovanom tvare.
        Ak nastane chyba (HTTP, parsovanie, prázdny feed), vráti prázdny zoznam.
        """
        feed = gtfs_realtime_pb2.FeedMessage()

        try:
            response = requests.get(self.url, timeout=self.timeout)
        except requests.RequestException as e:
            logger.warning("GTFS-RT request failed: %s", e)
            return []

        if response.status_code != 200:
            logger.warning("GTFS-RT returned non-200 status: %s", response.status_code)
            return []

        try:
            feed.ParseFromString(response.content)
        except Exception as e:
            logger.warning("Failed to parse GTFS-RT feed: %s", e)
            return []

        vehicles: List[Dict[str, Any]] = []

        for entity in feed.entity:
            if not entity.HasField("vehicle"):
                continue

            vp = entity.vehicle

            # Bezpečné čítanie polí
            vehicle_id: Optional[str] = vp.vehicle.id if vp.vehicle and vp.vehicle.id else None
            trip_id: Optional[str] = vp.trip.trip_id if vp.trip and vp.trip.trip_id else None
            route_id: Optional[str] = vp.trip.route_id if vp.trip and vp.trip.route_id else None

            lat: Optional[float] = None
            lon: Optional[float] = None
            bearing: Optional[float] = None
            speed: Optional[float] = None

            if vp.HasField("position"):
                # Pozícia môže byť čiastočná
                if vp.position.HasField("latitude"):
                    lat = vp.position.latitude
                if vp.position.HasField("longitude"):
                    lon = vp.position.longitude
                if vp.position.HasField("bearing"):
                    bearing = vp.position.bearing
                if vp.position.HasField("speed"):
                    speed = vp.position.speed

            # Ak nemáme ani lat/lon, záznam je prakticky nepoužiteľný
            if lat is None or lon is None:
                logger.debug(
                    "Skipping vehicle without valid position (vehicle_id=%s, trip_id=%s, route_id=%s)",
                    vehicle_id,
                    trip_id,
                    route_id,
                )
                continue

            vehicles.append(
                {
                    "vehicle_id": vehicle_id,
                    "trip_id": trip_id,
                    "route_id": route_id,
                    "lat": lat,
                    "lon": lon,
                    "bearing": bearing,
                    "speed": speed,
                }
            )

        return vehicles
