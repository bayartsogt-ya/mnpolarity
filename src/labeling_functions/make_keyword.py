from snorkel.labeling import LabelingFunction
from ..classes import ABSTAIN


def keyword_lookup(x, keywords, label):
    if any(word in x.tweet.lower() for word in keywords):
        return label

    return ABSTAIN


def make_keyword_lf(keywords, label):
    return LabelingFunction(
        name=f"keyword_{keywords[0]}",
        f=keyword_lookup,
        resources=dict(keywords=keywords, label=label),
    )
