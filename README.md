# Weakly-Supervised Tweet Sentiment Classification

`#nolabel #tweet #classification #snorkel #weaklysupervised`

Tweet polarization can be useful in many analysis as a extra factor. However, because of a lack of labeled data in Mongolian (low resource language), it is hard to make progress. So in this repo, we will try to improve our classification model by using the technique called *data programming*.

*This project is highly dependant on snorkel.ai*


## Usage

```python
import joblib

vectorizer = joblib.load("output/1621912006.721575/vectorizer.pkl")
sklearn_model = joblib.load("output/1621912006.721575/sklearn_model.pkl")

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
    print(f"{t:90s} => {pred} ({round(prob[preds[i]], 3)})")
```


## Reference
* Data Programming [read more](https://arxiv.org/abs/1605.07723)
* Software 2.0 [read more](https://karpathy.medium.com/software-2-0-a64152b37c35)

