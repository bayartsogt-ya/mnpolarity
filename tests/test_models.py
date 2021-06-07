import pytest
from mnpolarity import models

sklearner = models.SKLearnModel()


def test_load():
    sklearner.load()
    assert True


def test_predict():
    result = sklearner.predict("Shaa shaa T1 sda".lower())
    assert type(result) == dict
    assert 'pred' in result
    assert 'label' in result
    assert 'prob' in result
    assert 'prettier' in result
    assert result['label'] == 'NEGATIVE'


def test_train():
    sklearner.train()
