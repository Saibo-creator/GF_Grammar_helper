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
    template = os.path.join(TEMPLATE_DIR, "EL", "ELAbsTemplate.txt")
    grammar_prefix = ""  # "SubjectCollapsed"
    grammar_suffix = ""

    def __init__(self):
        super().__init__()

    def build(self, base_grammar_name: str, entities_or_path: Union[List[str], str], tokenizer_or_path) -> Grammar:
        grammar: str = self.read_template()
        entities: List[str] = self.read_jsonl(entities_or_path) if isinstance(entities_or_path,
                                                                              str) else entities_or_path
        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        formatted_grammar: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                entities_str=self.get_entities_str(entities=entities))
        grammar_meta = self.build_meta(entities=entities)

        return Grammar(formatted_grammar, name=abs_grammar_name, meta=grammar_meta)

    def build_entities_ids(self, entities: List[str]) -> Dict[str, str]:
        return {self.get_tokenization_func_name(entity=entity): entity for entity in entities}

    def build_meta(self, entities: List[str]):
        entities_ids: Dict[str, str] = self.build_entities_ids(entities=entities)
        return {"entities": entities_ids}

    def get_entities_str(self, entities: List[str]) -> str:
        entities_id_map: Dict[str, str] = self.build_entities_ids(entities=entities)
        entities_ids = [entity_key if i == len(entities_id_map) - 1 else entity_key + "," for i, entity_key in
                        enumerate(entities_id_map.keys())]
        return self.join_statements_multi_line(statements=entities_ids)
