import json
import os
from typing import List, Dict

from transformers import AutoTokenizer

from src.ED_grammar.abs_grammar import ED_AbstractGrammar
from src.ED_grammar.crt_grammar import ED_ConcreteGrammar
from src.config.config import DATA_PATHS, GRAMMAR_JSON_CONFIG_ASSET_DIR

if __name__ == "__main__":

    LITERAL = False

    task, grammar_type, dataset = "ED", "canonical", "aida"
    tokenizer = AutoTokenizer.from_pretrained("saibo/llama-7B", use_fast=False)

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

    BASE_JSON_PATH = os.path.join(
        GRAMMAR_JSON_CONFIG_ASSET_DIR, task, grammar_type, "concrete.json"
    )

    ABS_BASE_JSON_PATH = os.path.join(
        GRAMMAR_JSON_CONFIG_ASSET_DIR, task, grammar_type, "abstract.json"
    )

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

        crt_grammar = ED_ConcreteGrammar(
            base_crt_grammar_path=BASE_JSON_PATH,
            entities=entities,
            categories=abs_grammar.categories,
            mention=dp["mention"],
            tokenizer=tokenizer,
            literal=LITERAL,
        )

        abs_grammar_name = "ED_canonical_aida_dp0"

        str_or_int = "str" if LITERAL else "int"
        crt_grammar.set_concrete_name(
            abs_name=abs_grammar_name, str_or_int=str_or_int, tokenizer="llama"
        )

        crt_grammar.save_to_gf(dir=os.path.join(WORKING_FILE_DIR))

        crt_grammar.summary()
