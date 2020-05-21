import pytest

from src.text_preprocessing import (
    remove_link,
    remove_discord_mention,
    remove_punc,
    preprocess_message,
)


@pytest.mark.parametrize(
    "token,expected", [("https://foo.com", None), ("httJustkidding", "httJustkidding")]
)
def test_remove_link(token, expected):
    assert remove_link(token) == expected


@pytest.mark.parametrize(
    "token,expected", [("<@!1232123432432432423>", None), ("@FOOBAR", "@FOOBAR")]
)
def test_remote_discord_mention(token, expected):
    assert remove_discord_mention(token) == expected


@pytest.mark.parametrize(
    "token,expected",
    [("YAY!!!!!!", "YAY"), ("$#*($#*(#@", None), ("Iamalongword", "Iamalongword")],
)
def test_remove_punc(token, expected):
    assert remove_punc(token) == expected


def test_preprocess_message():
    message = "HELLO ARE YOU THERE"
    result = preprocess_message(message, [str.lower], [lambda x: x[0]])
    assert result == ["h", "a", "y", "t"]
