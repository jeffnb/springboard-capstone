from unittest.mock import MagicMock

import pytest

from src.core_processor import CoreProcessor, SpeechClass


@pytest.fixture
def processor():
    classifier1 = MagicMock()
    classifier2 = MagicMock()
    return CoreProcessor(3, 2, [classifier1, classifier2])


def test_add_infraction(processor):
    id = "FOOBAR"

    assert processor.add_infraction(id) == 1
    assert processor.add_infraction(id) == 2


def test_should_take_action(processor):
    id = "FOOBAR"

    processor.offending[id] = 1
    assert not processor.should_take_action(id)

    processor.offending[id] = 20
    assert processor.should_take_action(id)


def test_register_over_limit(processor):
    processor.add_infraction = MagicMock()
    processor.should_take_action = MagicMock()

    id = "FOOBAR"
    processor.register_over_limit(id)
    processor.add_infraction.assert_called_once_with(id)
    processor.should_take_action.assert_called_once_with(id)


def test_classify_message(processor):
    message = "Hello my dear"
    classifier_mock = processor.classifiers[0]

    classifier_mock.classify_message = MagicMock()
    processor.classify_message(message)

    classifier_mock.classify_message.assert_called_once_with(message)


@pytest.mark.parametrize(
    "level,result,expected",
    [
        (0, SpeechClass.HATE_SPEECH, False),
        (1, SpeechClass.HATE_SPEECH, True),
        (2, SpeechClass.OFFENSIVE, True),
        (2, SpeechClass.HATE_SPEECH, True),
        (2, SpeechClass.CLEAN, False),
        (1, SpeechClass.OFFENSIVE, False),
    ],
)
def test_evaluate_message_no_monitor(processor, level, result, expected):
    """
    This should test all of the usecase logic
    """
    processor.classify_message = MagicMock()
    processor.classify_message.return_value = result

    processor.monitor_level = level

    assert processor.evaluate_message("HELLO") == expected
