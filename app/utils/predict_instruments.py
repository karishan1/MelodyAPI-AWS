import numpy as np
from essentia.standard import TensorflowPredict2D


# List of instrument names corresponding to the 40 classes
instrument_names = [
    "accordion", "acousticbassguitar", "acousticguitar", "bass", "beat", "bell", "bongo", "brass", "cello", 
    "clarinet", "classicalguitar", "computer", "doublebass", "drummachine", "drums", "electricguitar", "electricpiano", 
    "flute", "guitar", "harmonica", "harp", "horn", "keyboard", "oboe", "orchestra", "organ", "pad", "percussion", 
    "piano", "pipeorgan", "rhodes", "sampler", "saxophone", "strings", "synthesizer", "trombone", "trumpet", "viola", 
    "violin", "voice"
]

def predict_instruments(embeddings: np.ndarray) -> np.ndarray:
    """
    Predict instrument probabilities based on embeddings.
    """
    model = TensorflowPredict2D(
        graphFilename= "models/instrument_classification_models/mtg_jamendo_instrument-discogs-effnet-1.pb"
    )
    predictions = model(embeddings)
    return predictions

def get_top_predictions(predictions: np.ndarray, top_n: int = 3) -> list:
    """
    Calculate the top N predictions with their probabilities.
    """
    average_probabilities = predictions.mean(axis=0)
    top_indices = np.argsort(average_probabilities)[-top_n:][::-1]  
    return [
        {
            "instrument": instrument_names[idx],
            "average_probability": round(float(average_probabilities[idx]), 4)
        }
        for idx in top_indices
    ]
