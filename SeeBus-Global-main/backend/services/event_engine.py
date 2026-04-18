from dataclasses import dataclass
from math import radians, sin, cos, sqrt, atan2

# -----------------------------
# Pomocná funkcia: vzdialenosť
# -----------------------------
def distance_m(lat1, lon1, lat2, lon2):
    R = 6371000  # polomer Zeme v metroch
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


# -----------------------------
# Stav vozidla
# -----------------------------
@dataclass
class VehicleState:
    trip_id: str
    last_state: str | None = None


# -----------------------------
# Event Engine
# -----------------------------
class EventEngine:

    def __init__(self, stops, stop_times):
        self.stops = stops
        self.stop_times = stop_times
        self.vehicle_states = {}  # vehicle_id → VehicleState

    def process_vehicle(self, vehicle):
        """
        vehicle = VehiclePosition(trip_id, lat, lon, speed)
        """
        if not vehicle.trip_id:
            return None

        trip_stops = self.stop_times.get(vehicle.trip_id)
        if not trip_stops:
            return None

        # Najbližšia zastávka
        next_stop = None
        min_dist = 999999

        for st in trip_stops:
            stop = self.stops.get(st.stop_id)
            if not stop:
                continue

            d = distance_m(vehicle.lat, vehicle.lon, stop.lat, stop.lon)
            if d < min_dist:
                min_dist = d
                next_stop = stop

        if not next_stop:
            return None

        # Logika stavov
        speed_kmh = (vehicle.speed or 0) * 3.6

        if 40 < min_dist < 120 and speed_kmh > 3:
            return "ARRIVING", next_stop

        if min_dist < 15 and speed_kmh < 1:
            return "AT_STOP", next_stop

        if min_dist > 20 and speed_kmh > 3:
            return "DEPARTING", next_stop

        return None
