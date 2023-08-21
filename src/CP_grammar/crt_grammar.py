from typing import List

from tqdm import tqdm

from src.CP_grammar.crt_production import *
from src.GrammarBuild.CP.const import FULL_PHRASE_LEVEL_TAGS, WORD_LEVEL_TAGS
from src.grammar import (
    ConcreteGrammar,
)
from src.new_utils import LiteralStr
from src.production import Production


def CP_ConcreteGrammar(
    base_concrete_grammar_path: str,
    words: List[str],
    tokenizer,
    literal: bool,
) -> ConcreteGrammar:

    n = len(words)

    Rule0: List[Production] = [Rule0Production.instantiate()]

    Rule1: List[Production] = [
        Rule1Production.instantiate(i, j) for i in range(n) for j in range(n)
    ]
    Rule2: List[Production] = [
        Rule2Production.instantiate(i, j) for i in range(n) for j in range(n + 1)
    ]

    Rule4: List[Production] = [
        Rule4Production.instantiate(i, j) for i in range(n) for j in range(n + 2)
    ]

    Rule5: List[Production] = [Rule5Production.instantiate(i, n) for i in range(n + 1)]

    Rule6: List[Production] = [
        Rule6Production.instantiate(i, j) for i in range(n) for j in range(1, n + 1)
    ]

    Rule7: List[Production] = [
        Rule7Production.instantiate(i, j) for i in range(n) for j in range(1, n + 1)
    ]

    Rule8: List[Production] = [
        Rule8Production.instantiate(i, n) for i in range(1, n + 1)
    ]

    Rule9: List[Production] = [Rule9Production.instantiate(n)]

    RuleW: List[Production] = [
        RuleWProduction.instantiate(i, words[i], tokenizer, literal) for i in range(n)
    ]

    RuleFullPhraseLevelTag: List[Production] = [
        RuleFullPhraseLevelTagProduction.instantiate(tag, tokenizer, literal)
        for tag in FULL_PHRASE_LEVEL_TAGS
    ]

    RuleWordLevelTag: List[Production] = [
        RuleWordLevelTagProduction.instantiate(tag, tokenizer, literal)
        for tag in WORD_LEVEL_TAGS
    ]

    prod_rules = (
        Rule0
        + Rule1
        + Rule2
        + Rule4
        + Rule5
        + Rule6
        + Rule7
        + Rule8
        + Rule9
        + RuleW
        + RuleFullPhraseLevelTag
        + RuleWordLevelTag
    )

    # Add special markers

    prod_rules.extend(
        [
            CrtTerminalProduction(name="Materialise_BOG", lhs=[], rhs_elements=["[]"]),
            CrtTerminalProduction(
                name="Materialise_EOG",
                lhs=[],
                rhs_elements=[LiteralStr(tokenizer.eos_token_id)],
            ),
        ]
    )

    special_marker_terminals: List[TerminalItem] = [
        TerminalItem(text="[", name="Materialise_OpenBracket"),
        TerminalItem(text="]", name="Materialise_CloseBracket"),
        TerminalItem(text="(", name="Materialize_Left"),
        TerminalItem(text=")", name="Materialize_Right"),
    ]

    all_terminals: List[TerminalItem] = special_marker_terminals

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
