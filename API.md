API Reference – SeeBus‑Global
This document describes the public API endpoints of SeeBus‑Global.
All responses are JSON.
The API is designed to be simple, predictable, and accessible for both web and mobile clients.

Base URL
/api

1. Journey Management
POST /journey
Starts a new user journey.

Request body:
{
"origin": "stop_id",
"destination": "stop_id",
"route": "bus_line",
"direction": "optional_direction"
}

Response:
{
"journey_id": "uuid",
"status": "initialized",
"message": "Journey created"
}

GET /journey/{journey_id}
Returns the current state of the journey.

Response:
{
"journey_id": "uuid",
"state": "onboard | waiting | approaching_destination | completed",
"current_stop": "stop_id",
"next_stop": "stop_id",
"eta": 180
}

2. Real‑time ETA
GET /eta
Returns ETA for a given route and stop.

Query parameters:
route
stop_id

Example:
/api/eta?route=24&stop_id=BB1234

Response:
{
"route": "24",
"stop_id": "BB1234",
"eta_seconds": 145,
"delay_seconds": 32,
"status": "on_time | delayed | cancelled"
}

3. Events
GET /events/{journey_id}
Returns all active events for the user’s journey.

Response:
{
"journey_id": "uuid",
"events": [
{
"type": "ARRIVAL_IMMINENT",
"message": "Your bus arrives in 2 minutes",
"timestamp": 1714152000
},
{
"type": "AT_STOP",
"message": "You are at stop Radvaň",
"timestamp": 1714152100
}
]
}

4. Stops & Routes
GET /routes
Returns list of available routes.

Response:
{
"routes": [
{"id": "24", "name": "Radvaň – Sásová"},
{"id": "20", "name": "Rooseveltova – Fončorda"}
]
}

GET /stops/{route}
Returns ordered stops for a given route.

Response:
{
"route": "24",
"stops": [
{"stop_id": "BB1001", "name": "Radvaň"},
{"stop_id": "BB1002", "name": "Tulská"},
{"stop_id": "BB1003", "name": "Námestie SNP"}
]
}

5. System Status
GET /status
Returns backend health information.

Response:
{
"status": "ok",
"gtfs_rt": "online",
"last_update": 1714152000
}

6. Error Format
All errors follow a unified structure:

{
"error": true,
"code": "INVALID_REQUEST | NOT_FOUND | INTERNAL_ERROR",
"message": "Human-readable explanation"
}

7. Notes
All timestamps are UNIX epoch (seconds).

All ETA values are in seconds.

All endpoints are stateless.

Future versions may add authentication for personalized profiles.
