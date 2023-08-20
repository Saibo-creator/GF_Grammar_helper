import os
from typing import List

from src.grammar import AbstractGrammar, Production, AbstractProduction
from src.IE_grammar import abstract
from src.config.config import DATA_PATHS, JSON_GF_ASSET_DIR
from src.utils import read_jsonl

if __name__ == "__main__":

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

    IE_ABS_BASE_JSON_PATH = os.path.join(
        JSON_GF_ASSET_DIR, "IE", "fully_expanded", "abstract.json"
    )
    IE_CRT_BASE_JSON_PATH = os.path.join(
        JSON_GF_ASSET_DIR, "IE", "fully_expanded", "concrete.json"
    )

    KB = "wiki_ner"
    entities_path = DATA_PATHS["IE"]["KB"][KB]["entity"]
    relations_path = DATA_PATHS["IE"]["KB"][KB]["relation"]

    entities: List[str] = read_jsonl(entities_path)
    relations: List[str] = read_jsonl(relations_path)

    _prod_rules: List[str] = abstract.get_production_rules_for_ie(
        entities=entities, relations=relations
    )["production_rules"]
    prod_rules: List[Production] = [
        AbstractProduction.from_str(prod_rule) for prod_rule in _prod_rules
    ]

    abs_grammar = AbstractGrammar.from_json(path=IE_ABS_BASE_JSON_PATH)
    abs_grammar.set_name("IE_wiki_ner_fe")
    abs_grammar.add_production_rules(prod_rules=prod_rules)
    abs_grammar.save(dir=os.path.join(WORKING_FILE_DIR))

    abs_grammar.summary()
