from fastapi import FastAPI

from app.api.routes.v1 import aggregator, auth, heartbeats

app = FastAPI(title="Enigmatica API")

app.include_router(auth.router, tags=["V1"])
app.include_router(heartbeats.router, tags=["V1"])
app.include_router(aggregator.router, tags=["V1"])


@app.get("/")
def root():
    return {"message": "Enigmatica backend is running"}
