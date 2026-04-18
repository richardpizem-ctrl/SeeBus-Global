from flask import Blueprint, request, jsonify
from backend.services.event_dispatcher import EventDispatcher

events_bp = Blueprint("events", __name__)

# Dispatcher budeš inicializovať v main.py
dispatcher: EventDispatcher = None


@events_bp.route("/events/process", methods=["GET"])
def process_event():
    """
    API endpoint:
    /api/events/process?vehicle_id=123&route=24&lang=sk
    """

    global dispatcher

    vehicle_id = request.args.get("vehicle_id")
    route_short_name = request.args.get("route")
    lang = request.args.get("lang", "en")

    if not vehicle_id or not route_short_name:
        return jsonify({"error": "Missing parameters"}), 400

    # Simulované vozidlo (v reálnej verzii príde z GTFS-RT)
    vehicle = {
        "lat": float(request.args.get("lat", 0)),
        "lon": float(request.args.get("lon", 0)),
        "timestamp": 0
    }

    result = dispatcher.process(vehicle_id, vehicle, route_short_name, lang)

    if not result:
        return jsonify({"event": None})

    return jsonify(result)
