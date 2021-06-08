# [main]
import os
import joblib
import time

# [snorkel]
from snorkel.labeling.model import LabelModel
from snorkel.labeling import PandasLFApplier, LFAnalysis, filter_unlabeled_dataframe
from snorkel.utils import probs_to_preds

# [local]
from mnpolarity.labeling_functions import get_all_lfs
from mnpolarity.config import config
from mnpolarity.utils import read_all_train_data


if __name__ == "__main__":

    st = time.time()
    output_dir = os.path.join(
        config["package_dir"], "output", "0.0")

    print("--------------------- -1. create LFS ---------------------")
    lfs = get_all_lfs()

    print("--------------------- 0. Read Data ---------------------")
    df = read_all_train_data(config['data_dir'], include_twitter_dump=False)
    print(f"Data Loaded df.shape={df.shape}")

    print("--------------------- 1. Snorkeling ---------------------")
    os.makedirs(output_dir, exist_ok=True)
    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df)

    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
    print("[done] pandas lf applier")

    # snorkeler = MajorityLabelVoter()
    snorkeler = LabelModel(cardinality=3, verbose=True)
    snorkeler.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=123)
    snorkeler.save(os.path.join(output_dir, "snorkel_label_model.pkl"))

    preds_train = snorkeler.predict(L=L_train)
    probs_train = snorkeler.predict_proba(L=L_train)

    df_train_filtered, probs_train_filtered = filter_unlabeled_dataframe(
        X=df, y=probs_train, L=L_train
    )

    preds_train_filtered = probs_to_preds(probs=probs_train_filtered)

    df_train_filtered["label"] = preds_train_filtered
    df_train_filtered.to_csv(os.path.join(output_dir, "pseudo_label.csv"))

    print(f"df_train_filtered\n{df_train_filtered}")

    print("--------------------- 2. Vectorization ---------------------")
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(ngram_range=(1, 3), max_features=3000)
    vectorizer.fit(df_train_filtered.tweet.str.lower().tolist())
    joblib.dump(vectorizer, os.path.join(output_dir, "vectorizer.pkl"))

    X_train = vectorizer.transform(df.tweet.str.lower().tolist())
    print("X_train.shape", X_train.shape)

    print("--------------------- 3. SKLearn Training ---------------------")
    from sklearn.linear_model import LogisticRegression

    sklearn_model = LogisticRegression(C=1e3, solver="liblinear")
    sklearn_model.fit(X=X_train, y=preds_train)
    joblib.dump(sklearn_model, os.path.join(output_dir, "sklearn_model.pkl"))

    y_pred = sklearn_model.predict(X_train)

    print("--------------------- 4. Evaluation ---------------------")
    from sklearn.metrics import classification_report
    print(classification_report(preds_train, y_pred))

    print("--------------------- 5. Testing ---------------------")
    # link to tweet
    text = [
        "эд нарыг үзэн ядаж байна",
        # https://twitter.com/tsbat_IT/status/937989630472761344
        "#Утаа г үзэн ядаж байна..",
        # https://twitter.com/gt_log/status/1338014887407091713
        "Өө тэнэг сда вэ. Орлого арав дахин өсгөж бхад хариуцлага ярих хэцүү шд гшш",
        # https://twitter.com/hariad_uyanga/status/1253729084858761216
        "Чи ямар тэнэг сда вэ. Одоо чамтай - чиний миний санал зөв гэж би маргах уу",
        "Shaa shaa T1 sda",  # https://twitter.com/Orchidz11/status/1315561414883500032
        # https://twitter.com/enzia3/status/1396662686042238981
        "Гоё сайхан үгс яахав ээ. Мөрийн хөтөлбөр уншмаар байна?"
    ]

    vectors = vectorizer.transform([t.lower() for t in text])
    probs = sklearn_model.predict_proba(vectors)

    preds = probs.argmax(-1)
    for i, t in enumerate(text):
        pred = "NEGATIVE" if preds[i] == 1 else "ABSTRAIN"
        prob = probs[i]
        print(f"{t} => {pred} ({round(prob[preds[i]], 3)})")

    print("------------------------------------------")
    print(f"done in {time.time() - st: .1f} sec")
    print("------------------------------------------")
