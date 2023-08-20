import os
from typing import List

from tqdm import tqdm
from transformers import AutoTokenizer

from src.grammar import (
    ConcreteGrammar,
    Production,
    TerminalItem,
    EntityTerminalItem,
    RelationTerminalItem,
    CrtTerminalProduction,
)
from src.config.config import DATA_PATHS, JSON_GF_ASSET_DIR
from src.new_utils import LiteralStr
from src.utils import read_jsonl

if __name__ == "__main__":

    LITERAL = False
    tokenizer = AutoTokenizer.from_pretrained("saibo/llama-7B", use_fast=False)

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    IE_CRT_BASE_JSON_PATH = os.path.join(
        JSON_GF_ASSET_DIR, "IE", "fully_expanded", "concrete.json"
    )

    KB = "wiki_ner"
    entities_path = DATA_PATHS["IE"]["KB"][KB]["entity"]
    relations_path = DATA_PATHS["IE"]["KB"][KB]["relation"]

    # Load entities and relations from jsonl files
    entities: List[str] = read_jsonl(entities_path)
    relations: List[str] = read_jsonl(relations_path)

    # Create terminal items from entities and relations
    entity_terminals: List[TerminalItem] = [
        EntityTerminalItem(entity=entity) for entity in entities
    ]
    relation_terminals: List[TerminalItem] = [
        RelationTerminalItem(relation=relation) for relation in relations
    ]

    special_marker_terminals: List[TerminalItem] = [
        TerminalItem(text="[s]", name="Materialise_SubjectMarker"),
        TerminalItem(text="[o]", name="Materialise_ObjectMarker"),
        TerminalItem(text="[r]", name="Materialise_RelationMarker"),
        TerminalItem(text="[e]", name="Materialise_TripletEndingMarker"),
    ]

    all_terminals: List[TerminalItem] = (
        special_marker_terminals + entity_terminals + relation_terminals
    )

    # Create terminal productions from terminal items
    prod_rules: List[CrtTerminalProduction] = []
    for terminal in tqdm(all_terminals):
        prod_rules.append(
            CrtTerminalProduction.from_terminal(
                terminal=terminal, tokenizer=tokenizer, literal=LITERAL
            )
        )

    prod_rules.extend(
        [
            CrtTerminalProduction(name="Materialise_BOG", lhs=[], rhs=["[]"]),
            CrtTerminalProduction(
                name="Materialise_EOG", lhs=[], rhs=[LiteralStr(tokenizer.eos_token_id)]
            ),
        ]
    )

    # Create concrete grammar by adding production rules to the base concrete grammar
    crt_grammar = ConcreteGrammar.from_json(path=IE_CRT_BASE_JSON_PATH)
    abs_grammar_name = "IE_wiki_ner_fe"
    crt_grammar.set_abstract_grammar_name(
        abs_name="IE_wiki_ner_fe", concrete_postfix="_str" if LITERAL else "_int"
    )
    crt_grammar.add_production_rules(prod_rules=prod_rules)

    crt_grammar.save(dir=os.path.join(WORKING_FILE_DIR))
    crt_grammar.summary()
