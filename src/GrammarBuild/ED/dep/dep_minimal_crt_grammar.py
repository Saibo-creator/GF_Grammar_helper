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


class ED_DepMinimalCrtGrammarBuilder(ED_IndepMinimalCrtGrammarBuilder, ABC):

    template = os.path.join(
        TEMPLATE_DIR, "ED", "Dep", "minimal", "ED-Dep-Minimal-CrtTemplate.hs"
    )
    grammar_prefix = ""

    Open_bracket_marker = "["
    Close_bracket_marker = "]"

    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        entities_or_path: Union[List[str], str, List[List[str]]] = kwargs[
            "entities_or_path"
        ]
        crt_grammar_name = kwargs.get("crt_grammar_name", None)
        mention: str = kwargs["mention"]
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(
                base_grammar_name=base_grammar_name, crt=True
            )
        entities = (
            self.read_jsonl(entities_or_path)
            if isinstance(entities_or_path, str)
            else entities_or_path
        )
        formatted_grammar_plain_text: str = grammar.format(
            abs_grammar_name=abs_grammar_name,
            crt_grammar_name=crt_grammar_name,
            bog_tokens="[]",  # self.get_entity_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False)
            eog_tokens=f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',  # "2" for llama and "1" for T5
            mention_tokens=self.get_entity_tokens(entity=mention, rm_eos=True),
            open_bracket_tokens=self.get_entity_tokens(
                self.Open_bracket_marker, rm_eos=True
            ),
            close_bracket_tokens=self.get_entity_tokens(
                self.Close_bracket_marker, rm_eos=True
            ),
            Materialize_Entities=self.batch_get_decoding_linearization_rules(
                entities=entities, rm_eos=True, rm_bos=True
            ),
        )
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)
