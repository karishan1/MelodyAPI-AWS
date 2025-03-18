from fastapi import APIRouter, HTTPException
from app.utils.dynamodb_cache import store_fingerprint, get_fingerprint
router = APIRouter()

@router.post("/cache")
async def store_fingerprint_route(audio_fingerprint : str,classification : str):
    result = store_fingerprint(audio_fingerprint,classification)
    if "error" in result:
        raise HTTPException(status_code=500,detail=result["error"])
    return result



@router.post("/cache/{fingerprint}")
async def get_fingerprint_route(fingerprint : str):
    result = get_fingerprint(fingerprint)
    if result:
        return result
    raise HTTPException(status_code=500,detail = "Fingerprint not found")