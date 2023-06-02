#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
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
from .const import PHRASE_LEVEL_TAGS, FUNCTIONAL_TAGS, WORD_LEVEL_TAGS, NUM_TAGS
from .crt_grammar import CPCrtGrammarBuilder

class CPotfCrtGrammarBuilder(CPCrtGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "CP", "CP-OTF-PTB-CrtTemplate.hs")
    grammar_prefix = ""  # "SubjectCollapsed"


    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)
        self.Hyphen = "-"
        self.S = "S"
        self.Left_Paren = "("
        self.Right_Paren = ")"
        self.Input_Word = "XX"
        self.Space = " "

    def build(self, base_grammar_name: str, crt_grammar_name=None, input_sentence=None) -> Grammar:
        assert input_sentence is not None, "input_sentence should not be None"
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)

        constituency_linearization_rules = self.add_constituency_linearization_rules()
        input_substring_materialise_rules = self.add_input_substring_materialise_rules(input_sentence=input_sentence)
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           crt_grammar_name=crt_grammar_name,
                                                           Hyphen=self.get_entity_tokens(entity=self.Hyphen, rm_bos=True, rm_eos=True),#, pseudo_prefix="Ж"
                                                           S=self.get_entity_tokens(entity=self.S, rm_bos=True, rm_eos=True),
                                                           Space=self.get_entity_tokens(entity=self.Space, rm_bos=True, rm_eos=True),
                                                           Left_Paren=self.get_entity_tokens(entity=self.Left_Paren, rm_bos=True, rm_eos=True),
                                                           Right_Paren=self.get_entity_tokens(entity=self.Right_Paren, rm_bos=True, rm_eos=True),
                                                           Input_Word=self.get_entity_tokens(entity=self.Input_Word, rm_bos=True, rm_eos=True),
                                                           constituency_linerization_rules=constituency_linearization_rules,
                                                           input_substring_materialise_rules=input_substring_materialise_rules)
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)

    def add_input_substring_materialise_rules(self, input_sentence: str):
        token_ids = self.tokenizer.encode(input_sentence, add_special_tokens=False)
        rules = []
        input_token_num = len(token_ids)
        for i in range(input_token_num):
            for j in range(i+1, input_token_num+1):
                rules.append(self.get_input_substring_materialise_rule(i, j, input_sentence=input_sentence))

        return self.join_statements_multi_line(statements=rules)

    def get_input_substring_materialise_rule(self, start_idx, end_idx, input_sentence):
        rule = self.get_materialization_rule(rule_name=f"Derive_InputSubstring_{start_idx}_{end_idx}",entity=input_sentence, start_idx=start_idx, end_idx=end_idx)
        return rule



if __name__ == '__main__':

    grammar_builder = CPotfCrtGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B",literal=False)
    grammar = grammar_builder.build(base_grammar_name="CP-PTB", crt_grammar_name="CP-PTB-Crt", input_sentence="hello world")
    grammar.save("./CP-PTB-OTF")