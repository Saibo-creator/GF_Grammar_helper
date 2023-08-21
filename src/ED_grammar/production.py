from typing import List, Dict

from src.IE_grammar.production import get_production_rules_for_ie


def get_production_rules_for_ed(entities: List[str], json_path: str = None) -> List:
    return get_production_rules_for_ie(
        entities=entities, relations=[], json_path=json_path
    )
