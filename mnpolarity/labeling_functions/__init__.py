from os.path import join
from . import custom_lfs
from .make_keyword import make_keyword_lf
from ..config import config
from ..utils import read_lf_list
from ..classes import *


def get_all_lfs() -> list:
    """
    Return all the labeling functions used in PandasLFApplier
    """

    default_lfs = []
    # ------- Negative default Labeling Functions (lfs) --------
    for _type in ['words', 'phrases', 'emojis']:
        _list = read_lf_list(
            join(config['data_dir'], 'lf_helpers', 'negative', f'{_type}.txt')
        )
        print(f"# of negative {_type}: {len(_list)}")

        _lf = [make_keyword_lf(words, NEGATIVE) for words in _list]

        default_lfs += _lf

    # ------- TODO Positive default Labeling Functions (lfs) --------
    # pass

    # ------- TODO Hand Labeled default Labeling Functions (lfs) --------
    # ref: https://www.snorkel.org/use-cases/crowdsourcing-tutorial
    lf_hand_labeled = []

    return [
        *default_lfs,
        *lf_hand_labeled,
        *custom_lfs.get_all_custom_lfs()
    ]
