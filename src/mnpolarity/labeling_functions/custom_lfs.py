"""
Labeling Function an example
"""

import pandas as pd
from snorkel.labeling import labeling_function

from ..classes import NEGATIVE, ABSTAIN, POSITIVE


@labeling_function()
def lf_negative_word_arai2(x: pd.Series):
    if "arai arai" in x.tweet.lower():
        return NEGATIVE

    return ABSTAIN


def get_all_custom_lfs() -> list:
    return [
        lf_negative_word_arai2
    ]
