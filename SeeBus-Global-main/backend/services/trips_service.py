from backend.gtfs_loader.loader import GTFSLoader

loader = GTFSLoader("gtfs")

def fetch_trips():
    return loader.load_trips()

def fetch_trip_by_id(trip_id: str):
    trips = loader.load_trips()
    for t in trips:
        if t.get("trip_id") == trip_id:
            return t
    return None

def fetch_trips_by_route(route_id: str):
    trips = loader.load_trips()
    return [t for t in trips if t.get("route_id") == route_id]
