import numpy as np
from essentia.standard import TensorflowPredictEffnetDiscogs, TensorflowPredict2D

instrument_names = [
    "accordion", "acousticbassguitar", "acousticguitar", "bass", "beat", "bell", "bongo", "brass", "cello", 
    "clarinet", "classicalguitar", "computer", "doublebass", "drummachine", "drums", "electricguitar", "electricpiano", 
    "flute", "guitar", "harmonica", "harp", "horn", "keyboard", "oboe", "orchestra", "organ", "pad", "percussion", 
    "piano", "pipeorgan", "rhodes", "sampler", "saxophone", "strings", "synthesizer", "trombone", "trumpet", "viola", 
    "violin", "voice"
]


def predict_instruments(embeddings: np.ndarray, threshold=0.5, time_step=1) -> list:

    model = TensorflowPredict2D(
        graphFilename="models/mtg_jamendo_instrument-discogs-effnet-1.pb"
    )

    predictions = model(embeddings)
    predictions = np.array(predictions) 

    instruments_data = []
    num_time_steps = predictions.shape[0]  # Number of time samples

    for i, instrument in enumerate(instrument_names):
        instrument_probs = predictions[:, i]  # Extract probabilities for each instrument

        avg_probability = float(np.mean(instrument_probs)) 
        max_probability = float(np.max(instrument_probs)) 

        active_timestamps = []
        for t in range(num_time_steps):
            probability = float(instrument_probs[t])
            if probability >= threshold:
                time_stamp = round(float(t * time_step), 2)  
                active_timestamps.append(time_stamp)

        # Only includes instruments that has the active timestamps
        if active_timestamps:
            instruments_data.append({
                "name": str(instrument),
                "average_probability": avg_probability, 
                "max_probability": max_probability, 
                "active_timestamps": active_timestamps  
            })

    return instruments_data