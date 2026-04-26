# DATA_MODEL – SeeBus‑Global

This document describes the internal data structures used by the SeeBus‑Global backend.  
The goal is to keep the model simple, predictable, and aligned with GTFS and GTFS‑RT standards.

---------------------------------------

## 1. Core Entities Overview

The system uses the following primary data models:

- Stop  
- Route  
- Trip  
- VehiclePosition  
- TripUpdate  
- Journey  
- Event  
- ETAResult  

Each model is optimized for fast lookup and real‑time updates.

---------------------------------------

## 2. Stop

Represents a physical bus stop.

stop_id: string  
name: string  
lat: float  
lon: float  
zone: string | null  
platform: string | null  

Example:
{
  "stop_id": "BB1001",
  "name": "Radvaň",
  "lat": 48.7281,
  "lon": 19.1462
}

---------------------------------------

## 3. Route

Represents a bus line.

route_id: string  
name: string  
color: string | null  
text_color: string | null  

Example:
{
  "route_id": "24",
  "name": "Radvaň – Sásová"
}

---------------------------------------

## 4. Trip

Represents a scheduled journey of a route.

trip_id: string  
route_id: string  
stop_sequence: list of stop_id  
service_day: string  
direction: string | null  

Example:
{
  "trip_id": "24_1035",
  "route_id": "24",
  "stop_sequence": ["BB1001", "BB1002", "BB1003"]
}

---------------------------------------

## 5. VehiclePosition (GTFS‑RT)

Represents the real‑time location of a vehicle.

trip_id: string  
lat: float  
lon: float  
timestamp: int  
speed: float | null  
bearing: float | null  

Example:
{
  "trip_id": "24_1035",
  "lat": 48.7290,
  "lon": 19.1500,
  "timestamp": 1714152000
}

---------------------------------------

## 6. TripUpdate (GTFS‑RT)

Represents delays and predicted arrival times.

trip_id: string  
stop_id: string  
arrival_delay: int  
departure_delay: int  
timestamp: int  

Example:
{
  "trip_id": "24_1035",
  "stop_id": "BB1002",
  "arrival_delay": 32
}

---------------------------------------

## 7. ETAResult

Represents the computed ETA for a stop.

route: string  
stop_id: string  
eta_seconds: int  
delay_seconds: int  
status: "on_time" | "delayed" | "cancelled"  

Example:
{
  "route": "24",
  "stop_id": "BB1003",
  "eta_seconds": 145,
  "delay_seconds": 32,
  "status": "delayed"
}

---------------------------------------

## 8. Journey

Represents a user‑initiated journey.

journey_id: string  
origin: stop_id  
destination: stop_id  
route: string  
state: "waiting" | "onboard" | "approaching_destination" | "completed"  
current_stop: stop_id | null  
next_stop: stop_id | null  
eta: int | null  

Example:
{
  "journey_id": "abc123",
  "origin": "BB1001",
  "destination": "BB1003",
  "route": "24",
  "state": "onboard",
  "current_stop": "BB1002",
  "next_stop": "BB1003",
  "eta": 180
}

---------------------------------------

## 9. Event

Represents a system‑generated event for a journey.

type: string  
message: string  
timestamp: int  

Example:
{
  "type": "ARRIVAL_IMMINENT",
  "message": "Your bus arrives in 2 minutes",
  "timestamp": 1714152000
}

---------------------------------------

## 10. Internal Caches

The backend maintains several in‑memory caches:

stops_cache: map<stop_id, Stop>  
routes_cache: map<route_id, Route>  
trips_cache: map<trip_id, Trip>  
vehicle_positions_cache: map<trip_id, VehiclePosition>  
trip_updates_cache: map<trip_id, TripUpdate>  

Caches are refreshed based on CACHE_TTL_SECONDS.

---------------------------------------

## 11. Data Flow Summary

1. Load static GTFS into memory.  
2. Fetch GTFS‑RT updates periodically.  
3. Merge static + real‑time data.  
4. Compute ETA.  
5. Generate journey events.  
6. Serve API responses.

---------------------------------------

# End of file
