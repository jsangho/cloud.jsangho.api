from typing import Any

from titanic.app.rose_model import RoseModel
from titanic.app.walter_reader import WalterReader


class JackService:

    def __init__(self) -> None:
        self.walter = WalterReader()
        self.rose = RoseModel()

    def get_data(self):
        return self.walter.get_data()

    def get_count(self):
        return self.walter.get_count()

    def get_survived_count(self) -> int:
        return self.walter.get_survived_count()

    def get_dead_count(self) -> int:
        return self.walter.get_dead_count()

    def get_model_name_and_accuracy(self):
        return self.rose.get_model_name()
       