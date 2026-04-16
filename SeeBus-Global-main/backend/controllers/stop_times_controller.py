# stop_times_controller.py
# Controller pre GTFS stop_times

from backend.gtfs_loader.loader import GTFSLoader

GTFS_PATH = "gtfs_data"
loader = GTFSLoader(GTFS_PATH)

def get_stop_times_data():
    data = loader.load_stop_times()
    return {
        "message": "GTFS stop_times loaded",
        "count": len(data),
        "data": data
    }
