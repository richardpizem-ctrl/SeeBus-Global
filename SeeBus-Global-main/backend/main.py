from fastapi import FastAPI

# Status endpoint
from backend.api.routes import get_status

# API endpointy
from backend.api.events_endpoint import router as events_router
from backend.api.stream_endpoint import router as stream_router


app = FastAPI()


@app.get("/status")
def status():
    return get_status()


# Registrácia API routerov
app.include_router(events_router)
app.include_router(stream_router)
