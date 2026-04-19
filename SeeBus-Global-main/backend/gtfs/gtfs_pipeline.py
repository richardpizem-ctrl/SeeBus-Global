from typing import List, Dict, Any

from .gtfs_rt_loader import GTFSRTLoader
from .gtfs_mapper import map_vehicles_batch, MappedVehicle


class GTFSPipeline:
    """
    Pipeline vrstva:
    - zavolá GTFS-RT loader
    - zavolá mapper
    - vráti kompletne pripravené vozidlá
    """

    def __init__(
        self,
        rt_url: str,
        trips_by_id: Dict[str, Dict[str, Any]],
        routes_by_id: Dict[str, Dict[str, Any]],
        stops_by_id: Dict[str, Dict[str, Any]],
    ):
        self.loader = GTFSRTLoader(rt_url)
        self.trips_by_id = trips_by_id
        self.routes_by_id = routes_by_id
        self.stops_by_id = stops_by_id

    def load_and_map_positions(self) -> List[MappedVehicle]:
        """
        Kompletný pipeline krok:
        1) načíta raw GTFS-RT dáta
        2) namapuje ich na statické GTFS
        3) vráti zoznam MappedVehicle objektov
        """
        raw_positions = self.loader.fetch_vehicle_positions()

        mapped = map_vehicles_batch(
            vehicles=raw_positions,
            trips_by_id=self.trips_by_id,
            routes_by_id=self.routes_by_id,
            stops_by_id=self.stops_by_id,
        )

        return mapped
