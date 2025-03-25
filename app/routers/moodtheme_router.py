from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predict_moodtheme import get_mood_and_theme_predictions, get_top_predictions
from app.utils.dynamodb_cache import generate_fingerprint, get_fingerprint, store_fingerprint

import os

router = APIRouter()
@router.post("/mood-theme-predict")
async def predict_instrument(file: UploadFile):
    file_location = None    
    try:

        file_location = save_uploaded_file(file)
        fingerprint = generate_fingerprint(file_location)
        if not fingerprint:
            raise HTTPException(status_code=500, detail="Failed to generate fingerprint")

        # Check if prediction exists in cache
        cached_result = get_fingerprint(fingerprint,"mood_theme")
        if cached_result:
            print("✅ Cache HIT: Returning cached mood-theme prediction")
            return {"top_3_predictions": cached_result["classification"]}
        
        print("❌ Cache MISS: Processing audio for mood-theme prediction")

        embeddings = process_audio(file_location)

        predictions = get_mood_and_theme_predictions(embeddings)

        top_3_predictions = get_top_predictions(predictions)
        print("Storing fingerprint")
        store_fingerprint(fingerprint,"mood_theme",top_3_predictions)
        print("Fingerprint stored in cache")      

        return {"top_3_predictions": top_3_predictions}

    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)