from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs
import numpy as np
import os


def process_audio(file_path: str) -> np.ndarray:
    """
    Load and process the audio file to extract embeddings.
    """
    model_path = os.path.abspath("models/discogs-effnet-bs64-1.pb")
    if os.path.exists(model_path):
        print("Model file found at:", model_path)
    else:
        print("Model file not found.")

    audio = MonoLoader(filename=file_path, sampleRate=16000, resampleQuality=4)()
    embedding_model = TensorflowPredictEffnetDiscogs(
        graphFilename="models/discogs-effnet-bs64-1.pb",
        output="PartitionedCall:1"
    )
    embeddings = embedding_model(audio)
    return embeddings