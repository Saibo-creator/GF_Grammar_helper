import os
from typing import List

from src.IE_grammar.abs_grammar import build_abstract_grammar_for_IE
from src.grammar import AbstractGrammar, Production, AbstractProduction
from src.IE_grammar import production
from src.config.config import DATA_PATHS, JSON_GF_ASSET_DIR
from src.utils import read_jsonl


if __name__ == "__main__":

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

    ABS_BASE_JSON_PATH = os.path.join(
        JSON_GF_ASSET_DIR, "IE", "fully_expanded", "abstract.json"
    )

    KB = "wiki_ner"
    entities_path = DATA_PATHS["IE"]["KB"][KB]["entity"]
    relations_path = DATA_PATHS["IE"]["KB"][KB]["relation"]

    entities: List[str] = read_jsonl(entities_path)
    relations: List[str] = read_jsonl(relations_path)

    # build grammar for IE

    abs_grammar = build_abstract_grammar_for_IE(
        base_abs_grammar_path=ABS_BASE_JSON_PATH,
        entities=entities,
        relations=relations,
        name="IE_wiki_ner_fe",
    )

    # save grammar
    abs_grammar.save(dir=os.path.join(WORKING_FILE_DIR))

    abs_grammar.summary()
