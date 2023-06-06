#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.CP.indep.indep_abs_grammar import CP_IndepPtbAbsGrammarBuilder


class CP_DepPtbAbsGrammarBuilder(CP_IndepPtbAbsGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "CP", "dep", "ptb", "CP-Dep-PTB-AbsTemplate.hs")
    grammar_prefix = ""

    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, input_sentence:str) -> Grammar:
        grammar: str = self.read_template()

        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        constituency_derivation_rules = self.add_constituency_derivation_rules()

        input_substring_materialise_rules = self.add_input_substring_materialise_rules(input_sentence=input_sentence)

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           constituency_derivation_rules=constituency_derivation_rules,
                                                           input_substring_materialise_rules=input_substring_materialise_rules)

        return Grammar(formatted_grammar_plain_text, name=abs_grammar_name)

    def add_input_substring_materialise_rules(self, input_sentence:str) -> str:

        input_token_ids = self.tokenizer.encode(input_sentence, add_special_tokens=False)
        input_token_num = len(input_token_ids)
        rules = []
        for i in range(input_token_num):
            for j in range(i+1, input_token_num+1):
                rules.append(self.get_input_substring_materialise_rule(i, j))
        return self.join_statements_multi_line(statements=rules)

    def get_input_substring_materialise_rule(self, start_idx:int, end_idx:int) -> str:
        return f"Derive_InputSubstring_{start_idx}_{end_idx}: Input_word ;"




if __name__ == '__main__':
    grammar = CP_DepPtbAbsGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=False) \
        .build(base_grammar_name="CP-PTB", input_sentence="Hello World")
    grammar.save("./CP-PTB-OTF")