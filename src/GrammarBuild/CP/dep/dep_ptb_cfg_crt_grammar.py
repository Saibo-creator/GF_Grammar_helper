#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os

from src.GrammarBuild.CP.const import WORD_LEVEL_TAGS, FULL_PHRASE_LEVEL_TAGS
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.CP.indep.indep_crt_grammar import CP_IndepPtbCrtGrammarBuilder

class CP_DepPtbCfgCrtGrammarBuilder(CP_IndepPtbCrtGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "CP", "Dep", "ptb-cfg", "CP-Dep-PTB-CrtTemplate.hs")
    grammar_prefix = ""  # "SubjectCollapsed"


    Open_bracket_marker = "["
    Close_bracket_marker = "]"

    Hyphen = "-"
    S = "S"
    Left_Paren = "("
    Right_Paren = ")"
    Input_Word = "XX"
    Space = " "

    FullPhraseLevelTags = FULL_PHRASE_LEVEL_TAGS
    WordLevelTags = WORD_LEVEL_TAGS


    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)


    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        crt_grammar_name = kwargs.get("crt_grammar_name", None)
        input_sentence = kwargs["text"]
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)

        constituency_linearization_rules = self.add_constituency_linearization_rules()
        Derive_FullPhraseLevelTags = self.get_Derive_FullPhraseLevelTags()
        Derive_WordTags = self.get_Derive_WordLevelTags()
        input_substring_materialise_rules = self.add_input_substring_materialise_rules(input_sentence=input_sentence)
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           crt_grammar_name=crt_grammar_name,
                                                           # Hyphen=self.get_entity_tokens(entity=self.Hyphen, rm_bos=True, rm_eos=True),#, pseudo_prefix="Ж"
                                                           # S=self.get_entity_tokens(entity=self.S, rm_bos=True, rm_eos=True),
                                                           # Space=self.get_entity_tokens(entity=self.Space, rm_bos=True, rm_eos=True),
                                                           Left_Paren=self.get_entity_tokens(entity=self.Left_Paren, rm_bos=True, rm_eos=True),
                                                           Right_Paren=self.get_entity_tokens(entity=self.Right_Paren, rm_bos=True, rm_eos=True),
                                                           Input_Word=self.get_entity_tokens(entity=self.Input_Word, rm_bos=True, rm_eos=True),
                                                           # constituency_linerization_rules=constituency_linearization_rules,
                                                           input_substring_materialise_rules=input_substring_materialise_rules,
                                                           bog_tokens="[]",
                                                           eog_tokens=f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',
                                                           Derive_FullPhraseLevelTags=Derive_FullPhraseLevelTags,
                                                           Derive_WordTags=Derive_WordTags,
                                                           open_bracket_tokens=self.get_entity_tokens(self.Open_bracket_marker, rm_eos=True),
                                                           close_bracket_tokens=self.get_entity_tokens(self.Close_bracket_marker, rm_eos=True))
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

    def get_Derive_FullPhraseLevelTags(self, ) -> str:
        return self.join_statements_multi_line(statements=[self.get_materialization_rule(rule_name=f'Derive_FullPhraseLevelTag_{tag.replace("-","_")}',entity=tag)
                                                           for tag in self.FullPhraseLevelTags])

    def get_Derive_WordLevelTags(self, ) -> str:
        return self.join_statements_multi_line(statements=[self.get_materialization_rule(rule_name=f'Derive_WordLevelTag_{tag.replace("-","_").replace("$","Dollar")}',entity=tag)
                                                           for tag in self.WordLevelTags])



if __name__ == '__main__':

    grammar_builder = CP_DepPtbCfgCrtGrammarBuilder(tokenizer_or_path="/home/saibo/Research/llama_models/7B", literal=False)
    grammar = grammar_builder.build(base_grammar_name="CP_PTB", crt_grammar_name="CP_PTB_Crt", text="hello world")
    grammar.save("./CP-PTB-OTF")