from __future__ import annotations

from neo4j import AsyncDriver

from ontology.adapter.outbound.neo4j_ontology_repository import (
    Neo4jOntologyRepository,
    create_driver,
)
from ontology.app.ports.input.spam_classifier_use_case import SpamClassifierUseCase
from ontology.app.use_cases.spam_classifier_interactor import SpamClassifierInteractor

_driver: AsyncDriver | None = None


def _get_driver() -> AsyncDriver:
    global _driver
    if _driver is None:
        _driver = create_driver()
    return _driver


def get_spam_classifier_use_case() -> SpamClassifierUseCase:
    return SpamClassifierInteractor(repository=Neo4jOntologyRepository(_get_driver()))
