import numpy as np
from essentia.standard import TensorflowPredict2D, TensorflowPredictMusiCNN

mood_themes = [
    "action", "adventure", "advertising", "background", "ballad", "calm", "children", "christmas",
    "commercial", "cool", "corporate", "dark", "deep", "documentary", "drama", "dramatic", "dream",
    "emotional", "energetic", "epic", "fast", "film", "fun", "funny", "game", "groovy", "happy",
    "heavy", "holiday", "hopeful", "inspiring", "love", "meditative", "melancholic", "melodic",
    "motivational", "movie", "nature", "party", "positive", "powerful", "relaxing", "retro",
    "romantic", "sad", "sexy", "slow", "soft", "soundscape", "space", "sport", "summer",
    "trailer", "travel", "upbeat", "uplifting"
]


def get_mood_and_theme_predictions(embeddings: np.ndarray) -> np.ndarray:
    """
    Predict genre probabilities based on embeddings.
    """
    model = TensorflowPredict2D(
        graphFilename= "models/moodtheme_classification_models/mtg_jamendo_moodtheme-discogs-effnet-1.pb"
        
    )
    
    predictions = model(embeddings)
    return predictions

def get_top_predictions(predictions: np.ndarray, top_n: int = 4) -> list:
    """
    Calculate the top N predictions with their probabilities.
    """
    print(predictions)
    average_probabilities = predictions.mean(axis=0)
    top_indices = np.argsort(average_probabilities)[-top_n:][::-1]
    return [
        {
            "Genre": mood_themes[idx],
            "average_probability": round(float(average_probabilities[idx]), 4)
        }
        for idx in top_indices
    ]
