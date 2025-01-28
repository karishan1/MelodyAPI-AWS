import shutil
import os
from fastapi import UploadFile, HTTPException

ALLOWED_FILE_TYPES = {".wav", ".mp3", ".flac"}


def save_uploaded_file(file: UploadFile, prefix: str = "temp_") -> str:
    """
    Save the uploaded file locally if it and return the file path.
    """
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed types are: {', '.join(ALLOWED_FILE_TYPES)}")

    file_location = f"{prefix}{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location
