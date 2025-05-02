from fastapi import FastAPI, status
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request


from app.routers.instrument_router import router as instrument_router
from app.routers.genre_router import router as genre_router
from app.routers.moodtheme_router import router as moodtheme_router
from app.utils.dynamodb_cache import init_db 


app = FastAPI(
    title="MelodyAPI",
    description="An API for genre, mood, and instrument classification of audio files."
)
@app.get("/")
def root():
    return {"message" : "MelodyAPI"}

origins = ["*"]  # Allow requests from any origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.on_event("startup")
def startup_event():
    print("Creating table")
    init_db()  # Ensure DynamoDB table exists

app.include_router(instrument_router, prefix="/api", tags=["Instrument Prediction"])
app.include_router(genre_router,prefix = "/api", tags=['Genre Prediction'])
app.include_router(moodtheme_router,prefix = "/api", tags=['Mood and Theme Prediction'])

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "The endpoint you are trying to reach does not exist. Please check the URL and try again."}
    )

lambda_handler = Mangum(app)

