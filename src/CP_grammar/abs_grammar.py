from typing import List
from src.ED_grammar import production
from src.grammar import AbstractGrammar
from src.production import Production, AbstractProduction
from src.CP_grammar.abs_production import *
from src.GrammarBuild.CP.const import WORD_LEVEL_TAGS, FULL_PHRASE_LEVEL_TAGS


def CP_AbstractGrammar(base_abs_grammar_path: str, num_input_words: int, name: str):
    """
    Build abstract grammar for IE
    :param entities: list of entities
    :param relations: list of relations
    :return: list of production rules
    """

    abs_grammar = AbstractGrammar.from_json(path=base_abs_grammar_path)

    n = num_input_words

    Rule1: List[AbstractProduction] = [
        Rule1Production.instantiate(i, j) for i in range(n) for j in range(n)
    ]

    Rule2: List[AbstractProduction] = [
        Rule2Production.instantiate(i, j) for i in range(n) for j in range(n + 1)
    ]

    Rule3: List[AbstractProduction] = [
        Rule4Production.instantiate(i, j) for i in range(n) for j in range(n + 2)
    ]

    Rule4: List[AbstractProduction] = [
        Rule5Production.instantiate(i, n) for i in range(n + 1)
    ]

    Rule5: List[AbstractProduction] = [
        Rule6Production.instantiate(i, j) for i in range(n) for j in range(1, n + 1)
    ]

    Rule6: List[AbstractProduction] = [
        Rule7Production.instantiate(i, j) for i in range(n) for j in range(1, n + 1)
    ]

    Rule7: List[AbstractProduction] = [
        Rule8Production.instantiate(i, n) for i in range(1, n + 1)
    ]

    Rule8: List[AbstractProduction] = [Rule9Production.instantiate(n)]

    RuleW: List[AbstractProduction] = [RuleWProduction.instantiate(i) for i in range(n)]

    RuleFullPhraseLevelTag: List[AbstractProduction] = [
        RuleFullPhraseLevelTagProduction.instantiate(tag)
        for tag in FULL_PHRASE_LEVEL_TAGS
    ]

    RuleWordLevelTag: List[AbstractProduction] = [
        RuleWordLevelTagProduction.instantiate(tag) for tag in WORD_LEVEL_TAGS
    ]

    prod_rules: List[Production] = (
        Rule1
        + Rule2
        + Rule3
        + Rule4
        + Rule5
        + Rule6
        + Rule7
        + Rule8
        + RuleW
        + RuleFullPhraseLevelTag
        + RuleWordLevelTag
    )

    abs_grammar.set_name(name)
    abs_grammar.add_production_rules(prod_rules=prod_rules)
    return abs_grammar
