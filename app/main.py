from fastapi import FastAPI
from app.routers.instrument_router import router as instrument_router
from app.routers.detailed_instrument_router import router as detailed_instrument_analysis
from app.routers.genre_router import router as genre_router

app = FastAPI()
app.include_router(instrument_router, prefix="/api", tags=["Instrument Prediction"])
app.include_router(detailed_instrument_analysis, prefix="/api", tags=["Detailed Instrument Prediction"])
app.include_router(genre_router,prefix = "/api", tags=['Genre Prediction'])
