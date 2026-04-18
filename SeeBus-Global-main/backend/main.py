from fastapi import FastAPI

# Status endpoint
from backend.api.routes import get_status

# API endpointy
from backend.api.events_endpoint import router as events_router
from backend.api.stream_endpoint import router as stream_router
from backend.api.language_endpoint import router as language_router

# GTFS dáta
from backend.gtfs.loader import stops, stop_times

# Dispatcher
from backend.services.event_dispatcher import EventDispatcher


app = FastAPI()

# Globálny dispatcher
dispatcher = EventDispatcher(stops, stop_times)


@app.get("/status")
def status():
    return get_status()


# Registrácia API routerov
app.include_router(events_router)
app.include_router(stream_router)
app.include_router(language_router)
