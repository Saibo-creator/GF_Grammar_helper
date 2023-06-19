#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from typing import List

from src.config.config import TEMPLATE_DIR
from src.GrammarBuild.CP.const import WORD_LEVEL_TAGS, FULL_PHRASE_LEVEL_TAGS

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.CP.indep.indep_crt_grammar import CP_IndepPtbCrtGrammarBuilder

class CP_DepPtbCrtGrammarBuilder(CP_IndepPtbCrtGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "CP", "dep", "ptb-re", "CP-Dep-PTB-CrtTemplate.hs")
    grammar_prefix = ""  # "SubjectCollapsed"
    Left_Paren = "("
    Right_Paren = ")"
    Space = " "
    FullPhraseLevelTags = FULL_PHRASE_LEVEL_TAGS
    WordLevelTags = WORD_LEVEL_TAGS

    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)
        # self.Hyphen = "-"
        # self.S = "S"


    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        crt_grammar_name = kwargs.get("crt_grammar_name", None)
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)

        input_words: list = kwargs["words"]
        num_input_words: int = len(input_words)

        Rule0_0D = self.get_Rule0_0D()
        Rule1_2D = self.get_Rule1_2D(n_words=num_input_words)
        Rule2_2D = self.get_Rule2_2D(n_words=num_input_words)
        Rule3_2D = "" # Rule3_2D = self.get_Rule3_2D(n_words=num_input_words)
        Rule4_2D = self.get_Rule4_2D(n_words=num_input_words)
        Rule5_1D = self.get_Rule5_1D(n_words=num_input_words)
        Rule6_2D = self.get_Rule6_2D(n_words=num_input_words)
        Rule7_2D = self.get_Rule7_2D(n_words=num_input_words)
        Rule8_1D = self.get_Rule8_1D(n_words=num_input_words)
        Rule9_0D = self.get_Rule9_0D(n_words=num_input_words)

        RuleW_1D = self.get_RuleW_1D(words=input_words)

        cat_B_2D = self.get_cat_B_2D(n_words=num_input_words)
        cat_C_2D = self.get_cat_C_2D(n_words=num_input_words)
        cat_E_2D = self.get_cat_E_2D(n_words=num_input_words)
        cat_W_1D = self.get_cat_W_1D(n_words=num_input_words)

        Derive_FullPhraseLevelTags = self.get_Derive_FullPhraseLevelTags()
        Derive_WordTags = self.get_Derive_WordLevelTags()

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                           crt_grammar_name=crt_grammar_name,
                                                           Hyphen=self.get_entity_tokens(entity=self.Hyphen, rm_bos=True, rm_eos=True),#, pseudo_prefix="Ж"
                                                           S=self.get_entity_tokens(entity=self.S, rm_bos=True, rm_eos=True),
                                                           Space=self.get_entity_tokens(entity=self.Space, rm_bos=True, rm_eos=True),
                                                           Left_Paren=self.get_entity_tokens(entity=self.Left_Paren, rm_bos=True, rm_eos=True),
                                                           Right_Paren=self.get_entity_tokens(entity=self.Right_Paren, rm_bos=True, rm_eos=True),
                                                           Rule0_0D=Rule0_0D,
                                                           Rule1_2D=Rule1_2D,
                                                           Rule2_2D=Rule2_2D,
                                                           Rule3_2D=Rule3_2D,
                                                           Rule4_2D=Rule4_2D,
                                                           Rule5_1D=Rule5_1D,
                                                           Rule6_2D=Rule6_2D,
                                                           Rule7_2D=Rule7_2D,
                                                           Rule8_1D=Rule8_1D,
                                                           Rule9_0D=Rule9_0D,
                                                           RuleW_1D=RuleW_1D,
                                                           cat_B_2D=cat_B_2D,
                                                           cat_C_2D=cat_C_2D,
                                                           cat_E_2D=cat_E_2D,
                                                           cat_W_1D=cat_W_1D,
                                                           Derive_FullPhraseLevelTags=Derive_FullPhraseLevelTags,
                                                           Derive_WordTags=Derive_WordTags,
                                                           )
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)


    def get_cat_B_2D(self, n_words:int) -> str:
        return  ",".join([self.get_cat_B_single(i, j) for i in range(n_words) for j in range(n_words+1)])

    def get_cat_B_single(self, i:int, j:int) -> str:
        return f"B_{i}_{j}"

    def get_cat_C_2D(self, n_words:int) -> str:
        return  ",".join([self.get_cat_C_single(i, j) for i in range(n_words+1) for j in range(n_words+2)])

    def get_cat_C_single(self, i:int, j:int) -> str:
        return f"C_{i}_{j}"

    def get_cat_E_2D(self, n_words:int) -> str:
        return  ",".join([self.get_cat_E_single(i, j) for i in range(n_words+1) for j in range(n_words+2)])

    def get_cat_E_single(self, i:int, j:int) -> str:
        return f"E_{i}_{j}"

    def get_cat_W_1D(self, n_words:int) -> str:
        return  ",".join([self.get_cat_W_single(i) for i in range(n_words)])

    def get_cat_W_single(self, i:int) -> str:
        return f"W{i}"


    def get_Rule0_0D(self) -> str:
        "Rule0 : B_0_0 -> S;"

        return "Rule0 a b c d = a ++ b ++ c ++ d ;"

    def get_Rule1_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule1_2D_single(i, j ) for i in range(n_words) for j in range(n_words)])

    def get_Rule1_2D_single(self, i:int, j:int) -> str:
        """Rule1_B_1_0 : Left -> FullPhraseLevelTag -> B_1_1 -> B_1_0 ;"""
        return f"Rule1_B_{i}_{j} a b c = a ++ b ++ c ;"

    def get_Rule2_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule2_2D_single(i, j ) for i in range(n_words) for j in range(n_words+1)])

    def get_Rule2_2D_single(self, i:int, j:int) -> str:
        "    Rule2_B_0_0 :=Left -> FullPhraseLevelTag -> C_0_1 -> B_0_0 ;"
        return f"Rule2_B_{i}_{j} a b c = a ++ b ++ c ;"

    def get_Rule3_2D(self, n_words:int) -> str:
        raise NotImplementedError

    def get_Rule3_2D_single(self, i:int, j:int) -> str:
        raise NotImplementedError

    def get_Rule4_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule4_2D_single(i, j ) for i in range(n_words) for j in range(n_words+2)])

    def get_Rule4_2D_single(self, i:int, j:int) -> str:
        "Rule4_C_1_0W1 -> E_2_0 -> C_1_0 ;"
        return f"Rule4_C_{i}_{j} a b = a ++ b ;"

    def get_Rule5_1D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule5_1D_single(i,n_words) for i in range(n_words+1)])

    def get_Rule5_1D_single(self, i:int, n_words:int) -> str:
        "Rule5_C_3_1 E_3_1 -> C_3_1 ;"
        return f"Rule5_C_{n_words}_{i} a = a ;"

    def get_Rule6_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule6_2D_single(i, j ) for i in range(n_words) for j in range(1, n_words+1)])

    def get_Rule6_2D_single(self, i:int, j:int) -> str:
        "Rule6_E_0_2 Right -> E_0_1 -> E_0_2 ;"
        return f"Rule6_E_{i}_{j} a b = a ++ b ;"

    def get_Rule7_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule7_2D_single(i, j ) for i in range(n_words) for j in range(1, n_words+1)])

    def get_Rule7_2D_single(self, i:int, j:int) -> str:
        "Rule7_E_2_1 Right -> B_2_0 -> E_2_1 ;"
        return f"Rule7_E_{i}_{j} a b = a ++ b ;"

    def get_Rule8_1D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule8_1D_single(i,n_words) for i in range(1, n_words+1)])

    def get_Rule8_1D_single(self, i:int, n_words:int) -> str:
        "Rule8_E_3_2 Right -> E_3_1 -> E_3_2 ;"
        return f"Rule8_E_{n_words}_{i} a b = a ++ b ;"

    def get_Rule9_0D(self, n_words:int) -> str:
        "Rule9_E_3_0 E_3_0 ;"
        return f"Rule9_E_{n_words}_0 = [] ;"


    def get_RuleW_1D(self, words:List[str]) -> str:
        return self.join_statements_multi_line(statements=[self.get_RuleW_1D_single(i, entity=words[i]) for i in range(len(words))])

    def get_RuleW_1D_single(self, i:int, entity:str) -> str:
        "Materialize_W0 W0;"

        rule = self.get_materialization_rule(rule_name=f"Materialize_W{i}",entity=entity)
        return rule

    # def add_input_substring_materialise_rules(self, input_sentence: str):
    #     token_ids = self.tokenizer.encode(input_sentence, add_special_tokens=False)
    #     rules = []
    #     input_token_num = len(token_ids)
    #     for i in range(input_token_num):
    #         for j in range(i+1, input_token_num+1):
    #             rules.append(self.get_input_substring_materialise_rule(i, j, input_sentence=input_sentence))
    #
    #     return self.join_statements_multi_line(statements=rules)
    #
    # def get_input_substring_materialise_rule(self, start_idx, end_idx, input_sentence):
    #     rule = self.get_materialization_rule(rule_name=f"Derive_InputSubstring_{start_idx}_{end_idx}",entity=input_sentence, start_idx=start_idx, end_idx=end_idx)
    #     return rule

    def get_Derive_FullPhraseLevelTags(self, ) -> str:
        return self.join_statements_multi_line(statements=[self.get_materialization_rule(rule_name=f'Derive_FullPhraseLevelTag_{tag.replace("-","_")}',entity=tag)
                                                           for tag in self.FullPhraseLevelTags])

    def get_Derive_WordLevelTags(self, ) -> str:
        return self.join_statements_multi_line(statements=[self.get_materialization_rule(rule_name=f'Derive_WordLevelTag_{tag.replace("-","_").replace("$","Dollar")}',entity=tag)
                                                           for tag in self.WordLevelTags])



if __name__ == '__main__':

    grammar_builder = CP_DepPtbCrtGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=True)
    grammar = grammar_builder.build(base_grammar_name="CP_PTB_RE", crt_grammar_name="CP_PTB_RE_Crt", words=["I", "love", "you"])
    grammar.save("./CP-PTB-OTF-RE")