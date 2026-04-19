from typing import List
from enum import Enum

from .gtfs_mapper import MappedVehicle


class VehicleEvent(Enum):
    ARRIVING = "arriving"
    AT_STOP = "at_stop"
    DEPARTING = "departing"
    IN_TRANSIT = "in_transit"


class EventEngine:
    """
    Jednoduchý event engine pre SeeBus-Global.
    Na základe vzdialenosti a rýchlosti určí stav vozidla.
    """

    ARRIVING_DISTANCE = 80.0      # m
    AT_STOP_DISTANCE = 30.0       # m
    STOP_SPEED_THRESHOLD = 1.0    # m/s

    def classify_vehicle(self, mv: MappedVehicle) -> VehicleEvent:
        """
        Určí stav jedného vozidla.
        """
        dist = mv.distance_to_next_stop_m
        speed = mv.speed or 0.0

        if dist is None:
            return VehicleEvent.IN_TRANSIT

        # AT_STOP
        if dist < self.AT_STOP_DISTANCE and speed < self.STOP_SPEED_THRESHOLD:
            return VehicleEvent.AT_STOP

        # ARRIVING
        if dist < self.ARRIVING_DISTANCE and speed < 5.0:
            return VehicleEvent.ARRIVING

        # DEPARTING
        if dist < self.ARRIVING_DISTANCE and speed >= 5.0:
            return VehicleEvent.DEPARTING

        return VehicleEvent.IN_TRANSIT

    def classify_batch(self, vehicles: List[MappedVehicle]) -> List[tuple]:
        """
        Prejde všetky vozidlá a vráti zoznam (vehicle, event).
        """
        results = []
        for mv in vehicles:
            event = self.classify_vehicle(mv)
            results.append((mv, event))
        return results
