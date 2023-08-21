from typing import List

from src.IE_grammar import production
from src.grammar import AbstractGrammar
from src.production import Production, AbstractProduction


def IE_AbstractGrammar(
    base_abs_grammar_path: str, entities: List[str], relations: List[str], name: str
):
    """
    Build abstract grammar for IE
    :param entities: list of entities
    :param relations: list of relations
    :return: list of production rules
    """

    abs_grammar = AbstractGrammar.from_json(path=base_abs_grammar_path)

    _prod_rules: List[str] = production.get_production_rules_for_ie(
        entities=entities, relations=relations
    )
    prod_rules: List[Production] = [
        AbstractProduction.from_str(prod_rule) for prod_rule in _prod_rules
    ]

    abs_grammar.set_name(name)
    abs_grammar.add_production_rules(prod_rules=prod_rules)
    return abs_grammar
