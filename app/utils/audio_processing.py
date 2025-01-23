from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs
import numpy as np
import os


def process_audio(file_path: str) -> np.ndarray:
    """
    Load and process the audio file to extract embeddings.
    """
    model_path = os.path.join(os.getcwd(), "models", "discogs-effnet-bs64-1.pb")

    print(f"Resolved model path: {model_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    else:
        print("Models file not found.", model_path)

    audio = MonoLoader(filename=file_path, sampleRate=16000, resampleQuality=4)()
    embedding_model = TensorflowPredictEffnetDiscogs(
        graphFilename = model_path,
        output="PartitionedCall:1"
    )
    embeddings = embedding_model(audio)
    return embeddings