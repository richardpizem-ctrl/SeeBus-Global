from backend.gtfs_loader.loader import GTFSLoader

loader = GTFSLoader("gtfs")

def fetch_shapes():
    return loader.load_shapes()

def fetch_shape_points(shape_id: str):
    shapes = loader.load_shapes()
    return [s for s in shapes if s.get("shape_id") == shape_id]
