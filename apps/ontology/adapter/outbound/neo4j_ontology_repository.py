from __future__ import annotations

import os
from collections import defaultdict

from neo4j import AsyncDriver, AsyncGraphDatabase

from ontology.app.dtos.spam_classification_dto import SpamClassificationDto
from ontology.app.ports.output.ontology_repository import OntologyRepository
from ontology.domain.enums.spam_classes import SpamLabel, description_of
from ontology.domain.enums.spam_rules import RULES

_SEED_QUERY = """
MERGE (c:SpamClass {label: $label})
ON CREATE SET c.description = $description
WITH c
UNWIND $keywords AS kw
MERGE (r:Rule {keyword: kw.keyword})
ON CREATE SET r.weight = toFloat(kw.weight)
MERGE (r)-[:BELONGS_TO]->(c)
"""

_CLASSIFY_QUERY = """
UNWIND $keywords AS kw
MATCH (r:Rule {keyword: kw})-[:BELONGS_TO]->(c:SpamClass)
RETURN c.label AS label, SUM(r.weight) AS score, COLLECT(r.keyword) AS matched
ORDER BY score DESC
LIMIT 1
"""


class Neo4jOntologyRepository(OntologyRepository):
    def __init__(self, driver: AsyncDriver) -> None:
        self._driver = driver

    async def seed(self) -> None:
        by_label: dict[str, list[dict]] = defaultdict(list)
        for rule in RULES:
            by_label[rule.label.value].append(
                {"keyword": rule.keyword, "weight": rule.weight}
            )

        async with self._driver.session() as session:
            for label, keywords in by_label.items():
                await session.run(
                    _SEED_QUERY,
                    label=label,
                    description=description_of(SpamLabel(label)),
                    keywords=keywords,
                )

    async def query_by_keywords(self, keywords: list[str]) -> SpamClassificationDto:
        async with self._driver.session() as session:
            result = await session.run(_CLASSIFY_QUERY, keywords=keywords)
            record = await result.single()

        if not record:
            return SpamClassificationDto(label="ham", confidence=1.0)

        total = sum(r.weight for r in RULES if r.keyword in keywords)
        confidence = round(min(record["score"] / max(total, 1.0), 1.0), 2)

        return SpamClassificationDto(
            label=record["label"],
            confidence=confidence,
            matched_keywords=list(record["matched"]),
        )


def create_driver() -> AsyncDriver:
    return AsyncGraphDatabase.driver(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        auth=(
            os.environ.get("NEO4J_USER", "neo4j"),
            os.environ["NEO4J_PASSWORD"],
        ),
    )
