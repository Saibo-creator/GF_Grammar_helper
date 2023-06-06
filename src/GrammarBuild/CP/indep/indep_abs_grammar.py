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
from src.GrammarBuild.CP.const import PHRASE_LEVEL_TAGS, FUNCTIONAL_TAGS, WORD_LEVEL_TAGS, NUM_TAGS

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder


class CP_IndepPtbAbsGrammarBuilder(TemplateTokenGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "CP", "indep", "ptb", "CP-Indep-PTB-AbsTemplate.hs")
    grammar_prefix = ""


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, *args, **kwargs) -> Grammar:
        grammar: str = self.read_template()

        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        constituency_derivation_rules = self.add_constituency_derivation_rules()

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                constituency_derivation_rules=constituency_derivation_rules)

        return Grammar(formatted_grammar_plain_text, name=abs_grammar_name)

    def add_constituency_derivation_rules(self) -> str:
        rules = []
        for tag in PHRASE_LEVEL_TAGS:
            rules.append(self.get_PhraseLevelTag_BuildRule(tag=tag))
        for tag in FUNCTIONAL_TAGS:
            rules.append(self.get_HyphenFunctionTag_BuildRule(tag=tag))
        for tag in WORD_LEVEL_TAGS:
            rules.append(self.get_WordLevelTag_BuildRule(tag=tag))
        for tag in NUM_TAGS:
            rules.append(self.get_HyphenNumTag_BuildRule(tag=tag))
        return self.join_statements_multi_line(statements=rules)

    def get_PhraseLevelTag_BuildRule(self, tag: str) -> str:
        tag_var_name = CP_IndepPtbAbsGrammarBuilder.normalize_tag(tag=tag)
        return f"Derive_PhraseLevelTag_{tag_var_name}: PhraseLevelTag;"

    def get_HyphenFunctionTag_BuildRule(self, tag: str) -> str:
        tag_var_name = CP_IndepPtbAbsGrammarBuilder.normalize_tag(tag=tag)
        return f"Derive_HyphenFunctionTag_{tag_var_name}: HyphenFunctionTag;"

    def get_WordLevelTag_BuildRule(self, tag: str) -> str:
        tag_var_name = CP_IndepPtbAbsGrammarBuilder.normalize_tag(tag=tag)
        return f"Derive_WordLevelTag_{tag_var_name}: WordTag;"

    def get_HyphenNumTag_BuildRule(self, tag: str) -> str:
        return f"Derive_HyphenNumTag_{tag}: HyphenNumTag;"

    @staticmethod
    def normalize_tag(tag: str) -> str:
        # if tag contains dollar sign, replace it with "dollarsign"
        if "$" in tag:
            return tag.replace("$", "DollarSign")
        # if contains other special characters, raise error
        if not tag.isalnum():
            raise ValueError(f"Tag {tag} contains special characters, please check!")
        return tag


if __name__ == '__main__':

    grammar = CP_IndepPtbAbsGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=False)\
        .build(base_grammar_name="CP-PTB")
    grammar.save("./CP-PTB-Abs")