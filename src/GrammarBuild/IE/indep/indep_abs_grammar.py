#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from typing import List, Union, Dict
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.grammar_builder import TemplateTokenGrammarBuilder


class IE_AbsGrammarBuilder(TemplateTokenGrammarBuilder):

    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        entities_or_path: Union[List[str], str, List[List[str]]] = kwargs["entities_or_path"]
        relations_or_path: Union[List[str], str, List[List[str]]] = kwargs["relationss_or_path"]
        grammar: str = self.read_template()
        entities: List[str] = self.read_jsonl(entities_or_path) if isinstance(entities_or_path,
                                                                              str) else entities_or_path
        relations: List[str] = self.read_jsonl(relations_or_path) if isinstance(relations_or_path,
                                                                                str) else relations_or_path

        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                Materialize_Entities=self.add_entities_derivative_rules(entities=entities),
                                                Materialize_Relations=self.add_relations_derivative_rules(relations=relations))
        grammar_meta = self.build_meta(entities=entities, relations=relations)

        return Grammar(formatted_grammar_plain_text, name=abs_grammar_name, meta=grammar_meta)

    def assign_entities_ids(self, entities: List[str]) -> Dict[str, str]:
        return {self.get_tokenization_func_name(entity=entity): entity for entity in entities}

    def assign_relations_ids(self, relations: List[str]) -> Dict[str, str]:
        return {self.get_tokenization_func_name(rel=relation): relation for relation in relations}

    def build_meta(self, entities: List[str], relations: List[str]):
        entities_ids: Dict[str, str] = self.assign_entities_ids(entities=entities)
        relations_ids: Dict[str, str] = self.assign_relations_ids(relations=relations)
        return {"entities": entities_ids, "relations": relations_ids}

    def add_entities_derivative_rules(self, entities: List[str]) -> str:
        entities_id_map: Dict[str, str] = self.assign_entities_ids(entities=entities)
        entities_ids = [entity_key if i == len(entities_id_map)-1 else entity_key+"," for i, entity_key in enumerate(entities_id_map.keys()) ]
        return self.join_statements_multi_line(statements=entities_ids)

    def add_relations_derivative_rules(self, relations: List[str]) -> str:
        relations_id_map: Dict[str, str] = self.assign_relations_ids(relations=relations)
        relations_ids = [relation_key if i == len(relations_id_map)-1 else relation_key+"," for i, relation_key in enumerate(relations_id_map.keys()) ]
        return self.join_statements_multi_line(statements=relations_ids)


class IE_IndepFullyExpandedAbsGrammarBuilder(IE_AbsGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "IE", "InDep", "FE", "IE-Indep-FullyExpanded-AbsTemplate.hs")
    grammar_prefix = "" # "FullyExpanded"


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)


class IE_IndepSubjectCollapsedAbsGrammarBuilder(IE_AbsGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "IE", "InDep", "SC", "IE-Indep-SubjectCollapsed-AbsTemplate.hs")
    grammar_prefix = "" # "SubjectCollapsed"


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

