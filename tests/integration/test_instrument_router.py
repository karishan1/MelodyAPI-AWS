import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_instrument_predict_endpoint():
    transport = ASGITransport(app=app)
    test_audio_file = "audio _files/harp sound.mp3"
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with open(test_audio_file, "rb") as f:
            response = await client.post(
                "/api/instrument-predict/3",
                files={"file": ("harp sound.mp3", f, "audio/wav")}
            )
    
    assert response.status_code == 200
    json_data = response.json()
    assert "top_n_predictions" in json_data
    assert isinstance(json_data["top_n_predictions"], list)
    assert len(json_data["top_n_predictions"]) == 3