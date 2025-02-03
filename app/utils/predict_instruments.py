import json
import numpy as np
from essentia.standard import TensorflowPredictEffnetDiscogs, TensorflowPredict2D

instrument_names = [
    "accordion", "acousticbassguitar", "acousticguitar", "bass", "beat", "bell", "bongo", "brass", "cello", 
    "clarinet", "classicalguitar", "computer", "doublebass", "drummachine", "drums", "electricguitar", "electricpiano", 
    "flute", "guitar", "harmonica", "harp", "horn", "keyboard", "oboe", "orchestra", "organ", "pad", "percussion", 
    "piano", "pipeorgan", "rhodes", "sampler", "saxophone", "strings", "synthesizer", "trombone", "trumpet", "viola", 
    "violin", "voice"
]

def get_active_time_period(active_time_stamps, min_duration=2):
    if not active_time_stamps:
        return []
    
    active_time_periods = []
    start_time = active_time_stamps[0]

    for i in range(1, len(active_time_stamps)):
        end_time = active_time_stamps[i - 1]
        if active_time_stamps[i] > active_time_stamps[i - 1] + 3:
            if (end_time - start_time) >= min_duration:
                active_time_periods.append([start_time, active_time_stamps[i - 1]])
            start_time = active_time_stamps[i] 

    if (active_time_stamps[-1] - start_time) >= min_duration:
        active_time_periods.append([start_time, active_time_stamps[-1]])

    return active_time_periods



def predict_instruments(embeddings: np.ndarray, threshold=0.3, time_step=1) -> list:

    model = TensorflowPredict2D(
        graphFilename="models/mtg_jamendo_instrument-discogs-effnet-1.pb"
    )

    predictions = model(embeddings)
    predictions = np.array(predictions) 

    instruments_data = []
    num_time_steps = predictions.shape[0]  # Number of time samples

    for i, instrument in enumerate(instrument_names):
        instrument_probs = predictions[:, i]  # Extract probabilities for each instrument

        avg_probability = round(float(np.mean(instrument_probs)), 3)
        max_probability = round(float(np.max(instrument_probs)), 3)


        active_timestamps = []
        for t in range(num_time_steps):
            probability = float(instrument_probs[t])
            if probability >= threshold:
                time_stamp = round(float(t * time_step), 2)  
                active_timestamps.append(time_stamp)

        active_timestamps = get_active_time_period(active_timestamps)

        if active_timestamps:
            instruments_data.append({
                "name": str(instrument),
                "average_probability": avg_probability, 
                "max_probability": max_probability, 
                "active_timestamps": active_timestamps  
            })

    return instruments_data
