import csv
from dataclasses import dataclass

@dataclass
class Route:
    route_id: str
    agency_id: str | None
    route_short_name: str | None
    route_long_name: str | None
    route_type: int | None

def load_routes(path: str) -> dict[str, Route]:
    routes = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            route = Route(
                route_id=row["route_id"],
                agency_id=row.get("agency_id"),
                route_short_name=row.get("route_short_name"),
                route_long_name=row.get("route_long_name"),
                route_type=int(row["route_type"]) if row.get("route_type") else None
            )
            routes[route.route_id] = route

    return routes

def get_route(routes: dict[str, Route], route_id: str) -> Route | None:
    return routes.get(route_id)
