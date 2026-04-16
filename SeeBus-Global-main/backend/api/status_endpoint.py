# status_endpoint.py
# Endpoint pre získanie statusu API

from backend.controllers.status_controller import get_status_info

def status():
    return get_status_info()
