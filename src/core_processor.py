from collections import defaultdict
from enum import IntEnum


class SpeechClass(IntEnum):
    CLEAN = 0
    HATE_SPEECH = 1
    OFFENSIVE = 2


class CoreProcessor:
    """
    Main central module.  Handles the state of the bot and all central interactions with functionality
    around processing incoming data from the different bots
    """

    def __init__(self, infraction_limit: int, monitor_level: int, classifiers: list):
        """

        Args:
            infraction_limit: how many before the processor returns flag to take action
            monitor_level: 0 for no monitoring, 1 hate speech only, 2 any offensive
            classifiers: List of classifiers to run
        """
        self.infraction_limit = infraction_limit
        self.monitor_level = monitor_level
        self.offending = defaultdict(int)
        self.classifiers = classifiers

    def evaluate_message(self, message: str) -> bool:
        """
        Method will take a string message and classify it then using the {self.monitor_level} determine if it is a problem
        Args:
            message: string problem

        Returns: bool if the message is an issue

        """

        # For speed if monitoring level is just return
        if self.monitor_level == 0:
            return False

        result = self.classify_message(message)

        issue = False
        if self.monitor_level == 1 and result == SpeechClass.HATE_SPEECH :
            issue = True
        elif self.monitor_level == 2 and result.value > 0:
            issue = True

        return issue

    def classify_message(self, message: str) -> SpeechClass:
        """
        Main core of the message monitoring. Runs through various logic for classification
        Args:
            message: text of message to classify
        Returns:
            SpeechClass
        """

        classifier = self.classifiers[0]
        return classifier.classify_message(message)

    def register_over_limit(self, identifier: str) -> bool:
        """
        Registers an infraction then returns if the infraction is over the limit
        Args:
            identifier: unique id from the bot

        Returns: bool if the user is over limit

        """
        self.add_infraction(identifier)
        return self.should_take_action(identifier)

    def add_infraction(self, identifier: str) -> int:
        """
        Takes the identifer and increments in the dict for the infractions and returns the number
        Args:
            identifier: unique identifier for the infraction

        Returns: how many infractions
        """

        self.offending[identifier] += 1
        return self.offending[identifier]

    def should_take_action(self, identifier: str) -> bool:
        """
        Take the identifier and compare the {self.infraction_limit} and return True if above
        Args:
            identifier: unique identifier for the person/location

        Returns: True if person is above limit and False if not

        """
        return self.offending[identifier] > self.infraction_limit

