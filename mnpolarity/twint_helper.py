import os
import twint
from .config import config


def getAndSaveTweetsByKeyword(keyword: str) -> bool:
    twint_config = config["twint"]
    twint_config["Search"] = keyword,
    twint_config["Output"] = os.path.join(
        config["data_dir"], "train", "twint", f"{keyword}.csv"
    )

    if os.path.isfile(twint_config["Output"]):
        print(f"The file has already downloaded in {twint_config['Output']}")
        return False

    c = twint.Config(**twint_config)
    twint.run.Search(c)

    return True
