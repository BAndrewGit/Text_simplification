import os
import fasttext
from config.config import HF_HOME

def load_fasttext_model():
    model_path = os.path.join(HF_HOME, "cc.en.300.bin")
    if not os.path.exists(model_path):
        raise FileNotFoundError("Modelul FastText nu a fost găsit. Te rog să-l descarci manual de la: https://fasttext.cc/docs/en/crawl-vectors.html")
    return fasttext.load_model(model_path)