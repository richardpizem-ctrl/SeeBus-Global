from backend.gtfs_loader.loader import GTFSLoader

loader = GTFSLoader("gtfs")

def fetch_calendar():
    return loader.load_calendar()

def fetch_calendar_service(service_id: str):
    calendar = loader.load_calendar()
    for c in calendar:
        if c.get("service_id") == service_id:
            return c
    return None
