from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predict_instruments import predict_instruments
import os

router = APIRouter()

@router.post("/detect-instruments/")
async def detailed_instrument_analysis(file: UploadFile):
    file_location = None    
    try:

        file_location = save_uploaded_file(file)
        embeddings = process_audio(file_location)
        instrument_analysis = predict_instruments(embeddings)
        return {"predictions": instrument_analysis}


    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)


