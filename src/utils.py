from glob import glob
import os
import pandas as pd
from tqdm import tqdm
import yaml


def read_lf_list(path: str, twinting: bool = True) -> list:
    """
    input:
    ---------
    path [str]: path to alternative writing dictionary with the following structure:
        ```
        муу|muu|mu|...
        ...
        ```
    return:
    ---------
    list of list of words
    """
    data = []
    with open(path, "r") as reader:
        for l in reader.readlines():
            l = l.rstrip("\n")
            words = [w.strip() for w in l.split("|")]
            data.append(words)

    if twinting and len(data[0]) > 0:
        from .twint_helper import getAndSaveTweetsByKeyword
        for words in data:
            for word in words:
                getAndSaveTweetsByKeyword(word)

    return data


def read_config(path: str) -> dict:

    config: str
    with open(path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            print(f"""---------- CONFIG ----------\n{config}\n""")
        except yaml.YAMLError as exc:
            print(exc)

    return config


def read_tweet_dump(directory: str) -> pd.DataFrame:

    from .config import config

    ll = sorted(glob(os.path.join(directory, "*.csv")))
    if len(ll) == 0:
        raise Exception(f"No csv data found inside {directory}")

    df = pd.DataFrame(columns=config['data']['columns'])
    for l in tqdm(ll):
        df = df.append(pd.read_csv(l, usecols=config['data']['columns']))

    return df
