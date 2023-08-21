import json
from typing import Dict, List

from src.utils import get_hashed_name


# Abstract


def _get_entity_production_rule(entity: str) -> str:
    entity_id = get_hashed_name(string=entity)
    return f"Ent_{entity_id}: Entity"


def _get_relation_production_rule(relation: str) -> str:
    relation_id = get_hashed_name(string=relation)
    return f"Rel_{relation_id}: Rel"


def _get_entity_production_rules(entities: List[str]) -> List[str]:
    return [_get_entity_production_rule(entity=entity) for entity in entities]


def _get_relation_production_rules(relations: List[str]) -> List[str]:
    return [_get_relation_production_rule(relation=relation) for relation in relations]


def get_production_rules_for_ie(
    entities: List[str], relations: List[str], json_path: str = None
) -> List:
    entity_production_rules = _get_entity_production_rules(entities=entities)
    relation_production_rules = _get_relation_production_rules(relations=relations)
    prod_rules = entity_production_rules + relation_production_rules
    if json_path:
        with open(json_path, "w") as json_file:
            json.dump(prod_rules, json_file)
    return prod_rules


# Concrete
