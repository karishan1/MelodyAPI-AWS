from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predict_moodtheme import get_mood_and_theme_predictions, get_top_predictions
import os

router = APIRouter()
@router.post("/mood-theme")
async def predict_instrument(file: UploadFile):
    file_location = None    
    try:

        file_location = save_uploaded_file(file)

        embeddings = process_audio(file_location)

        predictions = get_mood_and_theme_predictions(embeddings)

        top_3_predictions = get_top_predictions(predictions)

        return {"top_3_predictions": top_3_predictions}

    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)