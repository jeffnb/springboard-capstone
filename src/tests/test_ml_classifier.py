import os
from unittest.mock import MagicMock

import pytest
from unittest import mock

from src.core_processor import SpeechClass
from src.ml_classifier import MLClassifier


@pytest.fixture
def ml_class():
    """
    We are going to instantiate the object with the same directories in an attempt to ensure things
    don't suddenly change.  This is brittle but will work for now
    """
    DATA_DIRECTORY = "../../model_data"
    COLUMNS_PATH = os.path.join(DATA_DIRECTORY, "bow-columns.p")
    MODEL_PATH = os.path.join(DATA_DIRECTORY, "bow_xgb.joblib")
    VOCAB_PATH = os.path.join(DATA_DIRECTORY, "vocab.p")

    return MLClassifier(MODEL_PATH, VOCAB_PATH, COLUMNS_PATH)

def test_setup(ml_class):
    assert len(ml_class.vocab_words) > 5000
    assert len(ml_class.columns) > 5000
    assert "<UNK>" not in ml_class.vocab_words


def test_classify_message(ml_class):
    ml_class.preprocess_message = MagicMock()
    ml_class.preprocess_message.return_value = "foo"
    ml_class.clf.predict = MagicMock()
    ml_class.clf.predict.return_value = [1]

    assert ml_class.classify_message("HELLO HOW ARE YOU") == SpeechClass.OFFENSIVE
    ml_class.preprocess_message.assert_called_once_with("HELLO HOW ARE YOU")
    ml_class.clf.predict.assert_called_once_with("foo")


def test_classify_messge_no_mock(ml_class):
    assert SpeechClass.CLEAN == ml_class.classify_message("hello how are you")
    assert SpeechClass.OFFENSIVE == ml_class.classify_message("piece of shit")


def test_vectorize_message(ml_class):
    matrix = ml_class._vectorize_message("HELLO how are you")
    assert matrix.shape == (1, len(ml_class.vocab_words))








