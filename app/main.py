from fastapi import FastAPI
#from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from app.routers.instrument_router import router as instrument_router
from app.routers.genre_router import router as genre_router
from app.routers.moodtheme_router import router as moodtheme_router
from app.utils.dynamodb_cache import init_db 
from app.routers.cache_router import router as cache_router  



app = FastAPI()
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
    init_db()  # Ensure DynamoDB table exists

app.include_router(instrument_router, prefix="/api", tags=["Instrument Prediction"])
app.include_router(genre_router,prefix = "/api", tags=['Genre Prediction'])
app.include_router(moodtheme_router,prefix = "/api", tags=['Mood and Theme Prediction'])
app.include_router(cache_router, prefix="/api", tags=["Caching"])



#lambda_handler = Mangum(app)

