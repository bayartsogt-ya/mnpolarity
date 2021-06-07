import os
from mnpolarity.config import config
from mnpolarity.twint_helper import getAndSaveTweetsByKeyword


def test_twint():
    keyword = "arai"

    getAndSaveTweetsByKeyword(keyword)

    # ------ Test ------
    import pandas as pd

    df = pd.read_csv(os.path.join(
        config["data_dir"], "twint", f"{keyword}.csv"))
    assert df.shape[0] > 0

    for row in df.itertuples():
        if keyword in row.tweet:
            print(row.tweet)
