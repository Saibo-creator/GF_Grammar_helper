#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from typing import List, Union
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.ED.indep.indep_abs_grammar import ED_IndepMinimalAbsGrammarBuilder


class ED_DepMultiMentionAbsGrammarBuilder(ED_IndepMinimalAbsGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "ED", "Dep", "multi-mention", "ED-Dep-multi-mention-AbsTemplate.hs")
    grammar_prefix = ""

    NUMERATED_MENTION_TEMPLATE = "Mention{i}"
    NUMERATED_RIGHT_CONTEXT_TEMPLATE = "RightContext{i}"
    NUMERATED_UNIT_TEMPLATE = "Unit{i}"
    NUMERATED_ENTITY_TEMPLATE = "Entity{i}"

    NUMERATED_UNIT_DERIVATION_RULE_TEMPLATE = "Unit{i}Derivation: StartMarker -> Mention{i} -> OpenBracket -> Entity{i} -> CloseBracket -> EndMarker -> RightContext{i} -> Unit{i};"
    NUMERATED_RIGHT_CONTEXT_MATERIALISATION_RULE_TEMPLATE = "Materialise_RightContext{i}: RightContext{i} ;"
    NUMERATED_MENTION_MATERIALISATION_RULE_TEMPLATE = "Materialise_Mention{i}: Mention{i} ;"

    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        grammar: str = self.read_template()

        entities_or_path: Union[List[str], str, List[List[str]]] = kwargs["entities_or_path"]
        num_mentions: int = kwargs["num_mentions"]
        assert type(entities_or_path) == list and type(
            entities_or_path[0]) == list, "entities should be list of list of entities"
        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        NumeratedMentions = self.get_NumeratedMentions(num_mentions=num_mentions)
        NumeratedRightContexts = self.get_NumeratedRightContexts(num_mentions=num_mentions)
        NumeratedUnits = self.get_NumeratedUnits(num_mentions=num_mentions)
        NumeratedEntities = self.get_NumeratedEntities(num_mentions=num_mentions)
        NumeratedUnitsAsInputVars = self.get_NumeratedUnitsAsInputVars(num_mentions=num_mentions)
        NumeratedUnitDerivationRules = self.get_NumeratedUnitDerivationRules(num_mentions=num_mentions)
        NumeratedRightContextMaterialisationRules = self.get_NumeratedRightContextMaterialisationRules(num_mentions=num_mentions)
        NumeratedMentionMaterialisationRules = self.get_NumeratedMentionMaterialisationRules(num_mentions=num_mentions)
        NumeratedEntitiesMaterialisationRules = self.get_NumeratedEntitiesMaterialisationRules(entities=entities_or_path)

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           NumeratedMentions=NumeratedMentions,
                                                           NumeratedRightContexts=NumeratedRightContexts,
                                                           NumeratedUnits=NumeratedUnits,
                                                           NumeratedEntities=NumeratedEntities,
                                                           NumeratedUnitsAsInputVars=NumeratedUnitsAsInputVars,
                                                           NumeratedUnitDerivationRules=NumeratedUnitDerivationRules,
                                                           NumeratedRightContextMaterialisationRules=NumeratedRightContextMaterialisationRules,
                                                           NumeratedMentionMaterialisationRules=NumeratedMentionMaterialisationRules,
                                                           NumeratedEntitiesMaterialisationRules=NumeratedEntitiesMaterialisationRules)
        # grammar_meta = self.build_meta(entities=entities)

        return Grammar(formatted_grammar_plain_text, name=abs_grammar_name, meta=None)
    def get_NumeratedMentions(self, num_mentions:int):
        mentions = [self.NUMERATED_MENTION_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ; ".join(mentions)

    def get_NumeratedRightContexts(self, num_mentions:int):
        right_contexts = [self.NUMERATED_RIGHT_CONTEXT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ; ".join(right_contexts)

    def get_NumeratedUnits(self, num_mentions:int):
        units = [self.NUMERATED_UNIT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ; ".join(units)

    def get_NumeratedEntities(self, num_mentions:int):
        entities = [self.NUMERATED_ENTITY_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ; ".join(entities)

    def get_NumeratedUnitsAsInputVars(self, num_mentions:int):
        units = [self.NUMERATED_UNIT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " -> ".join(units)

    def get_NumeratedUnitDerivationRules(self, num_mentions:int):
        UnitDerivationRules = [self.NUMERATED_UNIT_DERIVATION_RULE_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return self.join_statements_multi_line(UnitDerivationRules)

    def get_NumeratedRightContextMaterialisationRules(self, num_mentions:int):
        RightContextMaterialisationRules = [self.NUMERATED_RIGHT_CONTEXT_MATERIALISATION_RULE_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return self.join_statements_multi_line(RightContextMaterialisationRules)

    def get_NumeratedMentionMaterialisationRules(self, num_mentions:int):
        MentionMaterialisationRules = [self.NUMERATED_MENTION_MATERIALISATION_RULE_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return self.join_statements_multi_line(MentionMaterialisationRules)

    def get_NumeratedEntitiesMaterialisationRules(self, entities:List[List[str]]):
        NumeratedEntitiesMaterialisationRules = [self.add_entities_derivative_rules(entities[i], i) for i in range(len(entities))]
        return self.join_statements_multi_line(NumeratedEntitiesMaterialisationRules)


if __name__ == '__main__':
    grammar = ED_DepMultiMentionAbsGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=True) \
        .build(base_grammar_name="ED-OTFE", num_mentions=2, entities_or_path=[["Q1", "Q2", "Q3", "Q4"], ["Q5", "Q6", "Q7", "Q8"]])
    grammar.save("./ED-Dep-multi-mention-AbsTemplate.hs")






