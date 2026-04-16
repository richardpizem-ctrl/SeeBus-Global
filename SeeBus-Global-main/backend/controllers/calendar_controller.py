from backend.services.calendar_service import (
    fetch_calendar,
    fetch_calendar_service
)

def get_calendar():
    return fetch_calendar()

def get_calendar_item(service_id: str):
    return fetch_calendar_service(service_id)
