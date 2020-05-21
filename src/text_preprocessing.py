import re
from nltk.tokenize import TweetTokenizer
from gensim.parsing.preprocessing import (
    preprocess_string,
    remove_stopwords,
    stem_text,
    strip_short,
    strip_non_alphanum,
    strip_numeric,
)
from functools import partial
import unicodedata

"""
Regex patters for mentions and uri patterns
"""
uri_pattern = re.compile(r"[A-z]+://.*")
discord_mention_pattern = re.compile(r"<@!\w+>")

# Default for strip_short is 3 this makes a callable function preset with 2 for later
strip_short2 = partial(strip_short, minsize=2)


def remove_link(token):
    """
    If the token is a uri then simply don't return anything back
    """
    if not re.match(uri_pattern, token):
        return token
    return


def remove_discord_mention(token):
    """
    If the token starts with an @ then return none otherwise return the token.  This is specific to discord.
    Other ones can be added as the bots are integrated since none should be in the corpus
    """
    if not re.match(discord_mention_pattern, token):
        return token

    return


def remove_punc(token):
    """
    Removes tokens that are only punctuation
    """
    token = re.sub(r"\W", "", token)
    return token if token else None


def remove_numeric(token):
    """
    Remove numeric only tokens.  They don't add value to this classification
    """
    return token if not token.isnumeric() else None


def remove_accented_chars(text):
    text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )
    return text


def preprocess_message(message, global_process, process_list):
    """
    Work through the message and do the following:
    * Tokenize with a message specific tokenizer
    * take a pass through all the tokens running tests on each one
    """
    tweet_tokenizer = TweetTokenizer()

    # Process global things done on entire message
    for func in global_process:
        message = func(message)

    # Now tokenize.  We will still use the tweet tokenizer for its extras
    tokens = tweet_tokenizer.tokenize(message)

    # Clean tokens
    processed_tokens = []
    for token in tokens:
        for func in process_list:
            token = func(token)
            if not token:
                break
        else:
            processed_tokens.append(token)

    return processed_tokens
