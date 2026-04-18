from dataclasses import dataclass
from math import radians, sin, cos, sqrt, atan2

# -----------------------------------
# Výpočet vzdialenosti v metroch
# -----------------------------------
def distance_m(lat1, lon1, lat2, lon2):
    R = 6371000  # polomer Zeme v metroch
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


# -----------------------------------
# Stav vozidla (pamäť)
# -----------------------------------
@dataclass
class VehicleState:
    last_state: str | None = None
    last_stop_id: str | None = None
    last_distance: float | None = None
    missed_stops: set | None = None


# -----------------------------------
# Event Engine
# -----------------------------------
class EventEngine:

    def __init__(self, stops, stop_times):
        self.stops = stops
        self.stop_times = stop_times
        self.vehicle_states = {}  # vehicle_id → VehicleState

    def process_vehicle(self, vehicle_id, vehicle):
        """
        vehicle = VehiclePosition(trip_id, lat, lon, speed)
        """
        if not vehicle.trip_id:
            return None

        trip_stops = self.stop_times.get(vehicle.trip_id)
        if not trip_stops:
            return None

        # Nájdeme najbližšiu zastávku
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

        # Prevod rýchlosti
        speed_kmh = (vehicle.speed or 0) * 3.6

        # Načítame pamäť vozidla
        vs = self.vehicle_states.get(vehicle_id, VehicleState(missed_stops=set()))

        # -----------------------------
        # MISSED detection
        # -----------------------------
        if vs.last_distance is not None:
            # Vozidlo sa vzďaľuje od zastávky
            if min_dist > vs.last_distance + 10:  # +10m tolerancia
                # A nebolo AT_STOP
                if vs.last_state != "AT_STOP":
                    # A ešte sme túto zastávku nehlásili ako MISSED
                    if next_stop.stop_id not in vs.missed_stops:
                        vs.missed_stops.add(next_stop.stop_id)
                        self.vehicle_states[vehicle_id] = vs
                        return "MISSED", next_stop

        # -----------------------------
        # Logika stavov
        # -----------------------------
        if 40 < min_dist < 120 and speed_kmh > 3:
            state = "ARRIVING"
        elif min_dist < 15 and speed_kmh < 1:
            state = "AT_STOP"
        elif min_dist > 20 and speed_kmh > 3:
            state = "DEPARTING"
        else:
            # Uložíme vzdialenosť aj keď nie je stav
            vs.last_distance = min_dist
            self.vehicle_states[vehicle_id] = vs
            return None

        # -----------------------------
        # Pamäť – aby sa stav neopakoval
        # -----------------------------
        if vs.last_state == state and vs.last_stop_id == next_stop.stop_id:
            vs.last_distance = min_dist
            self.vehicle_states[vehicle_id] = vs
            return None  # nič nové

        # Uložíme nový stav
        vs.last_state = state
        vs.last_stop_id = next_stop.stop_id
        vs.last_distance = min_dist
        self.vehicle_states[vehicle_id] = vs

        return state, next_stop
