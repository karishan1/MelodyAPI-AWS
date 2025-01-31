import numpy as np
from essentia.standard import TensorflowPredictEffnetDiscogs, TensorflowPredict2D

instrument_names = [
    "accordion", "acousticbassguitar", "acousticguitar", "bass", "beat", "bell", "bongo", "brass", "cello", 
    "clarinet", "classicalguitar", "computer", "doublebass", "drummachine", "drums", "electricguitar", "electricpiano", 
    "flute", "guitar", "harmonica", "harp", "horn", "keyboard", "oboe", "orchestra", "organ", "pad", "percussion", 
    "piano", "pipeorgan", "rhodes", "sampler", "saxophone", "strings", "synthesizer", "trombone", "trumpet", "viola", 
    "violin", "voice"
]

def smooth_timestamps(time_stamps, min_duration = 2):
    if not time_stamps:
        return []
    
    filtered = []
    temp_group = [time_stamps[0]]

    for i in range(1, len(time_stamps)):
        if time_stamps[i] == time_stamps[i - 1] + 1:
            temp_group.append(time_stamps[i])
        else:
            if len(temp_group) >= min_duration:
                filtered.extend(temp_group)
            temp_group = [time_stamps[i]]

    if len(temp_group) >= min_duration:
        filtered.extend(temp_group)

    return filtered

def get_segment_starts(active_time_stamps):

    if not active_time_stamps:
        return []
    
    segment_starts = [active_time_stamps[0]]

    for i in range(1, len(active_time_stamps)):
        if active_time_stamps[i] >= active_time_stamps[i - 1] + 3:  # If there's a gap, start a new segment
            segment_starts.append(active_time_stamps[i])

    return segment_starts
    

def predict_instruments(embeddings: np.ndarray, threshold=0.2, time_step=1) -> list:

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
        
        active_timestamps = smooth_timestamps(active_timestamps, min_duration=3)
        active_timestamps = get_segment_starts(active_timestamps)


        # Only includes instruments that has the active timestamps
        if active_timestamps:
            instruments_data.append({
                "name": str(instrument),
                "average_probability": avg_probability, 
                "max_probability": max_probability, 
                "active_timestamps": active_timestamps  
            })

    return instruments_data