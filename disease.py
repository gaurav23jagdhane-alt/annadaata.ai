# Loads the trained CNN and predicts disease from a leaf image.
import os
import numpy as np
from PIL import Image

CONFIDENCE_LIMIT = 0.70  # below this -> refer to expert (from your PPT: confidence-based assistance)
_model = None
_classes = None


def model_ready():
    return os.path.exists("disease_model.keras") and os.path.exists("class_names.txt")


def predict(pil_image):
    global _model, _classes
    import tensorflow as tf
    if _model is None:
        _model = tf.keras.models.load_model("disease_model.keras")
        _classes = open("class_names.txt").read().split("\n")
    img = pil_image.convert("RGB").resize((160, 160))
    x = np.expand_dims(np.array(img, dtype="float32"), 0)
    probs = _model.predict(x, verbose=0)[0]
    i = int(np.argmax(probs))
    return _classes[i], float(probs[i])
