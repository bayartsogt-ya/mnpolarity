import os
import time
import joblib
from os.path import join
import pandas as pd

# [sklearn]
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# [snorkel]
from snorkel.labeling.model import LabelModel, MajorityLabelVoter
from snorkel.labeling import PandasLFApplier, LFAnalysis, filter_unlabeled_dataframe
from snorkel.utils import probs_to_preds

# [local]
from .classes import *
from .utils import read_tweet_dump
from .config import config
from .labeling_functions import get_all_lfs


class BaseModel:
    def __init__(self) -> None:
        self.output_dir = os.path.join(
            config["package_dir"], "output", str(time.time()))

        self.df = None
        self.preds_train = None
        self.probs_train = None

        self.df_train_filtered = None

    def load(self) -> None:
        raise NotImplementedError

    def predict(self, text: str) -> dict:
        raise NotImplementedError

    def train(self) -> None:
        raise NotImplementedError

    def read_dataset(self) -> None:
        self.df = read_tweet_dump(os.path.join(
            config["data_dir"], config["data"]["twitter_dump"]))
        df_twint = read_tweet_dump(os.path.join(config["data_dir"], "twint"))

        self.df = self.df.append(df_twint)
        del df_twint

        # self.df = read_tweet_dump(os.path.join(config["data_dir"], "twint"))
        print(f"[done] dataset.shape={self.df.shape}")

    def snorkel(self, lfs: list) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

        print("Starting Snorkel...")
        applier = PandasLFApplier(lfs=lfs)
        L_train = applier.apply(df=self.df)

        print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
        print("[done] pandas lf applier")

        # snorkeler = MajorityLabelVoter()
        snorkeler = LabelModel(cardinality=3, verbose=True)
        snorkeler.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=123)
        snorkeler.save(os.path.join(
            self.output_dir, "snorkel_label_model.pkl"))

        self.preds_train = snorkeler.predict(L=L_train)
        self.probs_train = snorkeler.predict_proba(L=L_train)

        self.df_train_filtered, probs_train_filtered = filter_unlabeled_dataframe(
            X=self.df, y=self.probs_train, L=L_train
        )

        preds_train_filtered = probs_to_preds(probs=probs_train_filtered)

        self.df_train_filtered["label"] = preds_train_filtered
        self.df_train_filtered.to_csv(os.path.join(
            self.output_dir, "pseudo_label.csv"))

        print(f"df_train_filtered\n{self.df_train_filtered.sample(5)}")
        print(f"[done] df_train_filtered.shape={self.df_train_filtered.shape}")

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


class SKLearnModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.vectorizer = None
        self.model = None
        self.loaded = False

    def load(self, path: str = "output/1621912006.721575") -> None:
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
            'prettier': f"{text:90s} => {label} ({round(prob, 3)})",
        }

    def train(self) -> None:
        lfs = get_all_lfs()
        self.read_dataset()
        self.snorkel(lfs)

        # --------------------- 2. Vectorization ---------------------
        print("Starting Vectorization...")
        self.vectorizer = CountVectorizer(
            ngram_range=(1, 3), max_features=3000)
        self.vectorizer.fit(self.df_train_filtered.tweet.str.lower().tolist())
        joblib.dump(self.vectorizer, os.path.join(
            self.output_dir, "vectorizer.pkl"))

        X_train = self.vectorizer.transform(self.df.tweet.str.lower().tolist())
        print("X_train.shape", X_train.shape)

        # --------------------- 3. SKLearn Training ---------------------
        print("Starting Train...")
        self.model = LogisticRegression(
            C=1e3, solver="liblinear", verbose=20)
        self.model.fit(X=X_train, y=self.preds_train)
        joblib.dump(self.model, os.path.join(
            self.output_dir, "sklearn_model.pkl"))

        y_pred = self.model.predict(X_train)

        # --------------------- 4. Evaluation ---------------------
        print("Train Stats...")
        print(classification_report(self.preds_train, y_pred))

        print("DONE")
