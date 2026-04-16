# routes.py
# Hlavné API routy pre SeeBus-Global

from backend.controllers.status_controller import get_status_info

def get_status():
    return get_status_info()
