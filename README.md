# Mongolian Polarity Detection in Weakly Supervised manner

`#nolabel #tweet #classification #snorkel #weaklysupervised #dataprogramming #software2.0` 

Tweet polarization can be useful in many analysis as an extra factor. However, because of the lack of labeled data in Mongolian (low resource language), it is hard to make progress. So in this repo, we will try to improve our classification model using *data programming*.

*This project is highly dependant on snorkel.ai*

Contents:
- [Usage](#Usage)
- [Installation](#Installation)
- [Structure](#Structure)
- [Train Simplest Model](#Train-Simplest-Model)
- [TODO](#TODO)
- [Reference](#Reference)

## Installation
```
git clone https://github.com/bayartsogt-ya/mnpolarity.git && cd mnpolarity
pip install -r requirements.txt
```

## Usage
```python
>>> from mnpolarity.models import SimplestModel
>>> model = SimplestModel()
>>> model.load()
>>> prediction = model.predict("Чи ямар тэнэг сда вэ. Одоо чамтай - чиний миний санал зөв гэж би маргах уу")  # https://twitter.com/hariad_uyanga/status/1253729084858761216")
>>> prediction["label"]
NEGATIVE
```

## Train Simplest Model
```
python train_simplest.py
```

## Structure
```
.
├── ...
├── configs
├── data
│   ├── lf_helpers
│   │   └── negative
│   │       ├── emojis.txt
│   │       ├── phrases.txt
│   │       └── words.txt
│   └── train
│       ├── twint
│       │   ├── bad_word1.csv
│       │   ├── bad_word2.csv
│       │   └── ...
│       └── twitter_dump
│           ├── dump1.csv
│           ├── dump2.csv
│           └── ...
├── mnpolarity
│   ├── labeling_functions
│   │   ├── custom_lfs.py
│   │   └── ...
│   ├── models.py
│   └── ...
└── ...
```

## How can you improve
- Improve [Negative List](./data/labeling_functions/negative)
- Add more [custom labeling functions](./mnpolarity/labeling_functions/custom_lfs.py)
- Try&Feedback. If you have any request or idea to improve, [please email to me](mailto:bayartsogt.yadamsuren@gmail.com)

## TODO
- [ ] Negative list completion
- [ ] Positive list creation
- [ ] Negative list completion
- [ ] Labeling Function addition
    - The MOST IMPORTANT part of this code is [labeling functions build](src/labeling_functions/__init__.py)
- [ ] Experiment with hand labeled data
- [ ] Create (well validated) 1000-row test set 


## Reference
* Data Programming [read more](https://arxiv.org/abs/1605.07723)
* Software 2.0 [read more](https://karpathy.medium.com/software-2-0-a64152b37c35)

## Citation
```
@misc{mnpolarity,
  author = {Bayartsogt Yadamsuren},
  title = {Mongolian Polarity Detection in Weakly Supervised manner},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bayartsogt-ya/mnpolarity/}}
}
```