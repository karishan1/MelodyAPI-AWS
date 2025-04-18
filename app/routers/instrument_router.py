from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predict_instruments import predict_instruments, get_top_predictions
from app.utils.dynamodb_cache import generate_fingerprint, get_fingerprint, store_fingerprint
import os

# Initialize API router 
router = APIRouter()

# POST endpoint for instrument prediction
@router.post("/instrument-predict/{predictions_num}")
async def predict_instrument(predictions_num: int, file: UploadFile):
    file_location = None    
    try:
        # Saves file to /tmp directory
        file_location = save_uploaded_file(file)

        # Generates unique fingerprint for audio file 
        fingerprint = generate_fingerprint(file_location)
        if not fingerprint:
            raise HTTPException(status_code=500, detail="Failed to generate fingerprint")

        # Attempts to retrieve cached result for this specific response
        cached_result = get_fingerprint(fingerprint,"instrument",predictions_num)
        # Returns cached result if available
        if cached_result:
            return {"top_genre_predictions": cached_result["classification"]}
        
        # Extract audio embeddings
        embeddings = process_audio(file_location)

        # Perform instrument classification
        predictions = predict_instruments(embeddings)

        # Retrieve top N predictions 
        top_n_predictions = get_top_predictions(predictions,predictions_num)

        # Stores fingerprint in cache for retrieval later on 
        store_fingerprint(fingerprint,"instrument",top_n_predictions, predictions_num)

        # Return final prediction
        return {"top_n_predictions": top_n_predictions}
        
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)