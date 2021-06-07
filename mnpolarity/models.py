import os
import time
import joblib
from os.path import join
from glob import glob

# [local]
from .classes import *
from .config import config


class BaseModel:
    def __init__(self) -> None:
        pass

    def load(self) -> None:
        raise NotImplementedError

    def predict(self, text: str) -> dict:
        raise NotImplementedError

    @staticmethod
    def validate_path(path: str, filename: str) -> None:
        if not os.path.isfile(join(path, filename)):
            raise Exception(
                f"Could not find a `{filename}` inside `{path}`")

    @staticmethod
    def pred2label(pred: int) -> str:
        if pred == NEGATIVE:
            return "NEGATIVE"
        elif pred == POSITIVE:
            return "POSITIVE"
        elif pred == ABSTAIN:
            return "ABSTAIN"
        else:
            raise Exception("prediction is not in [-1, 0, 1]")

    def load_latest(self) -> str:
        print("Loading latest in `output` folder...")

        folders = sorted(glob(join(config["package_dir"], "output", "*.*")))
        if len(folders) == 0:
            raise Exception(
                f"No output result found in {join(config['package_dir'], 'output')}")

        return folders[-1]


class SimplestModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.vectorizer = None
        self.model = None
        self.loaded = False

    def load(self, path: str = None) -> None:
        if not path:
            path = self.load_latest()

        self.validate_path(path, "vectorizer.pkl")
        self.validate_path(path, 'sklearn_model.pkl')

        self.vectorizer = joblib.load(join(path, 'vectorizer.pkl'))
        self.model = joblib.load(join(path, 'sklearn_model.pkl'))
        self.loaded = True

    def predict(self, text: str) -> dict:

        if not self.loaded:
            raise Exception(
                "Models are not loaded, please make sure to use .load method")

        vectors = self.vectorizer.transform([text])
        prob = self.model.predict_proba(vectors)[0]
        pred = prob.argmax(-1)
        prob = prob[pred]

        label = self.pred2label(pred)

        return {
            'pred': pred,
            'label': label,
            'prob': prob,
            'prettier': f"`{text}` => {label} ({round(prob, 3)})",
        }
