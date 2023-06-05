#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from typing import List, Union, Dict
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder


class ELAbsGrammarBuilder(TemplateTokenGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "EL", "ELAbsTemplate.hs")
    grammar_prefix = ""  # "SubjectCollapsed"


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, entities_or_path: Union[List[str], str, List[List[str]]], **kwargs) -> Grammar:
        grammar: str = self.read_template()
        entities: List[str] = self.read_jsonl(entities_or_path) if isinstance(entities_or_path,
                                                                              str) else entities_or_path
        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                Materialize_Entities=self.add_entities_derivative_rules(entities=entities))
        grammar_meta = self.build_meta(entities=entities)

        return Grammar(formatted_grammar_plain_text, name=abs_grammar_name, meta=grammar_meta)

    def assign_entities_ids(self, entities: List[str]) -> Dict[str, str]:
        return {self.get_tokenization_func_name(entity=entity): entity for entity in entities}

    def build_meta(self, entities: List[str]):
        entities_ids: Dict[str, str] = self.assign_entities_ids(entities=entities)
        return {"entities": entities_ids}

    def add_entities_derivative_rules(self, entities: List[str], entity_idx=None) -> str:
        """Spaghetti code, but it works. TODO: refactor this function."""
        entities_id_map: Dict[str, str] = self.assign_entities_ids(entities=entities)
        entities_ids = [entity_key if i == len(entities_id_map) - 1 else entity_key + "," for i, entity_key in
                        enumerate(entities_id_map.keys())]

        statement = self.join_statements_multi_line(statements=entities_ids) + f": Entity{entity_idx};" if entity_idx is not None else self.join_statements_multi_line(statements=entities_ids)
        return statement
