#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb

from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.CP.indep.indep_abs_grammar import CP_IndepPtbAbsGrammarBuilder
from src.GrammarBuild.CP.const import WORD_LEVEL_TAGS, FULL_PHRASE_LEVEL_TAGS

class CP_DepPtbAbsGrammarBuilder(CP_IndepPtbAbsGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "CP", "dep", "ptb-re", "CP-Dep-PTB-AbsTemplate.hs")
    grammar_prefix = ""

    FullPhraseLevelTags = FULL_PHRASE_LEVEL_TAGS
    WordLevelTags = WORD_LEVEL_TAGS

    def __init__(self, tokenizer_or_path: str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, **kwargs) -> Grammar:
        grammar: str = self.read_template()
        input_words: list = kwargs["words"]
        num_input_words: int = len(input_words)

        abs_grammar_name = self.get_grammar_name(base_grammar_name)

        Rule0_0D = self.get_Rule0_0D()
        Rule1_2D = self.get_Rule1_2D(n_words=num_input_words)
        Rule2_2D = self.get_Rule2_2D(n_words=num_input_words)
        Rule3_2D = ""# Rule3_2D = self.get_Rule3_2D(n_words=num_input_words)
        Rule4_2D = self.get_Rule4_2D(n_words=num_input_words)
        Rule5_1D = self.get_Rule5_1D(n_words=num_input_words)
        Rule6_2D = self.get_Rule6_2D(n_words=num_input_words)
        Rule7_2D = self.get_Rule7_2D(n_words=num_input_words)
        Rule8_1D = self.get_Rule8_1D(n_words=num_input_words)
        Rule9_0D = self.get_Rule9_0D(n_words=num_input_words)

        RuleW_1D = self.get_RuleW_1D(n_words=num_input_words)

        cat_B_2D = self.get_cat_B_2D(n_words=num_input_words)
        cat_C_2D = self.get_cat_C_2D(n_words=num_input_words)
        cat_E_2D = self.get_cat_E_2D(n_words=num_input_words)
        cat_W_1D = self.get_cat_W_1D(n_words=num_input_words)

        Derive_FullPhraseLevelTags = self.get_Derive_FullPhraseLevelTags()
        Derive_WordTags = self.get_Derive_WordLevelTags()


        # constituency_derivation_rules = self.add_constituency_derivation_rules()

        # input_substring_materialise_rules = self.add_input_substring_materialise_rules(input_sentence=input_sentence)

        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name,
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

        return Grammar(formatted_grammar_plain_text, name=abs_grammar_name)

    def get_cat_B_2D(self, n_words:int) -> str:
        return  ";".join([self.get_cat_B_single(i, j) for i in range(n_words) for j in range(n_words+1)])

    def get_cat_B_single(self, i:int, j:int) -> str:
        return f"B_{i}_{j}"

    def get_cat_C_2D(self, n_words:int) -> str:
        return  ";".join([self.get_cat_C_single(i, j) for i in range(n_words+1) for j in range(n_words+2)])

    def get_cat_C_single(self, i:int, j:int) -> str:
        return f"C_{i}_{j}"

    def get_cat_E_2D(self, n_words:int) -> str:
        return  ";".join([self.get_cat_E_single(i, j) for i in range(n_words+1) for j in range(n_words+2)])

    def get_cat_E_single(self, i:int, j:int) -> str:
        return f"E_{i}_{j}"

    def get_cat_W_1D(self, n_words:int) -> str:
        return  ";".join([self.get_cat_W_single(i) for i in range(n_words)])

    def get_cat_W_single(self, i:int) -> str:
        return f"W{i}"


    def get_Rule0_0D(self) -> str:
        "Rule0 : B_0_0 -> S;"
        return "Rule0 : Left -> FullPhraseLevelTag -> B_0_0 -> Right -> S;"

    def get_Rule1_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule1_2D_single(i, j ) for i in range(n_words) for j in range(n_words)])

    def get_Rule1_2D_single(self, i:int, j:int) -> str:
        """Rule1_B_1_0 : Left -> FullPhraseLevelTag -> B_1_1 -> B_1_0 ;"""
        return f"Rule1_B_{i}_{j} : Left -> FullPhraseLevelTag -> B_{i}_{j+1} -> B_{i}_{j} ;"

    def get_Rule2_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule2_2D_single(i, j ) for i in range(n_words) for j in range(n_words+1)])

    def get_Rule2_2D_single(self, i:int, j:int) -> str:
        "    Rule2_B_0_0 : Left -> FullPhraseLevelTag -> C_0_1 -> B_0_0 ;"
        return f"Rule2_B_{i}_{j} : Left -> FullPhraseLevelTag -> C_{i}_{j+1} -> B_{i}_{j} ;"

    def get_Rule3_2D(self, n_words:int) -> str:
        raise NotImplementedError

    def get_Rule3_2D_single(self, i:int, j:int) -> str:
        raise NotImplementedError

    def get_Rule4_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule4_2D_single(i, j ) for i in range(n_words) for j in range(n_words+2)])

    def get_Rule4_2D_single(self, i:int, j:int) -> str:
        "Rule4_C_1_0 : W1 -> E_2_0 -> C_1_0 ;"
        return f"Rule4_C_{i}_{j} : W{i} -> E_{i+1}_{j} -> C_{i}_{j} ;"

    def get_Rule5_1D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule5_1D_single(i,n_words) for i in range(n_words+1)])

    def get_Rule5_1D_single(self, i:int, n_words:int) -> str:
        "Rule5_C_3_1 : E_3_1 -> C_3_1 ;"
        return f"Rule5_C_{n_words}_{i} : E_{n_words}_{i} -> C_{n_words}_{i} ;"

    def get_Rule6_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule6_2D_single(i, j ) for i in range(n_words) for j in range(1, n_words+1)])

    def get_Rule6_2D_single(self, i:int, j:int) -> str:
        "Rule6_E_0_2 : Right -> E_0_1 -> E_0_2 ;"
        return f"Rule6_E_{i}_{j} : Right -> E_{i}_{j-1} -> E_{i}_{j} ;"

    def get_Rule7_2D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule7_2D_single(i, j ) for i in range(n_words) for j in range(1, n_words+1)])

    def get_Rule7_2D_single(self, i:int, j:int) -> str:
        "Rule7_E_2_1 : Right -> B_2_0 -> E_2_1 ;"
        return f"Rule7_E_{i}_{j} : Right -> B_{i}_{j-1} -> E_{i}_{j} ;"

    def get_Rule8_1D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_Rule8_1D_single(i,n_words) for i in  range(1, n_words+1)])

    def get_Rule8_1D_single(self, i:int, n_words:int) -> str:
        "Rule8_E_3_2 : Right -> E_3_1 -> E_3_2 ;"
        return f"Rule8_E_{n_words}_{i} : Right -> E_{n_words}_{i-1} -> E_{n_words}_{i} ;"

    def get_Rule9_0D(self, n_words:int) -> str:
        "Rule9_E_3_0 : E_3_0 ;"
        return f"Rule9_E_{n_words}_0 : E_{n_words}_0 ;"


    def get_RuleW_1D(self, n_words:int) -> str:
        return self.join_statements_multi_line(statements=[self.get_RuleW_1D_single(i) for i in range(n_words)])

    def get_RuleW_1D_single(self, i:int) -> str:
        "Materialize_W0 : W0;"
        return f"Materialize_W{i} : W{i} ;"


    def get_Derive_FullPhraseLevelTags(self) -> str:
        return self.join_statements_multi_line(statements=[self.get_Derive_FullPhraseLevelTags_single(tag.replace("-","_")) for tag in self.FullPhraseLevelTags])

    def get_Derive_FullPhraseLevelTags_single(self, tag:str) -> str:
        "Derive_FullPhraseLevelTag_NP : FullPhraseLevelTag;"
        return f"Derive_FullPhraseLevelTag_{tag} : FullPhraseLevelTag ;"

    def get_Derive_WordLevelTags(self) -> str:
        return self.join_statements_multi_line(statements=[self.get_Derive_WordLevelTags_single(tag.replace("-","_").replace("$","Dollar")) for tag in self.WordLevelTags])

    def get_Derive_WordLevelTags_single(self, tag:str) -> str:
        "Derive_WordLevelTag_NN : WordLevelTag;"
        return f"Derive_WordLevelTag_{tag} : WordLevelTag ;"

    # def add_input_substring_materialise_rules(self, input_sentence:str) -> str:
    #
    #     input_token_ids = self.tokenizer.encode(input_sentence, add_special_tokens=False)
    #     input_token_num = len(input_token_ids)
    #     rules = []
    #     for i in range(input_token_num):
    #         for j in range(i+1, input_token_num+1):
    #             rules.append(self.get_input_substring_materialise_rule(i, j))
    #     return self.join_statements_multi_line(statements=rules)
    #
    # def get_input_substring_materialise_rule(self, start_idx:int, end_idx:int) -> str:
    #     return f"Derive_InputSubstring_{start_idx}_{end_idx}: Input_word ;"




if __name__ == '__main__':
    grammar = CP_DepPtbAbsGrammarBuilder(tokenizer_or_path="/Users/saibo/Research/llama_hf/7B", literal=True) \
        .build(base_grammar_name="CP_PTB_RE", words=["I", "love", "you"])
    grammar.save("./CP-PTB-OTF-RE")