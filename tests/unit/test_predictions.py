from app.utils.predict_instruments import get_top_predictions as get_top_instrument_predictions
from app.utils.predict_genre import get_top_predictions as get_top_genre_predictions
from app.utils.predict_moodtheme import get_top_predictions as get_top_moodtheme_predictions
import numpy as np

def test_get_top_instrument_predictions():
    predictions = np.array([
        [0.1, 0.2, 0.3],
        [0.2, 0.3, 0.5]
    ])
    result = get_top_instrument_predictions(predictions, 2)

    assert len(result) == 2
    assert result[0]["average_probability"] >= result[1]["average_probability"]
    assert "instrument" in result[0]

def test_get_top_genre_predictions():
    predictions = np.array([
        [0.1, 0.2, 0.3],
        [0.2, 0.3, 0.5]
    ])
    result = get_top_genre_predictions(predictions, 2)

    assert len(result) == 2
    assert result[0]["average_probability"] >= result[1]["average_probability"]
    assert "genre" in result[0]

def test_get_top_moodtheme_predictions():
    predictions = np.array([
        [0.1, 0.2, 0.3],
        [0.2, 0.3, 0.5]
    ])
    result = get_top_moodtheme_predictions(predictions, 2)

    assert len(result) == 2
    assert result[0]["average_probability"] >= result[1]["average_probability"]
    assert "mood_theme" in result[0]