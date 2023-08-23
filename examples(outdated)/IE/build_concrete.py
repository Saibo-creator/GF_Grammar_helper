import os
from typing import List

from transformers import AutoTokenizer

from src.IE_grammar.crt_grammar import IE_ConcreteGrammar
from src.config.config import DATA_PATHS, GRAMMAR_JSON_CONFIG_ASSET_DIR
from src.utils import read_jsonl

if __name__ == "__main__":

    LITERAL = False
    tokenizer = AutoTokenizer.from_pretrained("saibo/llama-7B", use_fast=False)

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    IE_CRT_BASE_JSON_PATH = os.path.join(
        GRAMMAR_JSON_CONFIG_ASSET_DIR, "IE", "fe", "concrete.json"
    )

    KB = "wiki_ner"
    entities_path = DATA_PATHS["IE"]["KB"][KB]["entity"]
    relations_path = DATA_PATHS["IE"]["KB"][KB]["relation"]

    # Load entities and relations from jsonl files
    entities: List[str] = read_jsonl(entities_path)
    relations: List[str] = read_jsonl(relations_path)

    crt_grammar = IE_ConcreteGrammar(
        base_abs_grammar_path=IE_CRT_BASE_JSON_PATH,
        entities=entities,
        relations=relations,
        tokenizer=tokenizer,
        literal=LITERAL,
    )

    abs_grammar_name = "IE_wiki_ner_fe"

    str_or_int = "str" if LITERAL else "int"
    crt_grammar.set_concrete_name(
        abs_name=abs_grammar_name, str_or_int=str_or_int, tokenizer="llama"
    )

    crt_grammar.save_to_gf(dir=os.path.join(WORKING_FILE_DIR))
    crt_grammar.summary()
