import json
import os
from typing import List, Dict

import src.ED_grammar.production
from src.ED_grammar.abs_grammar import ED_AbstractGrammar
from src.grammar import AbstractGrammar
from src.production import Production, AbstractProduction
from src.IE_grammar import production
from src.config.config import DATA_PATHS, GRAMMAR_JSON_CONFIG_ASSET_DIR
from src.utils import read_jsonl

if __name__ == "__main__":

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

    ABS_BASE_JSON_PATH = os.path.join(
        GRAMMAR_JSON_CONFIG_ASSET_DIR, "ED", "canonical", "abstract.json"
    )

    dataset = "aida"

    dataset_jsonl = DATA_PATHS["ED"]["Tasks"][dataset]

    # entities_path = DATA_PATHS["ED"]["KB"][None]["entity"]
    # entities: List[str] = read_jsonl(entities_path)
    with open(dataset_jsonl, "r", encoding="utf-8") as f:
        dps: List[Dict] = [json.loads(line) for line in f]

    for dp in dps[:1]:
        entities: List[str] = dp.get("candidates", None)

        abs_grammar = ED_AbstractGrammar(
            base_abs_grammar_path=ABS_BASE_JSON_PATH,
            entities=entities,
            name="ED_canonical_aida_dp0",
        )
        abs_grammar.save_to_gf(dir=os.path.join(WORKING_FILE_DIR))

        abs_grammar.summary()
