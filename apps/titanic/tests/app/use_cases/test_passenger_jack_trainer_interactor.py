import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.introduce_myself = AsyncMock(
        return_value=JackTrainerResponse(id=9, name="Jack Dawson")
    )
    return repo


@pytest.fixture
def interactor(mock_repository):
    return JackTrainerInteractor(repository=mock_repository)


class TestIntroduceMyself:
    def test_calls_repository_with_correct_query(self, interactor, mock_repository):
        query = JackTrainerQuery(id=9, name="Jack Dawson")

        asyncio.run(interactor.introduce_myself(query))

        mock_repository.introduce_myself.assert_called_once_with(query)

    def test_returns_repository_response(self, interactor):
        query = JackTrainerQuery(id=9, name="Jack Dawson")

        response = asyncio.run(interactor.introduce_myself(query))

        assert response == JackTrainerResponse(id=9, name="Jack Dawson")
