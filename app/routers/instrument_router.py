from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predictions import predict_instruments, get_top_predictions
from app.utils.dynamodb_cache import generate_fingerprint, get_fingerprint, store_fingerprint
import os

router = APIRouter()
@router.post("/predict/{predictions_num}")
async def predict_instrument(predictions_num: int, file: UploadFile):
    file_location = None    
    try:

        file_location = save_uploaded_file(file)

        fingerprint = generate_fingerprint(file_location)
        if not fingerprint:
            raise HTTPException(status_code=500, detail="Failed to generate fingerprint")

        # Check if prediction exists in cache
        cached_result = get_fingerprint(fingerprint,"instrument",predictions_num)
        if cached_result:
            print("✅ Cache HIT: Returning cached instrument prediction")
            return {"top_genre_predictions": cached_result["classification"]}
        
        print("❌ Cache MISS: Processing audio for genre prediction")

        embeddings = process_audio(file_location)

        predictions = predict_instruments(embeddings)

        top_3_predictions = get_top_predictions(predictions,predictions_num)
        print("Storing fingerprint")
        store_fingerprint(fingerprint,"instrument",top_3_predictions, predictions_num)
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