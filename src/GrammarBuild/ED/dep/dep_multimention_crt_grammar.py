#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from abc import ABC
from typing import List, Union

from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.ED.indep.indep_crt_grammar import ED_IndepMinimalCrtGrammarBuilder


class ED_DepMultiMentionCrtGrammarBuilder(ED_IndepMinimalCrtGrammarBuilder, ABC):
    template = os.path.join(TEMPLATE_DIR, "ED", "dep", "multi-mention", "ED-DEP-multi-mention-CrtTemplate.hs")
    grammar_prefix = ""

    Open_bracket_marker = "["
    Close_bracket_marker = "]"

    

    StartMarker = "[START_ENT]"
    EndMarker = "[END_ENT]"

    NUMERATED_MENTION_TEMPLATE = "Mention{i}"
    NUMERATED_RIGHT_CONTEXT_TEMPLATE = "RightContext{i}"
    NUMERATED_UNIT_TEMPLATE = "Unit{i}"
    NUMERATED_ENTITY_TEMPLATE = "Entity{i}"

    NUMERATED_UNIT_DERIVATION_RULE_TEMPLATE = "Unit{i}Derivation: start_marker mention{i} open_bracket entity{i} close_bracket end_marker right_context{i} = start_marker ++ mention{i} ++ open_bracket ++ entity{i} ++ close_bracket ++ end_marker ++ right_context{i};"
    # start_marker mention1 open_bracket entity1 close_bracket end_marker right_context1 = start_marker ++ mention1 ++ open_bracket ++ entity1 ++ close_bracket ++ end_marker ++ right_context1;
    NUMERATED_RIGHT_CONTEXT_MATERIALISATION_RULE_TEMPLATE = "Materialise_RightContext{i}: {tokens} ;"
    NUMERATED_MENTION_MATERIALISATION_RULE_TEMPLATE = "Materialise_Mention{i}: {tokens} ;"

    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        entities_or_path: Union[List[str], str, List[List[str]]] = kwargs["entities_or_path"]
        crt_grammar_name = kwargs.get("crt_grammar_name", None)
        mentions: List[str] = kwargs["mentions"]
        contexts: List[str] = kwargs["contexts"]

        # entities should be list of list of entities
        assert type(entities_or_path) == list and type(entities_or_path[0]) == list, "entities should be list of list of entities"

        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path

        num_mentions = len(mentions)
        left_context0 = contexts[0]

        NumeratedMentions = self.get_NumeratedMentions(num_mentions=num_mentions)
        NumeratedRightContexts = self.get_NumeratedRightContexts(num_mentions=num_mentions)
        NumeratedUnits = self.get_NumeratedUnits(num_mentions=num_mentions)
        NumeratedEntities = self.get_NumeratedEntities(num_mentions=num_mentions)
        NumeratedUnitsAsInputVars = self.get_NumeratedUnitsAsInputVars(num_mentions=num_mentions)
        NumeratedUnitsAsInputVarsConcat = self.get_NumeratedUnitsAsInputVarsConcat(num_mentions=num_mentions)

        NumeratedUnitDerivationRules = self.get_NumeratedUnitDerivationRules(num_mentions=num_mentions)
        NumeratedRightContextMaterialisationRules = self.get_NumeratedRightContextMaterialisationRules(
            right_contexts=contexts[1:])
        NumeratedMentionMaterialisationRules = self.get_NumeratedMentionMaterialisationRules(mentions=mentions)

        # flatten the list of lists
        all_entities = [entity for entity_list in entities for entity in entity_list]
        EntitiesMaterialisationRules = self.batch_get_decoding_linearization_rules(entities=all_entities, rm_eos=True,
                                                                                   rm_bos=True)

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           crt_grammar_name=crt_grammar_name,
                                                           bog_tokens="[]",
                                                           # self.get_entity_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False)
                                                           eog_tokens=f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',
                                                           # "2" for llama and "1" for T5
                                                           open_bracket_tokens=self.get_entity_tokens(
                                                               self.Open_bracket_marker, rm_eos=True),
                                                           close_bracket_tokens=self.get_entity_tokens(
                                                               self.Close_bracket_marker, rm_eos=True),
                                                           left_context0_tokens=self.get_entity_tokens(
                                                               entity=left_context0, rm_eos=True),
                                                           start_marker_tokens=self.get_entity_tokens(
                                                               entity=self.StartMarker, rm_eos=True),
                                                           end_marker_tokens=self.get_entity_tokens(
                                                               entity=self.EndMarker, rm_eos=True),
                                                              NumeratedMentions=NumeratedMentions,
                                                              NumeratedRightContexts=NumeratedRightContexts,
                                                                NumeratedUnits=NumeratedUnits,
                                                                NumeratedEntities=NumeratedEntities,
                                                                NumeratedUnitsAsInputVars=NumeratedUnitsAsInputVars,
                                                                NumeratedUnitsAsInputVarsConcat=NumeratedUnitsAsInputVarsConcat,
                                                           NumeratedUnitDerivationRules=NumeratedUnitDerivationRules,
                                                           NumeratedMentionMaterialisationRules=NumeratedMentionMaterialisationRules,
                                                           NumeratedRightContextMaterialisationRules=NumeratedRightContextMaterialisationRules,
                                                           Materialize_Entities=EntitiesMaterialisationRules)
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)

    def get_NumeratedMentions(self, num_mentions: int):
        mentions = [self.NUMERATED_MENTION_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " , ".join(mentions)

    def get_NumeratedRightContexts(self, num_mentions: int):
        right_contexts = [self.NUMERATED_RIGHT_CONTEXT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " , ".join(right_contexts)

    def get_NumeratedUnits(self, num_mentions: int):
        units = [self.NUMERATED_UNIT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " , ".join(units)

    def get_NumeratedEntities(self, num_mentions: int):
        entities = [self.NUMERATED_ENTITY_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ; ".join(entities)

    def get_NumeratedUnitsAsInputVars(self, num_mentions: int):
        units = [self.NUMERATED_UNIT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ".join(units)

    def get_NumeratedUnitsAsInputVarsConcat(self, num_mentions: int):
        units = [self.NUMERATED_UNIT_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return " ++ ".join(units)

    def get_NumeratedUnitDerivationRules(self, num_mentions: int):
        rules = [self.NUMERATED_UNIT_DERIVATION_RULE_TEMPLATE.format(i=i) for i in range(num_mentions)]
        return self.join_statements_multi_line(statements=rules)

    def get_NumeratedRightContextMaterialisationRules(self, right_contexts: List[str] = None):
        right_context_tokens: List[str] = [self.get_entity_tokens(entity=right_context, rm_eos=True) for right_context
                                           in right_contexts]
        rules = [self.NUMERATED_RIGHT_CONTEXT_MATERIALISATION_RULE_TEMPLATE.format(i=i,tokens=
        right_context_tokens[i]) for i in range(len(right_contexts))]
        return self.join_statements_multi_line(statements=rules)

    def get_NumeratedMentionMaterialisationRules(self, mentions: List[str] = None):
        mention_tokens: List[str] = [self.get_entity_tokens(entity=mention, rm_eos=True) for mention in mentions]
        rules = [self.NUMERATED_MENTION_MATERIALISATION_RULE_TEMPLATE.format(i=i, tokens=mention_tokens[i]) for
                 i in range(len(mentions))]
        return self.join_statements_multi_line(statements=rules)


if __name__ == '__main__':
    grammar_builder = ED_DepMultiMentionCrtGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=True)
    grammar = grammar_builder.build(base_grammar_name="ED-efficient", mentions=["mention0","mention1","mention2"],contexts=["context0","context1","context2", "context3"],entities_or_path=[["ent0", "ent1", "ent2"]])
    grammar.save("./ED-efficient")



