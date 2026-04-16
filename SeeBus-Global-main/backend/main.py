
from fastapi import FastAPI
from backend.api.routes import get_status

app = FastAPI()

@app.get("/status")
def status():
    return get_status()
