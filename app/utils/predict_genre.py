import numpy as np
from essentia.standard import TensorflowPredict2D, TensorflowPredictMusiCNN

genres = [
    "60s", "70s", "80s", "90s", "acidjazz", "alternative", "alternativerock", "ambient", "atmospheric",
    "blues", "bluesrock", "bossanova", "breakbeat", "celtic", "chanson", "chillout", "choir", "classical",
    "classicrock", "club", "contemporary", "country", "dance", "darkambient", "darkwave", "deephouse", "disco",
    "downtempo", "drumnbass", "dub", "dubstep", "easylistening", "edm", "electronic", "electronica", "electropop",
    "ethno", "eurodance", "experimental", "folk", "funk", "fusion", "groove", "grunge", "hard", "hardrock", 
    "hiphop", "house", "idm", "improvisation", "indie", "industrial", "instrumentalpop", "instrumentalrock",
    "jazz", "jazzfusion", "latin", "lounge", "medieval", "metal", "minimal", "newage", "newwave", "orchestral",
    "pop", "popfolk", "poprock", "postrock", "progressive", "psychedelic", "punkrock", "rap", "reggae", "rnb",
    "rock", "rocknroll", "singersongwriter", "soul", "soundtrack", "swing", "symphonic", "synthpop", "techno",
    "trance", "triphop", "world", "worldfusion"
]

def get_genre_predictions(embeddings: np.ndarray) -> np.ndarray:
    """
    Predict genre probabilities based on embeddings.
    """
    model = TensorflowPredict2D(
        graphFilename= "models/genre_classification_models/mtg_jamendo_genre-discogs-effnet-1.pb"
        
    )
    
    predictions = model(embeddings)
    return predictions
def get_top_predictions(predictions: np.ndarray, top_n: int = 4) -> list:
    """
    Calculate the top N predictions with their probabilities.
    """
    average_probabilities = predictions.mean(axis=0)
    top_indices = np.argsort(average_probabilities)[-top_n:][::-1]
    return [
        {
            "Genre": genres[idx],
            "average_probability": round(float(average_probabilities[idx]), 4)
        }
        for idx in top_indices
    ]
