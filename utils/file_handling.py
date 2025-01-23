import shutil
from fastapi import UploadFile

def save_uploaded_file(file: UploadFile, prefix: str = "temp_") -> str:
    """
    Save the uploaded file locally and return the file path.
    """
    file_location = f"{prefix}{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location
