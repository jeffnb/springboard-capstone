import os
import logging
import sys

from src.buttersbot import Buttersbot
from src.core_processor import CoreProcessor
from src.ml_classifier import MLClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("buttersbot.log"), logging.StreamHandler(sys.stdout)],
)

if __name__ == "__main__":

    DATA_DIRECTORY = "model_data"
    COLUMNS_PATH = os.path.join(DATA_DIRECTORY, "bow-columns.p")
    MODEL_PATH = os.path.join(DATA_DIRECTORY, "bow_xgb.joblib")
    VOCAB_PATH = os.path.join(DATA_DIRECTORY, "vocab.p")
    INFRACTION_LIMIT = 3
    # 0 for no montoring, 1 for hate speech, 2 for anything offensive
    MONITOR_LEVEL = 2

    ml_classifier = MLClassifier(MODEL_PATH, VOCAB_PATH, COLUMNS_PATH)

    processor = CoreProcessor(INFRACTION_LIMIT, MONITOR_LEVEL, [ml_classifier])

    bot = Buttersbot(
        command_prefix="!", description="Cute and watching", processor=processor
    )
    bot.run(os.environ["DISCORD_KEY"])
