import requests
from google.transit import gtfs_realtime_pb2

class GTFSRTLoader:
    def __init__(self, url: str):
        self.url = url

    def fetch_vehicle_positions(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(self.url)

        if response.status_code != 200:
            return []

        feed.ParseFromString(response.content)

        vehicles = []
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                vp = entity.vehicle
                vehicles.append({
                    "vehicle_id": vp.vehicle.id,
                    "trip_id": vp.trip.trip_id,
                    "route_id": vp.trip.route_id,
                    "lat": vp.position.latitude,
                    "lon": vp.position.longitude,
                    "bearing": vp.position.bearing,
                    "speed": vp.position.speed
                })

        return vehicles
