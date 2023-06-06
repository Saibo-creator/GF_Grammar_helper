#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb
from abc import ABC, abstractmethod
from typing import List, Union

from tqdm import tqdm

from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder
from src.GrammarBuild.CP.const import PHRASE_LEVEL_TAGS, FUNCTIONAL_TAGS, WORD_LEVEL_TAGS, NUM_TAGS


class CP_IndepPtbCrtGrammarBuilder(TemplateTokenGrammarBuilder, ABC):
    template = os.path.join(TEMPLATE_DIR, "CP", "indep", "ptb", "CP-Indep-PTB-CrtTemplate.hs")
    grammar_prefix = ""  # "SubjectCollapsed"


    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)
        self.Hyphen = "-"
        self.S = "S"
        self.Left_Paren = "("
        self.Right_Paren = ")"
        self.Input_Word = "XX"
        self.Space = " "

    def build(self, base_grammar_name: str, crt_grammar_name=None, **kwargs) -> Grammar:
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)

        constituency_linearization_rules = self.add_constituency_linearization_rules()
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           crt_grammar_name=crt_grammar_name,
                                                           Hyphen=self.get_entity_tokens(entity=self.Hyphen, rm_bos=True, rm_eos=True),#, pseudo_prefix="Ж"
                                                           S=self.get_entity_tokens(entity=self.S, rm_bos=True, rm_eos=True),
                                                           Space=self.get_entity_tokens(entity=self.Space, rm_bos=True, rm_eos=True),
                                                           Left_Paren=self.get_entity_tokens(entity=self.Left_Paren, rm_bos=True, rm_eos=True),
                                                           Right_Paren=self.get_entity_tokens(entity=self.Right_Paren, rm_bos=True, rm_eos=True),
                                                           Input_Word=self.get_entity_tokens(entity=self.Input_Word, rm_bos=True, rm_eos=True),
                                                           constituency_linerization_rules=constituency_linearization_rules)
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)

    def add_constituency_linearization_rules(self):
        rules = []
        for tag in PHRASE_LEVEL_TAGS:
            rules.append(self.get_PhraseLevelTag_LinearizationRule(tag=tag))
        for tag in FUNCTIONAL_TAGS:
            rules.append(self.get_HyphenFunctionTag_LinearizationRule(tag=tag))
        for tag in WORD_LEVEL_TAGS:
            rules.append(self.get_WordLevelTag_LinearizationRule(tag=tag))
        for tag in NUM_TAGS:
            rules.append(self.get_HyphenNumTag_LinearizationRule(tag=tag))
        return self.join_statements_multi_line(statements=rules)

    def get_PhraseLevelTag_LinearizationRule(self, tag: str) -> str:
        tag_var_name = self.normalize_tag(tag=tag)
        rule_name = f"Derive_PhraseLevelTag_{tag_var_name}"
        materialization_rule: str = self.get_materialization_rule(rule_name=rule_name, entity=tag)
        return materialization_rule

    def get_HyphenFunctionTag_LinearizationRule(self, tag: str) -> str:
        tag_var_name = self.normalize_tag(tag=tag)
        rule_name = f"Derive_HyphenFunctionTag_{tag_var_name}"
        hyphen_tag = f"{self.Hyphen}{tag}"
        materialization_rule: str = self.get_materialization_rule(rule_name=rule_name, entity=hyphen_tag, pseudo_prefix=True)
        return materialization_rule

    def get_WordLevelTag_LinearizationRule(self, tag: str) -> str:
        tag_var_name = self.normalize_tag(tag=tag)
        rule_name = f"Derive_WordLevelTag_{tag_var_name}"
        materialization_rule: str = self.get_materialization_rule(rule_name=rule_name, entity=tag)
        return materialization_rule

    def get_HyphenNumTag_LinearizationRule(self, tag: str) -> str:
        rule_name = f"Derive_HyphenNumTag_{tag}"
        hyphen_tag = f"{self.Hyphen}{tag}"
        materialization_rule: str = self.get_materialization_rule(rule_name=rule_name, entity=hyphen_tag, pseudo_prefix=True)
        return materialization_rule

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

    grammar = CP_IndepPtbCrtGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=False).build(base_grammar_name="CP-PTB",
                                                                                                                       crt_grammar_name="CP-PTB-Crt"
                                                                                                                       )
    grammar.save("./CP-PTB-Abs")