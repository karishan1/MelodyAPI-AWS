from fastapi import APIRouter, UploadFile, HTTPException, status, File
from typing import Optional

from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predict_genre import get_genre_predictions, get_top_predictions
from app.utils.dynamodb_cache import generate_fingerprint, get_fingerprint, store_fingerprint

import os

MAX_FILE_SIZE_MB = 50 # Max file size in MB
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024 # Max file size in Bytes

# Initialise API router
router = APIRouter()

# POST endpoint for genre prediction
@router.post("/genre-predict/{predictions_num}",
            summary="Predict genre from uploaded audio",
            description="""
                Upload an audio file and receive the top N predicted genres from a machine learning model.

                - Supported formats : .mp3, .wav, .flac
                - Returns json format
                - Max file size : 50MB
            """)

async def predict_genre(predictions_num: int, file: Optional[UploadFile] = File(None)):
    file_location = None    
    try:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file uploaded. Please upload a valid audio file (mp3, wav, flac)."
            )
        
        # Checks file size 
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail = f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB."
            )
        # Rewinds file after checking
        await file.seek(0)

        # Saves file to /tmp directory
        file_location = save_uploaded_file(file)

        # Generates unique fingerprint for audio file 
        fingerprint = generate_fingerprint(file_location)
        if not fingerprint:
            raise HTTPException(status_code=500, detail="Failed to generate fingerprint")

        # Attempts to retrieve cached result for this specific response
        cached_result = get_fingerprint(fingerprint,"genre",predictions_num)
        # Returns cached result if available
        if cached_result:
            print("CACHE HIT")
            return {"top_genre_predictions": cached_result["classification"]}
        print("CACHE MISS")
        # Extract audio embeddings
        embeddings = process_audio(file_location)

        # Perform genre classification
        predictions = get_genre_predictions(embeddings) 
        
        # Retrieve top N predictions
        result = get_top_predictions(predictions,predictions_num)

        # Stores fingerprint in cache for retrieval later on 
        store_fingerprint(fingerprint,"genre",result,predictions_num)

        # Return final prediction
        return result
        
        
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)