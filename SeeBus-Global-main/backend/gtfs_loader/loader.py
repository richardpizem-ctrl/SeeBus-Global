# loader.py
# GTFS Loader – načítanie a parsovanie GTFS .txt súborov

import csv
import os

class GTFSLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_file(self, filename):
        path = os.path.join(self.folder_path, filename)
        if not os.path.exists(path):
            return []

        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return list(reader)
    def load_stops(self):
        return self.load_file("stops.txt")
    def load_routes(self):
        return self.load_file("routes.txt")
    def load_trips(self):
        return self.load_file("trips.txt")
    def load_stop_times(self):
        return self.load_file("stop_times.txt")
    def load_shapes(self):
        return self.load_file("shapes.txt")
    def load_calendar(self):
        return self.load_file("calendar.txt")
