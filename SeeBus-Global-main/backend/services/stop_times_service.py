from backend.gtfs_loader.loader import GTFSLoader

loader = GTFSLoader("gtfs")

def fetch_stop_times():
    return loader.load_stop_times()

def fetch_stop_times_for_trip(trip_id: str):
    stop_times = loader.load_stop_times()
    return [s for s in stop_times if s.get("trip_id") == trip_id]
