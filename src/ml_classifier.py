import numpy as np
import pandas as pd
import pickle
import re
import os
import contractions
import joblib
from gensim.parsing import strip_non_alphanum, strip_numeric, remove_stopwords, stem_text
from sklearn.feature_extraction.text import CountVectorizer

from src import text_preprocessing
from src.core_processor import SpeechClass
from src.text_preprocessing import remove_accented_chars, remove_link, remove_discord_mention, remove_punc, strip_short2


class MLClassifier:

    predict_map = {0: SpeechClass.HATE_SPEECH, 1: SpeechClass.OFFENSIVE, 2: SpeechClass.CLEAN}

    def __init__(self, model_path: str, vocab_path: str, column_path: str):
        """
        Loads the model in case it doesn't exist
        Args:
            model_location: string path to model dump file
        """
        self.clf = joblib.load(model_path)
        self.vocab_words = self._process_vocab(pickle.load(open(vocab_path, "rb")))
        self.columns = pickle.load(open(column_path, "rb"))

    @staticmethod
    def _process_vocab(vocab) -> list:
        """
        Converts the vocab to a list of words and pulls out the <UNK> token just in case it exists
        Args:
            vocab: vocabulary

        Returns: list of vocabulary words

        """
        vocab_words = list(vocab)
        vocab_words.remove("<UNK>")
        return vocab_words

    def classify_message(self, message: str) -> SpeechClass:
        """

        Args:
            message: string message to be processed

        Returns: SpeechClass transforming the internal classes to common ones
        """
        processed = self.preprocess_message(message)
        prediction = self.clf.predict(processed)[0]

        return self.predict_map[prediction]

    def preprocess_message(self, message:str) -> pd.DataFrame:

        globa_process_list = [str.lower, contractions.fix, remove_accented_chars]
        process_list = [str.lower, str.strip, remove_link, remove_discord_mention, remove_punc,
                        strip_non_alphanum, strip_numeric, strip_short2, remove_stopwords, stem_text]

        tokenized_message = text_preprocessing.preprocess_message(message, globa_process_list, process_list)
        processed = ' '.join(tokenized_message)
        cv_matrix = self._vectorize_message(processed)
        return self._matrix_to_dataframe(cv_matrix)

    def _vectorize_message(self, message: str) -> np.ndarray:
        """
        Simply vectorizes the message into a matrix for bow
        Args:
            message: string to pricess
        Returns:matrix for the count vectors

        """
        cv = CountVectorizer(min_df=0., max_df=1., vocabulary=self.vocab_words)
        cv_matrix = cv.fit_transform([message])
        return cv_matrix.toarray()

    def _matrix_to_dataframe(self, matrix: np.ndarray) -> pd.DataFrame:
        """
        For no reason I have been able to find the XGBoost algorithm needs to have a dataframe
        Args:
            matrix: matrix created by {self._vectorize_message}
        Returns: dataframe with correct columns
        """

        return pd.DataFrame(matrix, columns=self.columns[3:])

