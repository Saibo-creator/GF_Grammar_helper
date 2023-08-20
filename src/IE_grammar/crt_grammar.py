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


def build_concrete_grammar_for_IE(
    base_concrete_grammar_path: str,
    entities: List[str],
    relations: List[str],
    tokenizer,
    literal: bool,
) -> ConcreteGrammar:
    """
    Build concrete grammar for IE
    :param entities: list of entities
    :param relations: list of relations
    :return: list of production rules
    """

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
                terminal=terminal, tokenizer=tokenizer, literal=literal
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
    crt_grammar = ConcreteGrammar.from_json(path=base_concrete_grammar_path)
    crt_grammar.add_production_rules(prod_rules=prod_rules)
    return crt_grammar
