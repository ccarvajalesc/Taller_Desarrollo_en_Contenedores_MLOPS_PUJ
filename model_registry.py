import os
from predict import load_model

_models_cache = {}
_models_mtime = {}

MODELS_PATH = "models"


def get_model(filename):
    path = os.path.join(MODELS_PATH, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Modelo {filename} no existe aún. Entrena primero en Jupyter."
        )

    mtime = os.path.getmtime(path)

    if filename not in _models_cache or _models_mtime.get(filename) != mtime:
        model, encoders, scaler = load_model(path)   # ⭐ aquí el fix

        _models_cache[filename] = {
            "model": model,
            "encoders": encoders,
            "scaler": scaler
        }
        _models_mtime[filename] = mtime

    return _models_cache[filename]