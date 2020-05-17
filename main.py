import os

from src.buttersbot import Buttersbot
from src.core_processor import CoreProcessor
from src.ml_classifier import MLClassifier

if __name__ == '__main__':
    DATA_DIRECTORY = "model_data"
    COLUMNS_PATH = os.path.join(DATA_DIRECTORY, "bow-columns.p")
    MODEL_PATH = os.path.join(DATA_DIRECTORY, "bow_xgb.joblib")
    VOCAB_PATH = os.path.join(DATA_DIRECTORY, "vocab.p")
    INFRACTION_LIMIT = 3
    MONITOR_LEVEL = 2

    ml_classifier = MLClassifier(MODEL_PATH, VOCAB_PATH, COLUMNS_PATH)

    processor = CoreProcessor(INFRACTION_LIMIT, MONITOR_LEVEL, [ml_classifier])

    bot = Buttersbot(command_prefix='!', description="Cute and watching", processor=processor)
    bot.run(os.environ["DISCORD_KEY"])