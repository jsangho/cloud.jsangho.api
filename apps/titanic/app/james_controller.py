from fastapi import FastAPI

from titanic.app.jack_service import JackService

app = FastAPI(title="Titanic (James)")


class JamesController:
    def __init__(self):
        self.service = JackService()

    def get_data(self):
        return self.service.get_data()

    def get_count(self):
        return self.service.get_count()

    def get_survived_count(self) -> int:
        return self.service.get_survived_count()

    def get_dead_count(self) -> int:
        return self.service.get_dead_count()
        
    def get_model_name_and_accuracy(self):
        return self.service.get_model_name_and_accuracy()
      