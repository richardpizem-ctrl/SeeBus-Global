from backend.gtfs_loader.loader import GTFSLoader

loader = GTFSLoader("gtfs")

def fetch_stops():
    return loader.load_stops()

def fetch_stop(stop_id: str):
    stops = loader.load_stops()
    for s in stops:
        if s.get("stop_id") == stop_id:
            return s
    return None
