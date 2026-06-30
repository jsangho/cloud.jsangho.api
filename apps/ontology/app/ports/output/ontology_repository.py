from __future__ import annotations

from abc import ABC, abstractmethod

from ontology.app.dtos.spam_classification_dto import SpamClassificationDto


class OntologyRepository(ABC):
    @abstractmethod
    async def query_by_keywords(self, keywords: list[str]) -> SpamClassificationDto: ...

    @abstractmethod
    async def seed(self) -> None: ...
