from __future__ import annotations

from ontology.app.dtos.spam_classification_dto import SpamClassificationDto
from ontology.app.ports.input.spam_classifier_use_case import SpamClassifierUseCase
from ontology.app.ports.output.ontology_repository import OntologyRepository
from ontology.domain.enums.spam_rules import RULES


class SpamClassifierInteractor(SpamClassifierUseCase):
    def __init__(self, repository: OntologyRepository) -> None:
        self._repository = repository

    async def classify(self, subject: str, body: str) -> SpamClassificationDto:
        text = f"{subject} {body}"
        matched = [r.keyword for r in RULES if r.keyword in text]
        if not matched:
            return SpamClassificationDto(label="ham", confidence=1.0)
        return await self._repository.query_by_keywords(matched)

    async def initialize(self) -> None:
        await self._repository.seed()
