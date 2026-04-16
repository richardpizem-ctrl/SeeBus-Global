from backend.gtfs_loader.loader import GTFSLoader

loader = GTFSLoader("gtfs")

def fetch_routes():
    return loader.load_routes()

def fetch_route(route_id: str):
    routes = loader.load_routes()
    for r in routes:
        if r.get("route_id") == route_id:
            return r
    return None
