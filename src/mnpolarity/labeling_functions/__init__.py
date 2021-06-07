from os.path import join
from . import custom_lfs
from .make_keyword import make_keyword_lf
from ..config import config
from ..utils import read_lf_list
from ..classes import *


print(f"INSIDE LFs: {config['data']}")


def get_all_lfs() -> list:
    """
    Return all the labeling functions used in PandasLFApplier
    """

    # 1. negative words ------------------------------
    negative_words = read_lf_list(
        join(config['data_dir'], config['data']['path_to_negative_words'])
    )
    print("Number of Negative Words:", len(negative_words))

    lf_negative_words = [make_keyword_lf(
        words, NEGATIVE) for words in negative_words]

    # 2. negative phrases ------------------------------
    negative_phrases = read_lf_list(
        join(config['data_dir'], config['data']['path_to_negative_phrases'])
    )
    print("Number of Negative Phrases:", len(negative_phrases))

    lf_negative_phrases = [make_keyword_lf(
        phrases, NEGATIVE) for phrases in negative_phrases]

    # 3. negative emojis ------------------------------
    negative_emojis = read_lf_list(
        join(config['data_dir'], config['data']['path_to_negative_emojis'])
    )
    print("Number of Negative Emojis:", len(negative_emojis))

    lf_negative_emojis = [make_keyword_lf(
        phrases, NEGATIVE) for phrases in negative_emojis]

    # 4. labeled data ------------------------------
    # TODO hand label data and read it here ->
    # ref: https://www.snorkel.org/use-cases/crowdsourcing-tutorial
    lf_hand_labeled = []

    return [
        *lf_negative_words,
        *lf_negative_phrases,
        *lf_negative_emojis,
        *lf_hand_labeled,
        *custom_lfs.get_all_custom_lfs()
    ]
