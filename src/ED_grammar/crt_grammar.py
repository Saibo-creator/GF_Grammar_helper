from typing import List

from tqdm import tqdm

from src.grammar import (
    ConcreteGrammar,
    TerminalItem,
    EntityTerminalItem,
    CrtTerminalProduction,
)
from src.new_utils import LiteralStr


def build_concrete_grammar_for_ED(
    base_concrete_grammar_path: str,
    mention: str,
    entities: List[str],
    tokenizer,
    literal: bool,
) -> ConcreteGrammar:
    """
    Build concrete grammar for IE
    :param entities: list of entities
    :param relations: list of relations
    :return: list of production rules
    """

    # Create terminal productions from terminal items
    prod_rules: List[CrtTerminalProduction] = []

    prod_rules.extend(
        [
            CrtTerminalProduction(name="Materialise_BOG", lhs=[], rhs=["[]"]),
            CrtTerminalProduction(
                name="Materialise_EOG", lhs=[], rhs=[LiteralStr(tokenizer.eos_token_id)]
            ),
        ]
    )

    # Create terminal items from entities and relations
    entity_terminals: List[TerminalItem] = [
        EntityTerminalItem(entity=entity) for entity in entities
    ]

    special_marker_terminals: List[TerminalItem] = [
        TerminalItem(text="[", name="Materialise_OpenBracket"),
        TerminalItem(text="]", name="Materialise_CloseBracket"),
        TerminalItem(text=mention, name="Materialise_Mention"),
        TerminalItem(text=": Canonical Form", name="Materialise_Canonical_phrase"),
    ]

    all_terminals: List[TerminalItem] = special_marker_terminals + entity_terminals

    for terminal in tqdm(all_terminals):
        prod_rules.append(
            CrtTerminalProduction.from_terminal(
                terminal=terminal, tokenizer=tokenizer, literal=literal
            )
        )

    # Create concrete grammar by adding production rules to the base concrete grammar
    crt_grammar = ConcreteGrammar.from_json(path=base_concrete_grammar_path)
    crt_grammar.add_production_rules(prod_rules=prod_rules)
    return crt_grammar
