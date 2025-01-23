from fastapi import FastAPI, UploadFile, HTTPException
from app.utils.file_handling import save_uploaded_file
from app.utils.audio_processing import process_audio
from app.utils.predictions import predict_instruments, get_top_predictions
import os

app = FastAPI()
@app.post("/predict/")
async def predict_instrument(file: UploadFile):
    try:
        file_location = save_uploaded_file(file)
        print(f"File saved at: {file_location}")

        embeddings = process_audio(file_location)
        print("Embeddings generated successfully.")

        predictions = predict_instruments(embeddings)
        print("Predictions generated successfully.")

        top_3_predictions = get_top_predictions(predictions)
        print("Top predictions extracted successfully.")

        return {"top_3_predictions": top_3_predictions}
    
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)