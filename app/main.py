from fastapi import FastAPI
from app.routers.instrument_router import router as instrument_router

app = FastAPI()
app.include_router(instrument_router, prefix="/api", tags=["Instrument Prediction"])

@app.get("/")
def home():
    return {"message": "Welcome to the Instrument Prediction API"}